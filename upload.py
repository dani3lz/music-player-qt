from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
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

        # Var
        self.file_name_final = "Undefined"

        # Connect button
        self.ui.pushButton_2.clicked.connect(self.finish)
        self.ui.pushButton.clicked.connect(self.select_cover)

    def start(self, position, file_name, song_name, artist, nr):
        self.ui.selectedFileInfo.setText(file_name)
        self.ui.textEditName.setText(song_name)
        self.ui.textEdit_2.setText(artist)
        self.file_name_final = "Undefined"
        self.nr = nr
        if position == "final":
            self.ui.pushButton_2.setText("Ok")
        else:
            self.ui.pushButton_2.setText("Next")
        self.show()

    def finish(self):
        self.hide()
        self.done = True


    def select_cover(self):
        final = "Undefined"
        if not os.path.exists('covers'):
            os.makedirs('covers')
        try:
            fname = QFileDialog.getOpenFileName(self, "Open File", "", "JPG (*.jpg);; PNG (*.png)")
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
