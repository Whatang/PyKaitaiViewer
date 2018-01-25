# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mike_000\workspace\pykaitai\src\pykaitai.ui'
#
# Created: Thu Jan 25 22:44:37 2018
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PksWindow(object):
    def setupUi(self, PksWindow):
        PksWindow.setObjectName(_fromUtf8("PksWindow"))
        PksWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(PksWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ksy_editor = QtGui.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ksy_editor.setFont(font)
        self.ksy_editor.setObjectName(_fromUtf8("ksy_editor"))
        self.horizontalLayout.addWidget(self.ksy_editor)
        self.data_tree = QtGui.QTreeWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        self.data_tree.setFont(font)
        self.data_tree.setObjectName(_fromUtf8("data_tree"))
        self.data_tree.header().setVisible(False)
        self.horizontalLayout.addWidget(self.data_tree)
        self.file_display = QtGui.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        self.file_display.setFont(font)
        self.file_display.setObjectName(_fromUtf8("file_display"))
        self.horizontalLayout.addWidget(self.file_display)
        PksWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PksWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PksWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PksWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PksWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PksWindow)
        QtCore.QMetaObject.connectSlotsByName(PksWindow)

    def retranslateUi(self, PksWindow):
        PksWindow.setWindowTitle(_translate("PksWindow", "PyKaitai Viewer", None))
        self.data_tree.headerItem().setText(0, _translate("PksWindow", "Data", None))

