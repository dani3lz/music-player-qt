from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1051, 655)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setStyleSheet("")
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.titleBarLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleBarLabel.setGeometry(QtCore.QRect(0, 0, 963, 30))
        self.titleBarLabel.setStyleSheet("background: #070707;\n"
                                         "color: #CDCDCD;")
        self.titleBarLabel.setText("")
        self.titleBarLabel.setObjectName("titleBarLabel")

        self.titleBarTitle = QtWidgets.QLabel(self.centralwidget)
        self.titleBarTitle.setGeometry(QtCore.QRect(88, 0, 875, 30))
        self.titleBarTitle.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Impact")
        font.setPointSize(13)
        self.titleBarTitle.setFont(font)
        self.titleBarTitle.setStyleSheet("background: transparent;\n"
                                         "color: #CDCDCD;")
        self.titleBarTitle.setText("Player")
        self.titleBarTitle.setObjectName("titleBarTitle")

        self.titleBarInfoLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleBarInfoLabel.setGeometry(QtCore.QRect(20, 0, 963, 30))
        font = QtGui.QFont("Courier")
        font.setPointSize(13)
        self.titleBarInfoLabel.setFont(font)
        self.titleBarInfoLabel.setStyleSheet("background: transparent;\n"
                                             "color: #CDCDCD;")
        self.titleBarInfoLabel.setText("")
        self.titleBarInfoLabel.setObjectName("titleBarInfoLabel")

        self.closeButton = QtWidgets.QPushButton(MainWindow)
        self.closeButton.setGeometry(QtCore.QRect(1007, 0, 44, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.closeButton.setFont(font)
        self.closeButton.setStyleSheet("QPushButton\n"
                                       "{\n"
                                       "    background: #070707;\n"
                                       "    color: #cdcdcd;\n"
                                       "    border-style: solid;\n"
                                       "    border-width: 1px;\n"
                                       "    border-color: transparent;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton::hover\n"
                                       "{\n"
                                       "    background-color: #E81123;\n"
                                       "    color: #fff;\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QPushButton::pressed\n"
                                       "{\n"
                                       "    background-color: #7D0913;\n"
                                       "    color: #fff;\n"
                                       "}")
        self.closeButton.setObjectName("closeButton")

        self.minimizeButton = QtWidgets.QPushButton(MainWindow)
        self.minimizeButton.setGeometry(QtCore.QRect(963, 0, 44, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.minimizeButton.setFont(font)
        self.minimizeButton.setStyleSheet("QPushButton\n"
                                          "{\n"
                                          "    background: #070707;\n"
                                          "    color: #cdcdcd;\n"
                                          "    border-style: solid;\n"
                                          "    border-width: 1px;\n"
                                          "    border-color: transparent;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton::hover\n"
                                          "{\n"
                                          "    background-color: #0F0F0F;\n"
                                          "    color: #fff;\n"
                                          "}\n"
                                          "\n"
                                          "\n"
                                          "QPushButton::pressed\n"
                                          "{\n"
                                          "    background-color: #4A4A4A;\n"
                                          "    color: #fff;\n"
                                          "}")
        self.minimizeButton.setObjectName("minimizeButton")

        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(270, 49, 501, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("background: none;\n"
                                      "color: white;")
        self.titleLabel.setText("")
        self.titleLabel.setObjectName("titleLabel")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(-10, 30, 1071, 641))
        self.groupBox.setStyleSheet(
            "background: qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(65, 65, 65, 255), stop:1 rgba(0, 0, 0, 255));\n"
            "border: none;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.prevButton = QtWidgets.QPushButton(self.groupBox)
        self.prevButton.setGeometry(QtCore.QRect(175, 60, 31, 31))
        self.prevButton.setStyleSheet("background-color: transparent;\n"
                                      "border-image: url(img/prev.png);\n"
                                      "background: none;\n"
                                      "border: none;\n"
                                      "background-repeat: none;")
        self.prevButton.setText("")
        self.prevButton.setObjectName("prevButton")
        self.durationLabel = QtWidgets.QLabel(self.groupBox)
        self.durationLabel.setGeometry(QtCore.QRect(790, 64, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.durationLabel.setFont(font)
        self.durationLabel.setStyleSheet("color: white;\n"
                                         "background: none;")
        self.durationLabel.setObjectName("durationLabel")
        self.playButton = QtWidgets.QPushButton(self.groupBox)
        self.playButton.setGeometry(QtCore.QRect(85, 40, 71, 71))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.playButton.setFont(font)
        self.playButton.setStyleSheet("background-color: transparent;\n"
                                      "border-image: url(img/play.png);\n"
                                      "background: none;\n"
                                      "border: none;\n"
                                      "background-repeat: none;")
        self.playButton.setText("")
        self.playButton.setObjectName("playButton")
        self.nextButton = QtWidgets.QPushButton(self.groupBox)
        self.nextButton.setGeometry(QtCore.QRect(225, 60, 31, 31))
        self.nextButton.setStyleSheet("background-color: transparent;\n"
                                      "border-image: url(img/next.png);\n"
                                      "background: none;\n"
                                      "border: none;\n"
                                      "background-repeat: none;")
        self.nextButton.setText("")
        self.nextButton.setObjectName("nextButton")
        self.volumeSlider = QtWidgets.QSlider(self.groupBox)
        self.volumeSlider.setGeometry(QtCore.QRect(899, 64, 131, 22))
        self.volumeSlider.setStyleSheet("QSlider{\n"
                                        "    background-color: transparent;\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QSlider::groove:horizontal \n"
                                        "{\n"
                                        "    background-color: transparent;\n"
                                        "    height: 3px;\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QSlider::sub-page:horizontal \n"
                                        "{\n"
                                        "    background-color: qlineargradient(spread:pad, x1:0, y1:0.494, x2:1, y2:0.5, stop:0 rgba(98, 9, 54, 255), stop:1 rgba(33, 13, 68, 255))\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QSlider::add-page:horizontal \n"
                                        "{\n"
                                        "    background-color: rgb(118, 118, 118);\n"
                                        "\n"
                                        "\n"
                                        ";\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QSlider::handle:horizontal \n"
                                        "{\n"
                                        "    background-color: rgb(216, 216, 216);\n"
                                        "    width: 14px;\n"
                                        "    margin: -5px;\n"
                                        "    border-radius: 6px;\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QSlider::handle:horizontal:hover \n"
                                        "{\n"
                                        "    background-color: rgb(240, 240, 240);\n"
                                        "\n"
                                        "}")
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setSingleStep(2)
        self.volumeSlider.setPageStep(10)
        self.volumeSlider.setProperty("value", 50)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.volumeSlider.setObjectName("volumeSlider")
        self.musicSlider = QtWidgets.QSlider(self.groupBox)
        self.musicSlider.setGeometry(QtCore.QRect(280, 60, 501, 31))
        self.musicSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.musicSlider.setStyleSheet("QSlider{\n"
                                       "    background-color: transparent;\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QSlider::groove:horizontal \n"
                                       "{\n"
                                       "    background-color: transparent;\n"
                                       "    height: 3px;\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QSlider::sub-page:horizontal \n"
                                       "{\n"
                                       "    background-color: qlineargradient(spread:pad, x1:0, y1:0.494, x2:1, y2:0.5, stop:0 rgba(98, 9, 54, 255), stop:1 rgba(33, 13, 68, 255))\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "QSlider::add-page:horizontal \n"
                                       "{\n"
                                       "    background-color: rgb(118, 118, 118);\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QSlider::handle:horizontal \n"
                                       "{\n"
                                       "    background-color: transparent;\n"
                                       "    width: 14px;\n"
                                       "    margin: -5px;\n"
                                       "    border-radius: 6px;\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "\n"
                                       "QSlider::handle:horizontal:hover \n"
                                       "{\n"
                                       "    background-color: rgb(240, 240, 240);\n"
                                       "\n"
                                       "}")
        self.musicSlider.setMinimum(0)
        self.musicSlider.setOrientation(QtCore.Qt.Horizontal)
        self.musicSlider.setObjectName("musicSlider")
        self.artistLabel = QtWidgets.QLabel(self.groupBox)
        self.artistLabel.setGeometry(QtCore.QRect(280, 40, 491, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.artistLabel.setFont(font)
        self.artistLabel.setStyleSheet("background: none;\n"
                                       "color: white;")
        self.artistLabel.setText("")
        self.artistLabel.setObjectName("artistLabel")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 1051, 140))
        self.groupBox_2.setStyleSheet("border: none; background: rgb(24, 24 ,24);")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.shuffleButton = QtWidgets.QPushButton(self.groupBox_2)
        self.shuffleButton.setGeometry(QtCore.QRect(10, 40, 30, 20))
        self.shuffleButton.setStyleSheet("background-color: transparent;\n"
                                         "border-image: url(img/shuffle.png);\n"
                                         "background: none;\n"
                                         "border: none;\n"
                                         "background-repeat: none;")
        self.shuffleButton.setText("")
        self.shuffleButton.setObjectName("shuffleButton")
        self.repeatThis = QtWidgets.QPushButton(self.groupBox_2)
        self.repeatThis.setGeometry(QtCore.QRect(10, 90, 30, 20))
        self.repeatThis.setStyleSheet("background-color: transparent;\n"
                                      "border-image: url(img/repeatthis.png);\n"
                                      "background: none;\n"
                                      "border: none;\n"
                                      "background-repeat: none;")
        self.repeatThis.setText("")
        self.repeatThis.setObjectName("repeatThis")
        self.volumeButton = QtWidgets.QPushButton(self.groupBox_2)
        self.volumeButton.setGeometry(QtCore.QRect(860, 66, 20, 18))
        self.volumeButton.setStyleSheet("background-color: transparent;\n"
                                        "border-image: url(img/medium.png);\n"
                                        "background: none;\n"
                                        "border: none;\n"
                                        "background-repeat: none;")
        self.volumeButton.setText("")
        self.volumeButton.setObjectName("volumeButton")

        self.imgLabel = QtWidgets.QLabel(self.groupBox)
        self.imgLabel.setGeometry(QtCore.QRect(60, 220, 150, 150))
        self.imgLabel.setStyleSheet("background: transparent;")
        self.imgLabel.setText("")
        self.imgLabel.setObjectName("imgLabel")

        self.deleteButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteButton.setGeometry(QtCore.QRect(146, 391, 28, 28))
        self.deleteButton.setStyleSheet("background-color: transparent;\n"
                                        "border-image: url(img/delete.png);\n"
                                        "background: none;\n"
                                        "border: none;\n"
                                        "background-repeat: none;")
        self.deleteButton.setObjectName("deleteButton")

        self.dropList = QtWidgets.QComboBox(self.groupBox)
        self.dropList.addItem('All your music')
        self.dropList.setGeometry(QtCore.QRect(28, 460, 187, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.dropList.setFont(font)
        self.dropList.view().window().setWindowFlags(Qt.Popup |
                                                     Qt.FramelessWindowHint |
                                                     Qt.NoDropShadowWindowHint)
        self.dropList.view().window().setAttribute(Qt.WA_TranslucentBackground)
        itemDelegate = QStyledItemDelegate()
        self.dropList.setItemDelegate(itemDelegate)
        self.dropList.setObjectName("dropList")
        self.dropList.setStyleSheet("#dropList {\n"
                                    "background: #181818;\n"
                                    "color: #cdcdcd;\n"
                                    "border: 2px solid #000;\n"
                                    "border-radius: 10px;\n"
                                    "padding-left: 5px;\n"
                                    "}\n"
                                    "#dropList::drop-down {\n"
                                    "border: 0px;\n"
                                    "}\n"
                                    "#dropList::down-arrow {\n"
                                    "image: url(assets/img/arrow_down.png);\n"
                                    "width: 12px;\n"
                                    "height: 12px;\n"
                                    "margin-right: 8px;\n"
                                    "}\n"
                                    "#dropList QAbstractItemView {\n"
                                    "background: #000;\n"
                                    "color: #cdcdcd;\n"
                                    "padding: 2px;\n"
                                    "border-radius: 8px;\n"
                                    "}\n"
                                    "#dropList::disabled {\n"
                                    "background: #A6A6A6;\n"
                                    "color: #D0D0D0;\n"
                                    "border: 2px solid #A6A6A6;\n"
                                    "}")

        self.dropListGear = QtWidgets.QPushButton(self.groupBox)
        self.dropListGear.setGeometry(QtCore.QRect(224, 463, 20, 20))
        self.dropListGear.setStyleSheet("border-image: url(img/gear.png);\n"
                                        "background: none;\n"
                                        "border: none;\n"
                                        "background-repeat: none;"
                                        "::menu-indicator{ image: none; }")
        self.dropListGear.setObjectName("dropListGear")
        self.gearMenu = QtWidgets.QMenu(self.groupBox)
        self.gearMenu.setStyleSheet("QMenu{\n"
                                    "background-color: #181818;\n"
                                    "color: #EAE9E9;}\n"
                                    "QMenu::item{\n"
                                    "}\n"
                                    "QMenu::item:selected{\n"
                                    "background: #252525;}\n"
                                    "QMenu::separator{\n"
                                    "height: 10px;\n"
                                    "margin-left: 10px;\n"
                                    "margin-right: 5px;\n"
                                    "image: none}\n")
        self.dropListGear.setMenu(self.gearMenu)

        self.uploadButton = QtWidgets.QPushButton(self.groupBox)
        self.uploadButton.setGeometry(QtCore.QRect(20, 585, 50, 31))
        self.uploadButton.setStyleSheet("QPushButton\n"
                                        "{\n"
                                        "    background-color: #138039;\n"
                                        "    color: #fff;\n"
                                        "    font-size: 11px;\n"
                                        "    font-weight: bold;\n"
                                        "    border: none;\n"
                                        "    border-radius: 25px;\n"
                                        "    padding: 5px;\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QPushButton::disabled\n"
                                        "{\n"
                                        "    background-color: #5c5c5c;\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "QPushButton::pressed\n"
                                        "{\n"
                                        "    background-color: #1DB954;\n"
                                        "\n"
                                        "}\n"
                                        "")
        self.uploadButton.setObjectName("uploadButton")

        self.edit_btn = QtWidgets.QPushButton(self.groupBox)
        self.edit_btn.setGeometry(QtCore.QRect(98, 390, 28, 28))
        self.edit_btn.setStyleSheet("background-color: transparent;\n"
                                    "border-image: url(img/edit.png);\n"
                                    "background: none;\n"
                                    "border: none;\n"
                                    "background-repeat: none;")
        self.edit_btn.setText("")
        self.edit_btn.setObjectName("edit_btn")

        self.aboutButton = QtWidgets.QPushButton(self.groupBox)
        self.aboutButton.setGeometry(QtCore.QRect(225, 591, 20, 20))
        self.aboutButton.setStyleSheet("background-color: transparent;\n"
                                       "border-image: url(img/about.png);\n"
                                       "background: none;\n"
                                       "border: none;\n"
                                       "background-repeat: none;")
        self.aboutButton.setText("")
        self.aboutButton.setObjectName("aboutButton")

        self.searchBar = QtWidgets.QLineEdit(self.groupBox)
        self.searchBar.setGeometry(QtCore.QRect(35, 160, 200, 25))
        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(10)
        self.searchBar.setFont(font)
        self.searchBar.setStyleSheet(
            "background: #181818; color: #cdcdcd; border: 2px solid #181818; border-radius: 10px; padding-left: 3px; padding-right: 22px;")
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setPlaceholderText("Search")

        self.clear_search = QtWidgets.QPushButton(self.groupBox)
        self.clear_search.setGeometry(QtCore.QRect(216, 167, 12, 12))
        self.clear_search.setStyleSheet("background-color: transparent;\n"
                                        "border-image: url(img/search_clear.png);\n"
                                        "background: none;\n"
                                        "border: none;\n"
                                        "background-repeat: none;")
        self.clear_search.setText("")
        self.clear_search.setObjectName("clear_search")

        self.groupBox_2.raise_()
        self.prevButton.raise_()
        self.durationLabel.raise_()
        self.playButton.raise_()
        self.nextButton.raise_()
        self.volumeSlider.raise_()
        self.musicSlider.raise_()
        self.artistLabel.raise_()
        self.imgLabel.raise_()
        self.titleBarLabel.raise_()
        self.titleBarTitle.raise_()
        self.titleBarInfoLabel.raise_()
        self.uploadButton.raise_()
        self.deleteButton.raise_()
        self.dropList.raise_()
        self.dropListGear.raise_()
        self.closeButton.raise_()
        self.minimizeButton.raise_()
        self.edit_btn.raise_()
        self.searchBar.raise_()
        self.clear_search.raise_()
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(250, 170, 801, 485))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListView\n"
                                      "{\n"
                                      "  background-color: #070202;\n"
                                      "  alternate-background-color: transparent;\n"
                                      "   border : none;\n"
                                      "   color: #fff;\n"
                                      "   show-decoration-selected: 1;\n"
                                      "   outline: 0;\n"
                                      "   border: 0px solid #1d1d1d;\n"
                                      "}\n"
                                      "QListView::disabled\n"
                                      "{\n"
                                      "   background-color: #000;\n"
                                      "   color: #212121;\n"
                                      "   border: none;\n"
                                      "}\n"
                                      "QListView::item\n"
                                      "{\n"
                                      "    background-color: transparent;\n"
                                      "    padding: 4px;\n"
                                      "}\n"
                                      "QListView::item:selected:!active\n"
                                      "{\n"
                                      "  color: #1DB954;\n"
                                      "}\n"
                                      "QListView::item:selected\n"
                                      "{\n"
                                      "  color: #1DB954;\n"
                                      "}\n"
                                      "QListView::item:hover {\n"
                                      "    background-color: transparent;\n"
                                      "   border: none;\n"
                                      "   color: #1DB954;\n"
                                      "\n"
                                      "}")
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setObjectName("listWidget")
        self.groupBox.raise_()
        self.titleLabel.raise_()
        self.listWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.durationLabel.setText(_translate("MainWindow", "0.00 / 0.00"))
        self.uploadButton.setText(_translate("MainWindow", "Upload"))
        self.closeButton.setText(_translate("MainWindow", "✕"))
        self.minimizeButton.setText(_translate("MainWindow", "🗕"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
