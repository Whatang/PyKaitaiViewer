'''
Created on 25 Jan 2018

@author: Mike Thomas
'''
import importlib
import os
import pprint
import subprocess
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import (QAbstractItemView, QStandardItemModel, QTreeWidgetItem,
                      QTextCursor, QTextCharFormat)
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog

from ui_pykaitai import Ui_PksWindow
import pks_inspector


CHARS_PER_LINE = 8


def hexdump(line):
    hexline = " ".join("%02x" % b for b in line)
    if len(line) < CHARS_PER_LINE:
        hexline += "   " * (CHARS_PER_LINE - len(line))
    return hexline


def to_display_pos(pos):
    line_num = pos // CHARS_PER_LINE
    char_num = pos % CHARS_PER_LINE
    return (line_num * CHARS_PER_LINE * 3) + (char_num * 3)


def get_ks_parser_file_from_ksy_file(ksy_filename):
    meta_seen = False
    with open(ksy_filename) as handle:
        for line in handle:
            line = line.rstrip()
            if line.lstrip()[:5] == "meta:":
                meta_seen = True
                meta_indent = line.index("meta:")
                continue
            if meta_seen:
                if line[:meta_indent] != " " * meta_indent:
                    break
                if line.lstrip()[:3] == "id:":
                    return line.lstrip()[3:].lstrip()

    return None


class PksMain(QMainWindow, Ui_PksWindow):
    def __init__(self):
        super(PksMain, self).__init__()
        self.setupUi(self)
        self.ksy_file = None
        self.ks_parser = None
        self.targetfile = None
        self.base_struct = None
        self._parsed = None
        self._parse_tree = None
        self._cursor = None
        self._ksc_path = "C:/Program Files (x86)/kaitai-struct-compiler/bin/kaitai-struct-compiler.bat"
        self.data_tree.itemSelectionChanged.connect(self._tree_line_selected)
        self.reloadButton.clicked.connect(self._load_data)
        self.ksyFileButton.clicked.connect(self._change_ksy)
        self.targetFileButton.clicked.connect(self._change_targetfile)
        self.reloadButton.setEnabled(False)

    def _set_tree_model(self, parsing, parent=None):
        self.data_tree.clear()
        for field_info in parsing:
            item = QTreeWidgetItem(parent)
            item.setText(0, "%s" % field_info['name'])
            item.setData(0, QtCore.Qt.UserRole,
                         (field_info['offset'], field_info['length']))
            if isinstance(field_info['value'], list):
                self._set_tree_model(field_info['value'], item)
            else:
                child = QTreeWidgetItem(item)
                child.setText(0, repr(field_info['value']))
            if parent is None:
                self.data_tree.addTopLevelItem(item)
            self.data_tree.expandItem(item)

    def _set_ksy_window(self):
        ksy_text = open(self.ksy_file).read()
        self.ksy_editor.setPlainText(ksy_text)

    def _set_data_window(self):
        self.file_display.setReadOnly(True)
        self._data = open(self.targetfile, 'rb').read()
        text = []
        for i in range(0, len(self._data), CHARS_PER_LINE):
            line = self._data[i:i + CHARS_PER_LINE]
            text.append(hexdump(line))
        self.file_display.setPlainText("\n".join(text))
        self._cursor = QTextCursor(self.file_display.document())
        self.file_display.setTextCursor(self._cursor)

    def _clear_data_highlight(self):
        if self._cursor is not None:
            unhighlight = QtGui.QTextCharFormat()
            unhighlight.clearBackground()
            self._cursor.setCharFormat(unhighlight)
            self._cursor = None

    def _tree_line_selected(self):
        if not self.data_tree.selectedItems():
            return
        item = self.data_tree.selectedItems()[0]
        data = item.data(0, QtCore.Qt.UserRole)
        while data is None:
            item = self.data_tree.itemAbove(item)
            if item is None:
                break
            data = item.data(0, QtCore.Qt.UserRole)
        if data is not None:
            start, length = data
            self._clear_data_highlight()
            curs_start = to_display_pos(start)
            curs_end = to_display_pos(start + length) - 1
            if self._cursor is None:
                self._cursor = QTextCursor(self.file_display.document())
                self.file_display.setTextCursor(self._cursor)
            self._cursor.setPosition(curs_start)
            self._cursor.setPosition(curs_end, mode=self._cursor.KeepAnchor)
            highlight = QtGui.QTextCharFormat()
            highlight.setBackground(QtGui.QBrush(QtGui.QColor("red")))
            self._cursor.mergeCharFormat(highlight)

    def _change_ksy(self):
        fname = dialog = QFileDialog.getOpenFileName(
            self, 'Select .ksy file', '', 'KSY Files (*.ksy)')
        if fname is None:
            return
        self.ksy_file = fname
        self.ksy_filename_value_label.setText(fname)
        self._load_data()

    def _change_targetfile(self):
        fname = dialog = QFileDialog.getOpenFileName(
            self, 'Select target file', '', 'All files (*)')
        if fname is None:
            return
        self.targetfile = fname
        self.target_file_label.setText(fname)
        self._load_data()

    def _load_data(self):
        self._clear_data_highlight()
        self.reloadButton.setEnabled(False)
        if self.ksy_file is None:
            return
        self.reloadButton.setEnabled(True)
        base_dir = os.path.dirname(self.ksy_file)
        self.ks_parser = get_ks_parser_file_from_ksy_file(self.ksy_file)
        parser_file_name = base_dir + "/" + self.ks_parser + ".py"
        self.parser_file_name.setText(parser_file_name)
        if self.ks_parser is None:
            self.data_tree.clear()
            self.base_struct = None
            self._parsed = None
            return
        os.chdir(base_dir)
        subprocess.call([self._ksc_path, "-t", "python",
                         self.ksy_file], cwd=base_dir)
        self.base_struct, base_parser_name = pks_inspector.get_base_parser(
            self.ks_parser, parser_file_name)
        if base_parser_name is None:
            self.root_parser_class_label.setText(
                "ERROR - cannot find Python parser for .ksy file")
        else:
            self.root_parser_class_label.setText(base_parser_name)
        if self.targetfile is not None and os.path.exists(self.targetfile) and base_parser_name is not None:
            self._parsed = self.base_struct.from_file(self.targetfile)
            self._parse_tree = pks_inspector.to_tree(self._parsed)
            self._set_tree_model(self._parse_tree)
            self._set_ksy_window()
            self._set_data_window()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName("pykaitai_viewer")
    main_win = PksMain()
    main_win.show()
    app.exec_()


if __name__ == '__main__':
    main()
