from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(404, 412)
        Dialog.setStyleSheet("background-color: #323232;")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 370, 381, 32))
        self.buttonBox.setStyleSheet("background: none;")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(20, 20, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("color: #fff")
        self.titleLabel.setObjectName("titleLabel")
        self.titleEdit = QtWidgets.QLineEdit(Dialog)
        self.titleEdit.setGeometry(QtCore.QRect(70, 20, 321, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleEdit.setFont(font)
        self.titleEdit.setStyleSheet("background: #fff; color: #000;")
        self.titleEdit.setObjectName("titleEdit")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 381, 311))
        self.tableWidget.setStyleSheet("background: #fff; color: #000;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.errorLabel = QtWidgets.QLabel(Dialog)
        self.errorLabel.setGeometry(QtCore.QRect(10, 380, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.errorLabel.setFont(font)
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.titleLabel.setText(_translate("Dialog", "Title: "))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Songs"))
        self.errorLabel.setText(_translate("Dialog", "TextLabel"))
