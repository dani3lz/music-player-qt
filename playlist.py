import json

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from assets.UI.playlistUI import Ui_Dialog


class PlaylistWindow(QMainWindow):
    def __init__(self):
        super(PlaylistWindow, self).__init__()

        # Setup Upload window
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Create new playlist")
        self.setWindowIcon(QIcon('linux_player.ico'))
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('assets/img/player.ico'))
        self.ui.tableWidget.removeRow(0)
        self.init_table()
        self.done = False

    def init_table(self):
        try:
            self.clear_table()
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            for i in data["Songs"]:
                if i["playlist"] == "Undefined":
                    song_name = i["title"] + " - " + i["artist"]
                    item = QTableWidgetItem(song_name)
                    item.setCheckState(Qt.Unchecked)
                    current_row = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(current_row)
                    self.ui.tableWidget.setItem(current_row, 0, item)
                    print("Inserted - " + str(current_row))
        except Exception as e:
            print(e)

    def clear_table(self):
        rows = self.ui.tableWidget.rowCount()
        print(rows)
        if rows > 0:
            for i in range(rows):
                self.ui.tableWidget.removeRow(0)
                print("Deleted - " + str(i))
        print(self.ui.tableWidget.rowCount())

    def closeEvent(self, event):
        self.done = True
        self.ui.titleEdit.clear()
        self.init_table()
        event.accept()

