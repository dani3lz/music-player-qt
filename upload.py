from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from uploadUI import Ui_Form
import os
import sys
import json
import shutil


# UPLOAD WINDOW ---------------------------------------------------------------------------------------------------------
class UploadWindow(QMainWindow):
    def __init__(self):
        super(UploadWindow, self).__init__()

        # Setup Upload window
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Upload")
        self.setWindowIcon(QIcon('linux_player.ico'))
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('player.ico'))

        # Var
        self.file_name_final = "Undefined"
        self.skip_clicked = False
        self.done = False
        self.cancel_edit = False

        # Connect button
        self.ui.pushButton_Ok.clicked.connect(self.finish)
        self.ui.pushButton_Cover.clicked.connect(self.select_cover)
        self.ui.pushButton_Skip.clicked.connect(self.skip_btn)

    def edit_btn(self, id_song, title, artist, cover):
        self.setWindowTitle("Edit")
        self.ui.pushButton_Skip.setText("Cancel")
        self.ui.pushButton_Ok.setText("Ok")
        self.nr = id_song
        file_name = str(id_song) + ".mp3"
        self.ui.selectedFileInfo.setText(file_name)
        self.ui.lineEditName.setText(title)
        self.ui.lineEditArtist.setText(artist)
        self.ui.coverLabelInfo.setText(cover)
        self.show()


    def start(self, file_name, song_name, artist, nr_of_files, current_nr, end_nr):
        if self.skip_clicked:
            self.ui.lineEditName.setText(song_name)
            self.ui.lineEditArtist.setText(artist)
            self.file_name_final = "Undefined"
            self.done = True
        else:
            current_nr += 1
            self.setWindowTitle("Upload " + str(current_nr) + " / " + str(end_nr))
            self.ui.selectedFileInfo.setText(file_name)
            self.ui.lineEditName.setText(song_name)
            self.ui.lineEditArtist.setText(artist)
            self.file_name_final = "Undefined"
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
            fname = QFileDialog.getOpenFileName(self, "Open File", "", "Images (*.png *.xpm *.jpg)")
            if fname:
                self.ui.coverLabelInfo.setText(fname[0])
                path = fname[0].split("/")
                file_name = path[-1]
                info = file_name.split(".")
                extension = info[-1]
                final = str(self.nr) + "." + str(extension)
                shutil.copy(fname[0], "./covers/" + final)
        except Exception as e:
            print(e)
        self.file_name_final = final

    def closeEvent(self, event):
        if self.windowTitle() == "Edit":
            self.cancel_edit = True
        self.done = True
        event.accept()
