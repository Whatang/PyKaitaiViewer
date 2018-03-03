# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\mike_000\workspace\pykaitai\src\pykaitai.ui'
#
# Created: Fri Jan 26 00:10:44 2018
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
        PksWindow.resize(1031, 758)
        self.centralwidget = QtGui.QWidget(PksWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.target_file_label = QtGui.QLabel(self.groupBox)
        self.target_file_label.setText(_fromUtf8(""))
        self.target_file_label.setObjectName(_fromUtf8("target_file_label"))
        self.gridLayout.addWidget(self.target_file_label, 3, 2, 1, 1)
        self.reloadButton = QtGui.QPushButton(self.groupBox)
        self.reloadButton.setObjectName(_fromUtf8("reloadButton"))
        self.gridLayout.addWidget(self.reloadButton, 4, 2, 1, 1)
        self.ksy_filename_value_label = QtGui.QLabel(self.groupBox)
        self.ksy_filename_value_label.setText(_fromUtf8(""))
        self.ksy_filename_value_label.setObjectName(_fromUtf8("ksy_filename_value_label"))
        self.gridLayout.addWidget(self.ksy_filename_value_label, 0, 2, 1, 1)
        self.targetFileButton = QtGui.QPushButton(self.groupBox)
        self.targetFileButton.setObjectName(_fromUtf8("targetFileButton"))
        self.gridLayout.addWidget(self.targetFileButton, 3, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.ksy_filename_label = QtGui.QLabel(self.groupBox)
        self.ksy_filename_label.setObjectName(_fromUtf8("ksy_filename_label"))
        self.gridLayout.addWidget(self.ksy_filename_label, 0, 0, 1, 1)
        self.ksyFileButton = QtGui.QPushButton(self.groupBox)
        self.ksyFileButton.setObjectName(_fromUtf8("ksyFileButton"))
        self.gridLayout.addWidget(self.ksyFileButton, 0, 3, 1, 1)
        self.parser_file_name = QtGui.QLabel(self.groupBox)
        self.parser_file_name.setText(_fromUtf8(""))
        self.parser_file_name.setObjectName(_fromUtf8("parser_file_name"))
        self.gridLayout.addWidget(self.parser_file_name, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.root_parser_class_label = QtGui.QLabel(self.groupBox)
        self.root_parser_class_label.setText(_fromUtf8(""))
        self.root_parser_class_label.setObjectName(_fromUtf8("root_parser_class_label"))
        self.gridLayout.addWidget(self.root_parser_class_label, 2, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.ksy_editor = QtGui.QPlainTextEdit(self.frame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ksy_editor.setFont(font)
        self.ksy_editor.setObjectName(_fromUtf8("ksy_editor"))
        self.horizontalLayout.addWidget(self.ksy_editor)
        self.data_tree = QtGui.QTreeWidget(self.frame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        self.data_tree.setFont(font)
        self.data_tree.setObjectName(_fromUtf8("data_tree"))
        self.data_tree.header().setVisible(False)
        self.horizontalLayout.addWidget(self.data_tree)
        self.file_display = QtGui.QTextBrowser(self.frame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("DejaVu Sans Mono"))
        font.setPointSize(10)
        self.file_display.setFont(font)
        self.file_display.setObjectName(_fromUtf8("file_display"))
        self.horizontalLayout.addWidget(self.file_display)
        self.verticalLayout.addWidget(self.frame)
        PksWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PksWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1031, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PksWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PksWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PksWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PksWindow)
        QtCore.QMetaObject.connectSlotsByName(PksWindow)

    def retranslateUi(self, PksWindow):
        PksWindow.setWindowTitle(_translate("PksWindow", "PyKaitai Viewer", None))
        self.groupBox.setTitle(_translate("PksWindow", "Details", None))
        self.reloadButton.setText(_translate("PksWindow", "Reload", None))
        self.targetFileButton.setText(_translate("PksWindow", "Open", None))
        self.label_2.setText(_translate("PksWindow", "Target File", None))
        self.ksy_filename_label.setText(_translate("PksWindow", ".ksy file", None))
        self.ksyFileButton.setText(_translate("PksWindow", "Open", None))
        self.label.setText(_translate("PksWindow", "Python Parser", None))
        self.label_3.setText(_translate("PksWindow", "Root Parser Class", None))
        self.data_tree.headerItem().setText(0, _translate("PksWindow", "Data", None))

