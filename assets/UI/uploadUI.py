from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(429, 236)
        Dialog.setStyleSheet("background-color: #323232;")
        self.selectedFileInfo = QtWidgets.QLabel(Dialog)
        self.selectedFileInfo.setGeometry(QtCore.QRect(10, 10, 421, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.selectedFileInfo.setFont(font)
        self.selectedFileInfo.setStyleSheet("color: #fff;")
        self.selectedFileInfo.setObjectName("selectedFileInfo")
        self.nameLabel = QtWidgets.QLabel(Dialog)
        self.nameLabel.setGeometry(QtCore.QRect(30, 50, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("color: #fff;")
        self.nameLabel.setObjectName("nameLabel")
        self.coverLabel = QtWidgets.QLabel(Dialog)
        self.coverLabel.setGeometry(QtCore.QRect(30, 130, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.coverLabel.setFont(font)
        self.coverLabel.setStyleSheet("color: #fff;")
        self.coverLabel.setObjectName("coverLabel")
        self.playlistLabel = QtWidgets.QLabel(Dialog)
        self.playlistLabel.setGeometry(QtCore.QRect(30, 170, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.playlistLabel.setFont(font)
        self.playlistLabel.setStyleSheet("color: #fff;")
        self.playlistLabel.setObjectName("playlistLabel")
        self.lineEditName = QtWidgets.QLineEdit(Dialog)
        self.lineEditName.setGeometry(QtCore.QRect(110, 50, 301, 21))
        self.lineEditName.setStyleSheet(
            "background: none; color: #000; border: 2px solid #fff; border-radius: 10px; padding-left: 3px;")
        self.lineEditName.setText("")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditName.setFont(font)
        self.lineEditName.setObjectName("lineEditName")
        self.pushButton_Cover = QtWidgets.QPushButton(Dialog)
        self.pushButton_Cover.setGeometry(QtCore.QRect(110, 130, 75, 23))
        self.pushButton_Cover.setStyleSheet("background: none;")
        self.pushButton_Cover.setObjectName("pushButton_Cover")
        self.coverLabelInfo = QtWidgets.QLabel(Dialog)
        self.coverLabelInfo.setGeometry(QtCore.QRect(190, 130, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.coverLabelInfo.setFont(font)
        self.coverLabelInfo.setStyleSheet("color: #fff;")
        self.coverLabelInfo.setObjectName("coverLabelInfo")
        self.pushButton_Ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_Ok.setGeometry(QtCore.QRect(340, 200, 75, 23))
        self.pushButton_Ok.setStyleSheet("background: none;")
        self.pushButton_Ok.setObjectName("pushButton_Ok")
        self.pushButton_Skip = QtWidgets.QPushButton(Dialog)
        self.pushButton_Skip.setGeometry(QtCore.QRect(260, 200, 75, 23))
        self.pushButton_Skip.setStyleSheet("background: none;")
        self.pushButton_Skip.setObjectName("pushButton_Skip")
        self.artistLabel = QtWidgets.QLabel(Dialog)
        self.artistLabel.setGeometry(QtCore.QRect(30, 90, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.artistLabel.setFont(font)
        self.artistLabel.setStyleSheet("color: #fff;")
        self.artistLabel.setObjectName("artistLabel")
        self.lineEditArtist = QtWidgets.QLineEdit(Dialog)
        self.lineEditArtist.setGeometry(QtCore.QRect(110, 90, 301, 21))
        self.lineEditArtist.setStyleSheet(
            "background: none; color: #000; border: 2px solid #fff; border-radius: 10px; padding-left: 3px;")
        self.lineEditArtist.setText("")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditArtist.setFont(font)
        self.lineEditArtist.setObjectName("lineEditArtist")
        self.playlistDropList = QtWidgets.QComboBox(Dialog)
        self.playlistDropList.setGeometry(QtCore.QRect(110, 170, 131, 22))
        self.playlistDropList.view().window().setWindowFlags(Qt.Popup |
                                                             Qt.FramelessWindowHint |
                                                             Qt.NoDropShadowWindowHint)
        self.playlistDropList.view().window().setAttribute(Qt.WA_TranslucentBackground)
        itemDelegate = QStyledItemDelegate()
        self.playlistDropList.setItemDelegate(itemDelegate)
        self.playlistDropList.setObjectName("playlistDropList")
        self.playlistDropList.setStyleSheet("#playlistDropList{\n"
                                            "font-family: Arial, Helvetica, sans-serif;\n"
                                            "font: 12px;\n"
                                            "background: #fff;\n"
                                            "color: #000;\n"
                                            "border: 2px solid #fff;\n"
                                            "border-radius: 10px;\n"
                                            "padding-left: 5px;\n"
                                            "}\n"
                                            "#playlistDropList::drop-down {\n"
                                            "border: 0px;\n"
                                            "}\n"
                                            "#playlistDropList::down-arrow {\n"
                                            "image: url(assets/img/arrow_down.png);\n"
                                            "width: 12px;\n"
                                            "height: 12px;\n"
                                            "margin-right: 8px;\n"
                                            "}\n"
                                            "#playlistDropList QAbstractItemView {\n"
                                            "background: #fff;\n"
                                            "padding: 2px;\n"
                                            "border-radius: 8px;\n"
                                            "}\n"
                                            "#playlistDropList::disabled {\n"
                                            "background: #A6A6A6;\n"
                                            "color: #D0D0D0;\n"
                                            "border: 2px solid #A6A6A6;\n"
                                            "}")
        self.playlistDropList.setObjectName("playlistDropList")

        self.checkboxPlaylist = QtWidgets.QCheckBox(Dialog)
        self.checkboxPlaylist.setGeometry(QtCore.QRect(250, 168, 170, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.checkboxPlaylist.setFont(font)
        self.checkboxPlaylist.setStyleSheet("color: #fff;")
        self.checkboxPlaylist.setObjectName("checkboxPlaylist")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.selectedFileInfo.setText(_translate("Dialog", "TextLabel"))
        self.nameLabel.setText(_translate("Dialog", "Title:"))
        self.coverLabel.setText(_translate("Dialog", "Cover:"))
        self.playlistLabel.setText(_translate("Dialog", "Playlist:"))
        self.pushButton_Cover.setText(_translate("Dialog", "Browse"))
        self.coverLabelInfo.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_Ok.setText(_translate("Dialog", "Ok"))
        self.pushButton_Skip.setText(_translate("Dialog", "Skip all"))
        self.artistLabel.setText(_translate("Dialog", "Artist:"))
        self.checkboxPlaylist.setText(_translate("Dialog", "by default for the following"))
