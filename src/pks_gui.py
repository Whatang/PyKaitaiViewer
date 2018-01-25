'''
Created on 25 Jan 2018

@author: Mike Thomas
'''
import importlib
import pprint
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import (QAbstractItemView, QStandardItemModel, QTreeWidgetItem,
                      QTextCursor, QTextCharFormat)
from PyQt4.QtGui import QApplication, QMainWindow

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


class PksMain(QMainWindow, Ui_PksWindow):
    def __init__(self):
        super(PksMain, self).__init__()
        self.setupUi(self)
        self.ksy_file = "../typeparser.ksy"
        self.ks_parser = "type_parser"
        self.targetfile = "testfile"
        self.base_struct = pks_inspector.get_base_parser(self.ks_parser)
        self._parsed = self.base_struct.from_file(self.targetfile)
        self._parse_tree = pks_inspector.to_tree(self._parsed)
        self._cursor = None
        self._set_tree_model(self._parse_tree)
        self.data_tree.itemSelectionChanged.connect(self._tree_line_selected)
        self._set_ksy_window()
        self._set_data_window()

    def _set_tree_model(self, parsing, parent=None):
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

    def _tree_line_selected(self):
        item = self.data_tree.selectedItems()[0]
        data = item.data(0, QtCore.Qt.UserRole)
        while data is None:
            item = self.data_tree.itemAbove(item)
            if item is None:
                break
            data = item.data(0, QtCore.Qt.UserRole)
        if data is not None:
            start, length = data
            if self._cursor is not None:
                unhighlight = QtGui.QTextCharFormat()
                unhighlight.clearBackground()
                self._cursor.setCharFormat(unhighlight)
            curs_start = to_display_pos(start)
            curs_end = to_display_pos(start + length) - 1
            self._cursor.setPosition(curs_start)
            self._cursor.setPosition(curs_end, mode=self._cursor.KeepAnchor)
            highlight = QtGui.QTextCharFormat()
            highlight.setBackground(QtGui.QBrush(QtGui.QColor("red")))
            self._cursor.mergeCharFormat(highlight)


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
