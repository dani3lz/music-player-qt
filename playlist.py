import json

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from assets.UI.playlistUI import Ui_Dialog


class PlaylistWindow(QMainWindow):
    def __init__(self):
        super(PlaylistWindow, self).__init__()

        # Setup Upload window
        self.songs_for_playlist = []
        self.playlist_name = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Create new playlist")
        self.setWindowIcon(QIcon('linux_player.ico'))
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('assets/img/player.ico'))
        self.ui.buttonBox.accepted.connect(self.save_playlist)
        self.ui.buttonBox.rejected.connect(self.cancel_action)
        self.errorMessage = None

        self.init_table()
        self.cancel = False

    def init_table(self):
        try:
            self.songs_for_playlist.clear()
            self.playlist_name = None
            self.clear_table()
            self.ui.titleEdit.clear()
            self.ui.errorLabel.clear()
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
        except Exception as e:
            print(e)

    def clear_table(self):
        rows = self.ui.tableWidget.rowCount()
        if rows > 0:
            for i in range(rows):
                self.ui.tableWidget.removeRow(0)

    def save_playlist(self):
        if len(self.ui.titleEdit.text()) > 0:
            self.playlist_name = self.ui.titleEdit.text()
            self.songs_for_playlist = []
            for i in range(self.ui.tableWidget.rowCount()):
                if self.ui.tableWidget.item(i, 0).checkState() == Qt.CheckState.Checked:
                    self.songs_for_playlist.append(i)
            if len(self.songs_for_playlist) > 0:
                self.hide()
            else:
                errorMessage = "You must add at least one song."
                self.ui.errorLabel.setText(errorMessage)
        else:
            errorMessage = "Title shouldn't be empty."
            self.ui.errorLabel.setText(errorMessage)

    def closeEvent(self, event):
        self.cancel = True
        self.hide()
        event.accept()

    def cancel_action(self):
        self.cancel = True
        self.hide()