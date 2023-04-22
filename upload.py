import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from assets.UI.uploadUI import Ui_Dialog


class UploadWindow(QMainWindow):
    def __init__(self):
        super(UploadWindow, self).__init__()

        # Setup Upload window
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Upload")
        self.setWindowIcon(QIcon('linux_player.ico'))
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('assets/img/player.ico'))

        # Var
        self.file_name_final = "Undefined"
        self.nr = None
        self.skip_clicked = False
        self.done = False
        self.cancel_edit = False
        self.isClicked = False
        self.mainPlaylistName = "ALL"
        self.selectedPlaylist = self.mainPlaylistName

        # Connect button
        self.ui.pushButton_Ok.clicked.connect(self.finish)
        self.ui.pushButton_Cover.clicked.connect(self.select_cover)
        self.ui.pushButton_Skip.clicked.connect(self.skip_btn)
        self.ui.playlistDropList.activated.connect(self.changed_playlist)
        self.ui.checkboxPlaylist.clicked.connect(self.checkbox_clicked)

    def checkbox_clicked(self):
        try:
            if self.ui.checkboxPlaylist.checkState() == Qt.Checked:
                self.ui.playlistDropList.setDisabled(True)
                self.isClicked = True
                self.selectedPlaylist = self.ui.playlistDropList.currentText()
            else:
                self.ui.playlistDropList.setDisabled(False)
                self.isClicked = False
        except Exception as e:
            print(e)

    def changed_playlist(self):
        self.selectedPlaylist = self.ui.playlistDropList.currentText()

    def edit_btn(self, id_song, title, artist, cover, playlist, all_playlists):
        self.ui.checkboxPlaylist.hide()
        self.ui.checkboxPlaylist.setCheckState(Qt.CheckState.Unchecked)
        self.isClicked = False
        self.ui.playlistDropList.setDisabled(False)
        self.setWindowTitle("Edit")
        self.ui.pushButton_Skip.setText("Cancel")
        self.ui.pushButton_Ok.setText("Ok")
        self.nr = id_song
        file_name = str(id_song) + ".mp3"
        self.ui.selectedFileInfo.setText(file_name)
        self.ui.lineEditName.setText(title)
        self.ui.lineEditArtist.setText(artist)
        self.file_name_final = cover
        if self.file_name_final == "Undefined":
            self.ui.coverLabelInfo.setText("No image.")
        else:
            self.ui.coverLabelInfo.setText(self.file_name_final)
        self.selectedPlaylist = playlist
        for i in all_playlists:
            self.ui.playlistDropList.addItem(i)
        self.ui.playlistDropList.setCurrentText(self.selectedPlaylist)
        self.show()

    def start(self, file_name, song_name, artist, nr_of_files, current_nr, end_nr, all_playlists):
        self.ui.checkboxPlaylist.show()
        if self.skip_clicked:
            self.ui.lineEditName.setText(song_name)
            self.ui.lineEditArtist.setText(artist)
            self.file_name_final = "Undefined"
            if self.isClicked:
                self.ui.playlistDropList.setDisabled(True)
            else:
                self.ui.playlistDropList.setDisabled(False)
                self.selectedPlaylist = self.mainPlaylistName
            self.done = True
        else:
            current_nr += 1
            self.setWindowTitle("Upload " + str(current_nr) + " / " + str(end_nr))
            self.ui.selectedFileInfo.setText(file_name)
            self.ui.lineEditName.setText(song_name)
            self.ui.lineEditArtist.setText(artist)
            self.file_name_final = "Undefined"
            self.ui.coverLabelInfo.setText("No image.")

            for i in all_playlists:
                self.ui.playlistDropList.addItem(i)

            if self.isClicked:
                self.ui.playlistDropList.setDisabled(True)
            else:
                self.ui.playlistDropList.setDisabled(False)
                self.selectedPlaylist = self.mainPlaylistName
            self.ui.playlistDropList.setCurrentText(self.selectedPlaylist)

            self.nr = nr_of_files
            if current_nr == end_nr:
                self.ui.pushButton_Ok.setText("Ok")
            else:
                self.ui.pushButton_Ok.setText("Next")
            self.show()

    def finish(self):
        self.hide()
        self.done = True

    def skip_btn(self):
        if self.windowTitle() == "Edit":
            self.cancel_edit = True
            self.done = True
            self.hide()
        else:
            self.skip_clicked = True
            self.done = True
            self.hide()

    def select_cover(self):
        final = "Undefined"
        if not os.path.exists('covers'):
            os.makedirs('covers')
        try:
            not_selected = True
            fname = QFileDialog.getOpenFileName(self, "Open File", "", "Images (*.png *.xpm *.jpg)")
            if fname:
                not_selected = False
                self.ui.coverLabelInfo.setText(fname[0].split("/")[-1])
                path = fname[0].split("/")
                file_name = path[-1]
                info = file_name.split(".")
                extension = info[-1]
                final = str(self.nr) + "." + str(extension)
                shutil.copy(fname[0], "./covers/" + final)
        except Exception as e:
            not_selected = True
            self.ui.coverLabelInfo.setText("No image.")
            print(e)
        if not not_selected:
            self.file_name_final = final

    def closeEvent(self, event):
        if self.windowTitle() == "Edit":
            self.cancel_edit = True
        self.done = True
        event.accept()
