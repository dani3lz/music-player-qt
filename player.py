from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QAction, qApp, QMenu, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtGui import QPixmap, QIcon, QColor, QDesktopServices
from playerUI import Ui_MainWindow
import upload
from args import *
from PyQt5.QtCore import QUrl, QTimer, Qt, QPoint, QDir
import os
import sys
import json
import shutil


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


class PlayerWindow(QMainWindow):
    def __init__(self):
        super(PlayerWindow, self).__init__()

        # Setup main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(name_window)
        self.setWindowIcon(QIcon('player.ico'))

        # Setup elements Nr.1
        self.first = True
        self.login_show = True
        self.volume = 50
        self.titles = []
        self.artists = []
        self.covers = []
        self.shuffle = False
        self.repeatthis = False
        self.repeatonce = False
        self.changeMode = False
        self.mode = "Normal"
        self.now_sec = 0
        self.currentIndex = 0

        # Read file with songs and settings
        self.row = 0
        self.read_songs_from_json()
        self.settings_read()
        self.checkCover()

        # Setup elements Nr.2
        self.isPlaying = False
        self.ui.musicSlider.setPageStep(0)
        self.valueSlider = 0
        self.newIndex = -1
        self.playlist.setPlaybackMode(3)
        self.ui.listWidget.setCurrentRow(0)
        self.ui.imgLabel.setPixmap(QPixmap("img/no_image.jpg").scaled(self.ui.imgLabel.width(), self.ui.imgLabel.width()))

        # Check if exist first song in file
        try:
            self.ui.titleLabel.setText(self.titles[self.row])
            self.ui.artistLabel.setText(self.artists[self.row])
            self.player.playlist().setCurrentIndex(self.row)
            self.ui.listWidget.setCurrentRow(self.row)
            first_song = True
        except Exception as e:
            print(e)
            first_song = False
            self.row = 0

        # Volume and duration label
        self.player.setVolume(self.volume)
        self.ui.durationLabel.setText("0:00 / 0:00")
        self.lastVolume = self.volume

        # Connect buttons
        self.ui.playButton.clicked.connect(self.play)
        self.ui.nextButton.clicked.connect(self.next)
        self.ui.prevButton.clicked.connect(self.prev)
        self.ui.shuffleButton.clicked.connect(self.shuffleMode)
        self.ui.repeatThis.clicked.connect(self.repeatThisMode)
        self.ui.uploadButton.clicked.connect(self.upload_btn)
        self.ui.playButton.setIcon(QIcon("play.png"))
        self.ui.volumeButton.clicked.connect(self.mute)
        self.ui.edit_btn.clicked.connect(self.edit_btn)
        self.ui.deleteButton.clicked.connect(self.delete_btn)
        self.ui.aboutButton.clicked.connect(self.aboutButton)
        self.ui.closeButton.clicked.connect(self.closeButton_clicked)
        self.ui.minimizeButton.clicked.connect(self.minimizeButton_clicked)

        # Music slider bar connect
        self.ui.musicSlider.sliderReleased.connect(self.sliderValue)
        self.ui.listWidget.itemClicked.connect(self.changeSong)

        # Volume slider bar connect
        self.ui.volumeSlider.setValue(self.volume)
        self.ui.volumeSlider.actionTriggered.connect(self.setVolume)

        # Setup timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time_hit)
        self.timer.start(int(1000 / 60))

        # Get text from current item
        try:
            self.text_item = self.ui.listWidget.currentItem().text()
        except Exception as e:
            print(e)

        # Check mode
        self.checkMode()
        if os.path.exists('songs'):
            self.read_files_songs()
            self.checkstylebuttons()
        else:
            self.checkstylebuttons()

        # Set color if exist first song
        if first_song:
            self.text_item = self.ui.listWidget.currentItem().text()
            self.ui.listWidget.currentItem().setText("❯ " + self.text_item)

        self.start = QPoint(0, 0)
        self.pressing = False

        # Tray menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("player.ico"))

        show_action = QAction(QIcon("player.ico"), "Player", self)
        github_action = QAction("Github", self)
        about_action = QAction("About", self)
        exit_action = QAction("Exit", self)
        show_action.triggered.connect(self.open_tray_button)
        github_action.triggered.connect(self.open_github)
        about_action.triggered.connect(self.aboutButton)
        exit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.setStyleSheet(tray_menu_css)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(github_action)
        tray_menu.addAction(about_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.systemIcon)
        self.tray_icon.show()


    # read songs from songs.json
    def read_songs_from_json(self):
        if not os.path.exists('songs'):
            os.makedirs('songs')
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            self.titles.clear()
            self.artists.clear()
            self.covers.clear()
            for i in data["Songs"]:
                # title
                self.titles.append(i["title"])
                # artist
                self.artists.append(i["artist"])
                # cover
                if i["cover"] == "Undefined":
                    self.covers.append("no_image.jpg")
                else:
                    self.covers.append(i["cover"])
        except Exception as e:
            print(e)
        self.read_files_songs()

    # read songs from dir
    def read_files_songs(self):
        try:
            self.ui.listWidget.clear()
            self.playlist = QMediaPlaylist(self.player)

            count = len(os.listdir("songs"))
            for nr in range(count):
                song_name = str(nr) + ".mp3"
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(QDir.currentPath() + "/songs/" + song_name)))
                self.ui.listWidget.addItem(str(nr + 1) + ". " + self.titles[nr] + " - " + self.artists[nr])
        except Exception as e:
            print(e)

        try:
            self.ui.titleLabel.setText(self.titles[self.row])
            self.ui.artistLabel.setText(self.artists[self.row])
            self.player.setPlaylist(self.playlist)
            self.currentIndex = self.row
            self.player.playlist().setCurrentIndex(self.currentIndex)
            self.ui.listWidget.setCurrentRow(self.currentIndex)
            self.text_item = self.ui.listWidget.currentItem().text()

        except Exception as e:
            print(e)
            try:
                self.row = 0
                self.ui.titleLabel.setText(self.titles[self.row])
                self.ui.artistLabel.setText(self.artists[self.row])
                self.player.setPlaylist(self.playlist)
                self.currentIndex = self.row
                self.player.playlist().setCurrentIndex(self.currentIndex)
                self.ui.listWidget.setCurrentRow(self.currentIndex)
                self.text_item = self.ui.listWidget.currentItem().text()
            except Exception as e:
                print(e)

        self.checkCover()

        try:
            self.player.setVolume(self.volume)
        except Exception as e:
            print(e)
            self.player.setVolume(50)

        try:
            if self.mode == "Shuffle":
                self.playlist.setPlaybackMode(4)
            elif self.mode == "Repeat This":
                self.playlist.setPlaybackMode(1)
            elif self.mode == "Repeat Once":
                self.playlist.setPlaybackMode(0)
            else:
                self.mode = "Normal"
                self.playlist.setPlaybackMode(3)
        except Exception as e:
            print(e)
            self.playlist.setPlaybackMode(3)

    # Upload button
    def upload_btn(self):
        self.timer.stop()
        completed = False
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                songs_list = json.load(file)
        except:
            songs_list = {}
            songs_list["Songs"] = []
        window.setEnabled(False)
        if not os.path.exists('songs'):
            os.makedirs('songs')
        nr_of_files = len(os.listdir("songs"))
        try:
            fname = QFileDialog.getOpenFileNames(self, "Open File", "", "MP3 Files (*.mp3)")
            if not len(fname[0]) == 0:
                self.setWindowTitle(name_window + " | Uploading... 0%")
                self.ui.titleBarInfoLabel.setText("Uploading... 0%")
                QApplication.processEvents()
                nr = len(fname[0])
                for i in range(nr):
                    percent = round((i / nr) * 100)
                    self.setWindowTitle(name_window + " | Uploading... " + str(percent) + "%")
                    self.ui.titleBarInfoLabel.setText("Uploading... " + str(percent) + "%")
                    QApplication.processEvents()
                    path = fname[0][i].split("/")
                    file_name_with_ext = path[-1]
                    file_name = file_name_with_ext.rsplit(".", 1)[0]

                    try:
                        if file_name.__contains__("-"):
                            info_song = file_name.split('-', 1)
                        elif file_name.__contains__(" "):
                            info_song = file_name.split(' ', 1)
                        else:
                            info_song = file_name

                        if len(info_song) == 2:
                            song_name = info_song[1].rstrip().strip()
                            artist = info_song[0].strip().rstrip()
                        elif len(info_song) == 1:
                            song_name = info_song[0].rstrip().strip()
                            artist = ""
                        elif len(info_song) > 2:
                            song_name = file_name.rstrip().strip()
                            artist = ""
                        else:
                            song_name = ""
                            artist = ""
                    except Exception as e:
                        print(e)
                        print("info_song")
                        song_name = ""
                        artist = ""

                    upload.start(file_name_with_ext, song_name, artist, nr_of_files, i, nr)
                    while not upload.done:
                        QApplication.processEvents()

                    upload.done = False

                    if str(upload.ui.lineEditName.text()) == "":
                        song_name = "Undefined"
                    else:
                        song_name = str(upload.ui.lineEditName.text())

                    if str(upload.ui.lineEditArtist.text()) == "":
                        artist = "Undefined"
                    else:
                        artist = str(upload.ui.lineEditArtist.text())

                    upload.ui.lineEditName.clear()
                    upload.ui.lineEditArtist.clear()
                    upload.ui.coverLabelInfo.clear()
                    upload.ui.selectedFileInfo.clear()

                    shutil.copy(fname[0][i], "./songs/" + str(nr_of_files) + ".mp3")

                    songs_list["Songs"].append({
                        "id": nr_of_files,
                        "title": song_name,
                        "artist": artist,
                        "cover": upload.file_name_final
                    })

                    nr_of_files += 1
                completed = True
        except Exception as e:
            completed = False
            print(e)
        if completed:
            upload.skip_clicked = False
            songs_list["Songs"].sort(key=lambda x: x["id"])
            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(songs_list, file, indent=4)
            self.read_songs_from_json()
        self.isPlaying = False
        self.setWindowTitle(name_window)
        self.ui.titleBarInfoLabel.setText("")
        self.timer.start()
        window.setEnabled(True)

    # Delete button
    def delete_btn(self):
        id_selected = self.row
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                songs_list = json.load(file)
            open_file = True
        except:
            print("No songs!")
            open_file = False

        if open_file:
            last_id = 0
            songs_list_new = {}
            songs_list_new["Songs"] = []

            for song in songs_list["Songs"]:
                if song["id"] == id_selected:
                    os.remove("./songs/" + str(id_selected) + ".mp3")
                    if not song["cover"] == "Undefined":
                        os.remove("./covers/" + song["cover"])
                else:
                    os.rename("./songs/" + str(song["id"]) + ".mp3", "./songs/" + str(last_id) + ".mp3")
                    if not song["cover"] == "Undefined":
                        cover_name_with_ex = song["cover"]
                        ext = cover_name_with_ex.split(".")[1]
                        cover_new_name = str(last_id) + "." + ext
                        os.rename("./covers/" + song["cover"], "./covers/" + cover_new_name)
                        songs_list_new["Songs"].append({
                            "id": last_id,
                            "title": song["title"],
                            "artist": song["artist"],
                            "cover": cover_new_name
                        })
                    else:
                        songs_list_new["Songs"].append({
                            "id": last_id,
                            "title": song["title"],
                            "artist": song["artist"],
                            "cover": song["cover"]
                        })

                    last_id += 1

            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(songs_list_new, file, indent=4)
            self.isPlaying = False
            self.read_songs_from_json()

    # Edit button
    def edit_btn(self):
        self.timer.stop()
        self.setEnabled(False)
        cancel_edit = False
        id_selected = self.row
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                songs_list = json.load(file)
            open_file = True
        except:
            print("No songs!")
            open_file = False

        if open_file:
            songs_list_new = {}
            songs_list_new["Songs"] = []

            for song in songs_list["Songs"]:
                if song["id"] == id_selected:
                    upload.edit_btn(song["id"], song["title"], song["artist"], song["cover"])
                    while not upload.done:
                        QApplication.processEvents()
                    upload.done = False
                    if upload.cancel_edit:
                        cancel_edit = True
                        upload.cancel_edit = False
                        songs_list_new["Songs"].append({
                            "id": song["id"],
                            "title": song["title"],
                            "artist": song["artist"],
                            "cover": song["cover"]
                        })
                    else:

                        if str(upload.ui.lineEditName.text()) == "":
                            song_name = "Undefined"
                        else:
                            song_name = str(upload.ui.lineEditName.text())

                        if str(upload.ui.lineEditArtist.text()) == "":
                            artist = "Undefined"
                        else:
                            artist = str(upload.ui.lineEditArtist.text())

                        songs_list_new["Songs"].append({
                            "id": song["id"],
                            "title": song_name,
                            "artist": artist,
                            "cover": upload.file_name_final
                        })

                    upload.ui.lineEditName.clear()
                    upload.ui.lineEditArtist.clear()
                    upload.ui.coverLabelInfo.clear()
                    upload.ui.selectedFileInfo.clear()
                    upload.ui.pushButton_Skip.setText("Skip all")
                else:
                    songs_list_new["Songs"].append({
                        "id": song["id"],
                        "title": song["title"],
                        "artist": song["artist"],
                        "cover": song["cover"]
                    })

            if not cancel_edit:
                with open("songs.json", "w", encoding="utf-8") as file:
                    json.dump(songs_list_new, file, indent=4)
                self.isPlaying = False
                self.read_songs_from_json()
                self.timer.start()
                window.setEnabled(True)
            else:
                self.timer.start()
                window.setEnabled(True)

    # Tray menu
    def open_tray_button(self):
        if not self.isVisible():
            self.show()
        else:
            self.activateWindow()

    def open_github(self):
        try:
            url = QUrl("https://github.com/dani3lz/Music_Player")
            QDesktopServices.openUrl(url)
        except Exception as e:
            print(e)

    def systemIcon(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.windowState() == Qt.WindowMinimized:
                self.setWindowState(Qt.WindowNoState)
            else:
                if not self.isVisible():
                    self.show()
                else:
                    self.activateWindow()

    # Check mouse press event
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    # Drag app
    def mouseMoveEvent(self, event):
        if self.pressing and (
                self.ui.titleBarLabel.underMouse() or self.ui.titleBarInfoLabel.underMouse() or self.ui.titleBarTitle.underMouse()):
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                             self.mapToGlobal(self.movement).y(),
                             self.width(),
                             self.height())
            self.start = self.end

    # Minimize App
    def minimizeButton_clicked(self):
        self.showMinimized()

    # Close App
    def closeButton_clicked(self):
        self.hide()

    # Close event in minimized status
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    # Function for About button
    def aboutButton(self):
        try:
            self.show()
            self.msg_about = QMessageBox()
            self.msg_about.setWindowTitle("About")
            self.msg_about.setWindowIcon(QIcon("img/about.ico"))
            self.msg_about.setText(about_text)
            self.msg_about.show()
        except Exception as e:
            print(e)

    # Mute - function for volume
    def mute(self):
        if self.volume > 0:
            self.lastVolume = self.volume
            self.volume = 0
            self.ui.volumeSlider.setValue(0)
            self.player.setVolume(0)
        else:
            if self.lastVolume > 0:
                self.volume = self.lastVolume
                self.ui.volumeSlider.setValue(self.volume)
                self.player.setVolume(self.volume)
            else:
                self.ui.volumeSlider.setValue(75)
                self.player.setVolume(75)

    # Convert duration of song to minutes and seconds
    def convertMillis(self, millis):
        seconds = (millis / 1000) % 60
        minutes = (millis / (1000 * 60)) % 60
        return minutes, seconds

    # Volume slider
    def setVolume(self):
        self.volume = self.ui.volumeSlider.value()
        self.player.setVolume(self.volume)

    # Change music using the list
    def changeSong(self):
        self.row = self.ui.listWidget.currentRow()
        self.player.playlist().setCurrentIndex(self.row)
        if not self.isPlaying:
            self.player.play()
            self.ui.playButton.setStyleSheet(pause_btn_css)
            self.isPlaying = True

    # Music slider
    def sliderValue(self):
        self.player.setPosition(self.ui.musicSlider.value())

    # Read information about player
    def settings_read(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for i in data["Settings"]:
                self.volume = i["Volume"]
                self.lastVolume = self.volume
                self.row = i["Row"]
                self.mode = i["Mode"]
            self.currentIndex = self.row
        except Exception as e:
            print(e)

    # Check player mode
    def checkMode(self):
        if self.mode == "Shuffle":
            self.shuffleMode()
        elif self.mode == "Repeat This":
            self.repeatThisMode()
        elif self.mode == "Repeat Once":
            self.repeatthis = True
            self.repeatThisMode()

    # Write current information about player
    def settings_write(self):
        settings_list = {}
        settings_list["Settings"] = []
        settings_list["Settings"].append({
            "Volume": self.volume,
            "Row": self.row,
            "Mode": self.mode
        })
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings_list, f, indent=4)

    # Timer
    def time_hit(self):
        self.checkStyle()
        self.checkstyleVolume()
        if self.isPlaying:
            self.ui.musicSlider.setMaximum(self.player.duration())
            if not self.ui.musicSlider.isSliderDown():
                self.ui.musicSlider.setValue(self.player.position())
            self.newIndex = self.player.playlist().currentIndex()
            self.checkList()

            song_min, song_sec = self.convertMillis(int(self.player.duration()))
            if song_sec < 10:
                self.song_duration = "{0}:0{1}".format(int(song_min), int(song_sec))
            else:
                self.song_duration = "{0}:{1}".format(int(song_min), int(song_sec))

            now_min, self.now_sec = self.convertMillis(int(self.ui.musicSlider.value()))
            if self.now_sec < 10:
                self.now_duration = "{0}:0{1}".format(int(now_min), int(self.now_sec))
            else:
                self.now_duration = "{0}:{1}".format(int(now_min), int(self.now_sec))

            self.ui.durationLabel.setText(str(self.now_duration) + " / " + str(self.song_duration))

            if self.repeatonce:
                if self.now_duration == self.song_duration:
                    self.isPlaying = False
                    self.ui.playButton.setStyleSheet(play_btn_css)
                    self.player.stop()
        self.settings_write()

    # Check cover image
    def checkCover(self):
        try:
            if self.covers[self.currentIndex] == "no_image.jpg":
                self.imgsrc = QPixmap("img/" + self.covers[self.currentIndex])
            else:
                self.imgsrc = QPixmap("covers/" + self.covers[self.currentIndex])
            self.w = self.ui.imgLabel.width()
            self.h = self.ui.imgLabel.width()
            self.ui.imgLabel.setPixmap(self.imgsrc.scaled(self.w, self.h))
        except Exception as e:
            print(e)

    # Sets the current position in the list
    def checkList(self):
        try:
            if self.currentIndex == self.newIndex:
                pass
            else:
                self.ui.listWidget.item(self.currentIndex).setText(self.text_item)
                self.ui.listWidget.item(self.currentIndex).setForeground(QColor("#fff"))

                self.text_item = self.ui.listWidget.item(self.newIndex).text()
                self.ui.listWidget.item(self.newIndex).setForeground(QColor("#1DB954"))
                self.ui.listWidget.item(self.newIndex).setText("❯ " + self.text_item)

                self.ui.titleLabel.setText(self.titles[self.newIndex])
                self.ui.artistLabel.setText(self.artists[self.newIndex])
                self.ui.listWidget.setCurrentRow(self.player.playlist().currentIndex())
                self.currentIndex = self.newIndex
                self.row = self.newIndex
                self.checkCover()
        except Exception as e:
            print(e)

    # Play button
    def play(self):
        if len(self.titles) > 0:
            if not self.isPlaying:
                self.player.play()
                self.isPlaying = True
                self.newIndex = self.player.playlist().currentIndex()
                self.checkStyle()
            else:
                self.player.pause()
                self.isPlaying = False
                self.checkStyle()

    # Next button
    def next(self):
        if len(self.titles) > 0:
            self.playlist.next()
            self.newIndex = self.player.playlist().currentIndex()
            if not self.isPlaying:
                self.player.play()
                self.isPlaying = True
                self.ui.playButton.setStyleSheet(pause_btn_css)

    # Previous button
    def prev(self):
        if len(self.titles) > 0:
            if int(self.now_sec) < 10:
                self.playlist.previous()
                self.newIndex = self.player.playlist().currentIndex()
            else:
                self.player.setPosition(0)
            if not self.isPlaying:
                self.player.play()
                self.isPlaying = True
                self.ui.playButton.setStyleSheet(pause_btn_css)

    # Repeat This button
    def repeatThisMode(self):
        if not self.repeatthis and not self.repeatonce:
            self.playlist.setPlaybackMode(1)
            self.repeatthis = True
            self.shuffle = False
            self.repeatonce = False
            self.mode = "Repeat This"
            self.checkstylebuttons()
        elif self.repeatthis:
            self.playlist.setPlaybackMode(0)
            self.repeatthis = False
            self.shuffle = False
            self.repeatonce = True
            self.mode = "Repeat Once"
            self.checkstylebuttons()
        else:
            self.playlist.setPlaybackMode(3)
            self.repeatonce = False
            self.mode = "Normal"
            self.checkstylebuttons()

    # Shuffle button
    def shuffleMode(self):
        if not self.shuffle:
            self.playlist.setPlaybackMode(4)
            self.shuffle = True
            self.repeatonce = False
            self.repeatthis = False
            self.mode = "Shuffle"
            self.checkstylebuttons()
        else:
            self.playlist.setPlaybackMode(3)
            self.shuffle = False
            self.mode = "Normal"
            self.checkstylebuttons()

    def checkstylebuttons(self):
        if self.shuffle:
            self.ui.shuffleButton.setStyleSheet(shuffle_on_css)
        else:
            self.ui.shuffleButton.setStyleSheet(shuffle_off_css)

        if self.repeatthis and not self.repeatonce:
            self.ui.repeatThis.setStyleSheet(repeatthis_on_css)
        elif not self.repeatthis and self.repeatonce:
            self.ui.repeatThis.setStyleSheet(repeatonce_off_css)
        else:
            self.ui.repeatThis.setStyleSheet(repeatthis_off_css)

    def checkStyle(self):
        if self.isEnabled():
            if self.ui.deleteButton.underMouse():
                self.ui.deleteButton.setStyleSheet(delete_btn_focus_css)
            else:
                self.ui.deleteButton.setStyleSheet(delete_btn_css)
            if self.ui.edit_btn.underMouse():
                self.ui.edit_btn.setStyleSheet(edit_btn_focus_css)
            else:
                self.ui.edit_btn.setStyleSheet(edit_btn_css)
            if self.ui.aboutButton.underMouse():
                self.ui.aboutButton.setStyleSheet(about_btn_focus_css)
            else:
                self.ui.aboutButton.setStyleSheet(about_btn_css)
            if self.ui.musicSlider.underMouse():
                self.ui.musicSlider.setStyleSheet(musicSlider_focus_css)
            else:
                self.ui.musicSlider.setStyleSheet(musicSlider_css)

            if self.ui.playButton.underMouse():
                if not self.isPlaying:
                    self.ui.playButton.setStyleSheet(play_btn_focus_css)
                else:
                    self.ui.playButton.setStyleSheet(pause_btn_focus_css)
            else:
                if not self.isPlaying:
                    self.ui.playButton.setStyleSheet(play_btn_css)
                else:
                    self.ui.playButton.setStyleSheet(pause_btn_css)

            if self.ui.nextButton.underMouse():
                self.ui.nextButton.setStyleSheet(next_btn_focus_css)
            else:
                self.ui.nextButton.setStyleSheet(next_btn_css)

            if self.ui.prevButton.underMouse():
                self.ui.prevButton.setStyleSheet(prev_btn_focus_css)
            else:
                self.ui.prevButton.setStyleSheet(prev_btn_css)

    def checkstyleVolume(self):
        if self.isEnabled():
            if self.ui.volumeButton.underMouse():
                if self.ui.volumeSlider.value() == 0:
                    self.ui.volumeButton.setStyleSheet(volume_mute_focus_css)
                elif self.ui.volumeSlider.value() > 0 and self.ui.volumeSlider.value() <= 30:
                    self.ui.volumeButton.setStyleSheet(volume_low_focus_css)
                elif self.ui.volumeSlider.value() > 30 and self.ui.volumeSlider.value() <= 70:
                    self.ui.volumeButton.setStyleSheet(volume_medium_focus_css)
                elif self.ui.volumeSlider.value() > 70:
                    self.ui.volumeButton.setStyleSheet(volume_max_focus_css)
            else:
                if self.ui.volumeSlider.value() == 0:
                    self.ui.volumeButton.setStyleSheet(volume_mute_css)
                elif self.ui.volumeSlider.value() > 0 and self.ui.volumeSlider.value() <= 30:
                    self.ui.volumeButton.setStyleSheet(volume_low_css)
                elif self.ui.volumeSlider.value() > 30 and self.ui.volumeSlider.value() <= 70:
                    self.ui.volumeButton.setStyleSheet(volume_medium_css)
                elif self.ui.volumeSlider.value() > 70:
                    self.ui.volumeButton.setStyleSheet(volume_max_css)

if __name__ == "__main__":
    suppress_qt_warnings()
    app = QApplication([])
    name_window = "Player"
    window = PlayerWindow()
    window.show()
    upload = upload.UploadWindow()
    sys.exit(app.exec())
