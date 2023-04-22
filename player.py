from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QAction, qApp, QMenu, QFileDialog, \
    QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtGui import QPixmap, QIcon, QColor, QDesktopServices

import playlist
from assets.UI.playerUI import Ui_MainWindow
import upload
from assets.args import *
from PyQt5.QtCore import QUrl, QTimer, Qt, QPoint, QDir
from PyQt5.QtWinExtras import QWinThumbnailToolBar, QWinThumbnailToolButton
import os
import sys
import json
import shutil
from mutagen.id3 import ID3


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


def open_github():
    try:
        url = QUrl("https://github.com/dani3lz/Music_Player")
        QDesktopServices.openUrl(url)
    except Exception as e:
        print(e)


class PlayerWindow(QMainWindow):
    def __init__(self):
        super(PlayerWindow, self).__init__()

        # Setup main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle(name_window)
        self.setWindowIcon(QIcon('assets/img/player.ico'))

        # Setup elements Nr.1
        self.first = True
        self.login_show = True
        self.volume = 50
        self.titles = []
        self.artists = []
        self.covers = []
        self.shuffle = False
        self.repeat_this = False
        self.repeatonce = False
        self.changeMode = False
        self.mode = "Normal"
        self.now_sec = 0
        self.currentIndex = 0

        # Read file with songs and settings
        self.row = 0
        self.songs_id_from_playlist = []
        self.mainPlaylistName = "ALL"
        self.currentPlaylist = self.mainPlaylistName
        self.read_songs_from_json()
        self.settings_read()
        self.check_cover()

        # Setup elements Nr.2
        self.isPlaying = False
        self.ui.musicSlider.setPageStep(0)
        self.valueSlider = 0
        self.newIndex = -1
        self.playlist.setPlaybackMode(3)
        self.ui.listWidget.setCurrentRow(0)
        self.ui.imgLabel.setPixmap(
            QPixmap("assets/img/no_image.jpg").scaled(self.ui.imgLabel.width(), self.ui.imgLabel.width()))

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
        self.ui.shuffleButton.clicked.connect(self.shuffle_btn)
        self.ui.repeatThis.clicked.connect(self.repeat_this_btn)
        self.ui.uploadButton.clicked.connect(self.upload_btn)
        self.ui.playButton.setIcon(QIcon("play.png"))
        self.ui.volumeButton.clicked.connect(self.mute)
        self.ui.edit_btn.clicked.connect(self.edit_btn)
        self.ui.deleteButton.clicked.connect(self.delete_btn)
        self.ui.aboutButton.clicked.connect(self.about_button)
        self.ui.closeButton.clicked.connect(self.closeButton_clicked)
        self.ui.minimizeButton.clicked.connect(self.minimizeButton_clicked)

        # Music slider bar connect
        self.ui.musicSlider.sliderReleased.connect(self.slider_value)
        self.ui.listWidget.itemClicked.connect(self.change_song)

        # Volume slider bar connect
        self.ui.volumeSlider.setMaximum(100)
        self.ui.volumeSlider.setMinimum(0)
        self.ui.volumeSlider.setValue(self.volume)
        self.ui.volumeSlider.valueChanged.connect(self.set_volume)

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
        self.check_mode()
        if os.path.exists('songs'):
            self.read_files_songs()
            self.check_style_mode()
        else:
            self.check_style_mode()

        # Set color if exist first song
        if first_song:
            self.text_item = self.ui.listWidget.currentItem().text()
            self.ui.listWidget.currentItem().setText("❯ " + self.text_item)

        self.start = QPoint(0, 0)
        self.pressing = False

        # Tray menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/img/player.ico"))

        show_action = QAction(QIcon("assets/img/player.ico"), "Player", self)
        github_action = QAction("Github", self)
        about_action = QAction("About", self)
        exit_action = QAction("Exit", self)
        show_action.triggered.connect(self.open_tray_button)
        github_action.triggered.connect(open_github)
        about_action.triggered.connect(self.about_button)
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
        self.tray_icon.activated.connect(self.system_icon)
        self.tray_icon.show()

        # Toolbar
        self.toolBar = QWinThumbnailToolBar(self)

        self.toolBtnPrev = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnPrev.setToolTip('Prev')
        self.toolBtnPrev.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.toolBtnPrev.clicked.connect(self.prev)
        self.toolBar.addButton(self.toolBtnPrev)

        self.toolBtnControl = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnControl.setToolTip('Play')
        self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.toolBtnControl.clicked.connect(self.play)
        self.toolBar.addButton(self.toolBtnControl)

        self.toolBtnNext = QWinThumbnailToolButton(self.toolBar)
        self.toolBtnNext.setToolTip('Next')
        self.toolBtnNext.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.toolBtnNext.clicked.connect(self.next)
        self.toolBar.addButton(self.toolBtnNext)

        # Playlist
        self.create_playlist_action = QAction("Create new playlist", self)
        self.delete_playlist_action = QAction("Delete current playlist", self)
        self.create_playlist_action.triggered.connect(self.create_playlist)
        self.delete_playlist_action.triggered.connect(self.delete_playlist)
        self.ui.gearMenu.addAction(self.create_playlist_action)
        self.ui.dropList.activated.connect(self.change_playlist)
        self.check_playlists()
        self.change_playlist()

    # delete current playlist
    def delete_playlist(self):
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            for i in data["Songs"]:
                if i["playlist"] == self.currentPlaylist:
                    i["playlist"] = "Undefined"
            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            self.currentPlaylist = self.mainPlaylistName
            self.check_playlists()
            self.change_playlist()
        except Exception as e:
            print(e)

    # add playlists to drop list
    def check_playlists(self):
        try:
            name_of_playlists = [self.mainPlaylistName]
            self.ui.dropList.clear()
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            for i in data["Songs"]:
                if i["playlist"] != "Undefined":
                    playlist_name = i["playlist"]
                    exists = False
                    for j in name_of_playlists:
                        if playlist_name == j:
                            exists = True
                            break
                    if not exists:
                        name_of_playlists.append(playlist_name)
            for i in name_of_playlists:
                self.ui.dropList.addItem(i)

            self.ui.dropList.setCurrentText(self.currentPlaylist)
        except Exception as e:
            print(e)

    # create new playlist
    def create_playlist(self):
        self.app_setEnabled(False)
        playlist_window.init_table()
        playlist_window.show()
        while not playlist_window.isHidden():
            QApplication.processEvents()

        if not playlist_window.cancel:
            playlist_name = playlist_window.playlist_name
            songs_for_playlist = playlist_window.songs_for_playlist.copy()
            self.insert_songs_into_playlist(playlist_name, songs_for_playlist)
            self.check_playlists()
        else:
            playlist_window.cancel = False
        self.app_setEnabled(True)

    # change value 'playlist' in songs.json
    def insert_songs_into_playlist(self, playlist_name, list):
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            j = 0
            for i in data["Songs"]:
                if i["playlist"] == "Undefined":
                    for k in list:
                        if k == j:
                            i["playlist"] = playlist_name
                            list.remove(k)
                            break
                    j += 1
            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(e)

    # change list of songs
    def change_playlist(self):
        self.isPlaying = False
        self.row = 0
        self.currentPlaylist = self.ui.dropList.currentText()
        self.ui.gearMenu.clear()
        if self.currentPlaylist == self.mainPlaylistName:
            self.ui.gearMenu.addAction(self.create_playlist_action)
        else:
            self.ui.gearMenu.addActions([self.create_playlist_action, self.delete_playlist_action])
        self.read_songs_from_json()

    # change middle button for toolbar nav
    def check_toolbar_button(self):
        if self.isPlaying:
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.toolBtnControl.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # toggle availability of window
    def app_setEnabled(self, b):
        window.setEnabled(b)
        self.toolBtnControl.blockSignals(not b)
        self.toolBtnNext.blockSignals(not b)
        self.toolBtnPrev.blockSignals(not b)

    # show nav buttons in toolbar
    def showEvent(self, event):
        super(PlayerWindow, self).showEvent(event)
        if not self.toolBar.window():
            self.toolBar.setWindow(self.windowHandle())

    # read songs from songs.json
    def read_songs_from_json(self):
        if not os.path.exists('songs'):
            os.makedirs('songs')
        if not os.path.exists("songs.json"):
            songs_list = {"Songs": []}
            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(songs_list, file, indent=4)
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        try:
            with open("songs.json", "r", encoding="utf-8") as file:
                data = json.load(file)
            self.titles.clear()
            self.artists.clear()
            self.covers.clear()
            self.songs_id_from_playlist.clear()
            if self.currentPlaylist == self.mainPlaylistName:
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
                    self.songs_id_from_playlist.append(i["id"])
            else:
                for i in data["Songs"]:
                    if i["playlist"] == self.currentPlaylist:
                        # title
                        self.titles.append(i["title"])
                        # artist
                        self.artists.append(i["artist"])
                        # cover
                        if i["cover"] == "Undefined":
                            self.covers.append("no_image.jpg")
                        else:
                            self.covers.append(i["cover"])
                        self.songs_id_from_playlist.append(i["id"])
        except Exception as e:
            print(e)
        self.read_files_songs()

    # read songs from dir
    def read_files_songs(self):
        try:
            self.ui.listWidget.clear()
            self.playlist = QMediaPlaylist(self.player)

            if self.currentPlaylist == self.mainPlaylistName:
                count = len(os.listdir("songs"))
                for nr in range(count):
                    song_name = str(nr) + ".mp3"
                    self.playlist.addMedia(
                        QMediaContent(QUrl.fromLocalFile(QDir.currentPath() + "/songs/" + song_name)))
                    self.ui.listWidget.addItem(str(nr + 1) + ". " + self.titles[nr] + " - " + self.artists[nr])
            else:
                i = 0
                for nr in self.songs_id_from_playlist:
                    song_name = str(nr) + ".mp3"
                    self.playlist.addMedia(
                        QMediaContent(QUrl.fromLocalFile(QDir.currentPath() + "/songs/" + song_name)))
                    self.ui.listWidget.addItem(str(i + 1) + ". " + self.titles[i] + " - " + self.artists[i])
                    i += 1
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

        self.check_cover()

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
            songs_list = {"Songs": []}
        self.app_setEnabled(False)
        if not os.path.exists('songs'):
            os.makedirs('songs')
        nr_of_files = len(os.listdir("songs"))
        try:
            fname = QFileDialog.getOpenFileNames(self, "Open File", "", "MP3 Files (*.mp3)")
            not_selected = True
            if not len(fname[0]) == 0:
                not_selected = False
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
                        try:
                            song_info = ID3(fname[0][i])
                            song_name = song_info['TIT2'].text[0]
                            artist = song_info['TPE1'].text[0]
                        except Exception as e:
                            print(e)
                            print("ID3 Problem")
                            song_name = file_name
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
                        song_name = "None"
                    else:
                        song_name = str(upload.ui.lineEditName.text())

                    if str(upload.ui.lineEditArtist.text()) == "":
                        artist = "None"
                    else:
                        artist = str(upload.ui.lineEditArtist.text())

                    upload.ui.lineEditName.clear()
                    upload.ui.lineEditArtist.clear()
                    upload.ui.coverLabelInfo.clear()
                    upload.ui.selectedFileInfo.clear()

                    path_copy = "./songs/" + str(nr_of_files) + ".mp3"
                    shutil.copy(fname[0][i], path_copy)

                    try:
                        song_info = ID3(path_copy)
                        song_info.delete()
                    except Exception as e:
                        print(e)
                        print("Deleting ID3 from dir songs")

                    songs_list["Songs"].append({
                        "id": nr_of_files,
                        "title": song_name,
                        "artist": artist,
                        "cover": upload.file_name_final,
                        "playlist": "Undefined"
                    })

                    nr_of_files += 1
                completed = True
        except Exception as e:
            completed = False
            not_selected = True
            print(e)
        if completed:
            upload.skip_clicked = False
            songs_list["Songs"].sort(key=lambda x: x["id"])
            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(songs_list, file, indent=4)
            self.read_songs_from_json()
        if not not_selected:
            self.isPlaying = False
            self.setWindowTitle(name_window)
            self.ui.titleBarInfoLabel.setText("")
        self.timer.start()
        self.app_setEnabled(True)

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
            songs_list_new = {"Songs": []}

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
                            "cover": cover_new_name,
                            "playlist": "Undefined"
                        })
                    else:
                        songs_list_new["Songs"].append({
                            "id": last_id,
                            "title": song["title"],
                            "artist": song["artist"],
                            "cover": song["cover"],
                            "playlist": "Undefined"
                        })

                    last_id += 1

            with open("songs.json", "w", encoding="utf-8") as file:
                json.dump(songs_list_new, file, indent=4)
            self.isPlaying = False
            self.read_songs_from_json()

    # Edit button
    def edit_btn(self):
        self.timer.stop()
        self.app_setEnabled(False)
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
            songs_list_new = {"Songs": []}

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
                            "cover": song["cover"],
                            "playlist": "Undefined"
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
                            "cover": upload.file_name_final,
                            "playlist": "Undefined"
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
                        "cover": song["cover"],
                        "playlist": "Undefined"
                    })

            if not cancel_edit:
                with open("songs.json", "w", encoding="utf-8") as file:
                    json.dump(songs_list_new, file, indent=4)
                self.isPlaying = False
                self.read_songs_from_json()
            self.timer.start()
            self.app_setEnabled(True)

    # Tray menu
    def open_tray_button(self):
        if not self.isVisible():
            self.show()
        else:
            self.activateWindow()

    def system_icon(self, reason):
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
    def about_button(self):
        try:
            self.show()
            self.msg_about = QMessageBox()
            self.msg_about.setWindowTitle("About")
            self.msg_about.setWindowIcon(QIcon("assets/img/about.ico"))
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
                self.ui.volumeSlider.setValue(50)
                self.player.setVolume(50)

    # Convert duration of song to minutes and seconds
    def convert_millis_to_seconds(self, millis):
        seconds = (millis / 1000) % 60
        minutes = (millis / (1000 * 60)) % 60
        return minutes, seconds

    # Volume slider
    def set_volume(self):
        self.volume = self.ui.volumeSlider.value()
        self.player.setVolume(self.volume)

    # Change music using the list
    def change_song(self):
        self.row = self.ui.listWidget.currentRow()
        self.player.playlist().setCurrentIndex(self.row)
        if not self.isPlaying:
            self.player.play()
            self.ui.playButton.setStyleSheet(pause_btn_css)
            self.isPlaying = True

    # Music slider
    def slider_value(self):
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
                self.currentPlaylist = i["Playlist"]
            self.currentIndex = self.row
        except Exception as e:
            print(e)

    # Check player mode
    def check_mode(self):
        if self.mode == "Shuffle":
            self.shuffle_btn()
        elif self.mode == "Repeat This":
            self.repeat_this_btn()
        elif self.mode == "Repeat Once":
            self.repeat_this = True
            self.repeat_this_btn()

    # Write current information about player
    def settings_write(self):
        settings_list = {"Settings": []}
        settings_list["Settings"].append({
            "Volume": self.volume,
            "Row": self.row,
            "Mode": self.mode,
            "Playlist": self.currentPlaylist
        })
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings_list, f, indent=4)

    def update_duration_of_music(self):
        song_min, song_sec = self.convert_millis_to_seconds(int(self.player.duration()))
        if song_sec < 10:
            self.song_duration = "{0}:0{1}".format(int(song_min), int(song_sec))
        else:
            self.song_duration = "{0}:{1}".format(int(song_min), int(song_sec))

        now_min, self.now_sec = self.convert_millis_to_seconds(int(self.ui.musicSlider.value()))
        if self.now_sec < 10:
            self.now_duration = "{0}:0{1}".format(int(now_min), int(self.now_sec))
        else:
            self.now_duration = "{0}:{1}".format(int(now_min), int(self.now_sec))

        self.ui.durationLabel.setText(str(self.now_duration) + " / " + str(self.song_duration))

    def check_repeat_once(self):
        if self.repeatonce:
            if self.now_duration == self.song_duration:
                self.isPlaying = False
                self.ui.playButton.setStyleSheet(play_btn_css)
                self.player.stop()

    # Timer
    def time_hit(self):
        self.check_style_buttons()
        self.check_style_volume()
        self.check_toolbar_button()
        if self.isPlaying:
            self.ui.musicSlider.setMaximum(self.player.duration())
            if not self.ui.musicSlider.isSliderDown():
                self.ui.musicSlider.setValue(self.player.position())
            self.newIndex = self.player.playlist().currentIndex()
            self.check_list()
            self.update_duration_of_music()
            self.check_repeat_once()
        self.settings_write()

    # Check cover image
    def check_cover(self):
        try:
            if self.covers[self.currentIndex] == "no_image.jpg":
                self.imgsrc = QPixmap("assets/img/" + self.covers[self.currentIndex])
            else:
                self.imgsrc = QPixmap("covers/" + self.covers[self.currentIndex])
            self.w = self.ui.imgLabel.width()
            self.h = self.ui.imgLabel.width()
            self.ui.imgLabel.setPixmap(self.imgsrc.scaled(self.w, self.h))
        except Exception as e:
            print(e)

    # Sets the current position in the list
    def check_list(self):
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
                self.check_cover()
        except Exception as e:
            print(e)

    # Play button
    def play(self):
        if len(self.titles) > 0:
            if not self.isPlaying:
                self.player.play()
                self.isPlaying = True
                self.toolBtnControl.setToolTip('Pause')
                self.newIndex = self.player.playlist().currentIndex()
                self.check_style_buttons()
            else:
                self.player.pause()
                self.isPlaying = False
                self.toolBtnControl.setToolTip('Play')
                self.check_style_buttons()

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
            if int(self.now_sec) < 5:
                self.playlist.previous()
                self.newIndex = self.player.playlist().currentIndex()
            else:
                self.player.setPosition(0)
            if not self.isPlaying:
                self.player.play()
                self.isPlaying = True
                self.ui.playButton.setStyleSheet(pause_btn_css)

    # Repeat This button
    def repeat_this_btn(self):
        if not self.repeat_this and not self.repeatonce:
            self.playlist.setPlaybackMode(1)
            self.repeat_this = True
            self.shuffle = False
            self.repeatonce = False
            self.mode = "Repeat This"
            self.check_style_mode()
        elif self.repeat_this:
            self.playlist.setPlaybackMode(0)
            self.repeat_this = False
            self.shuffle = False
            self.repeatonce = True
            self.mode = "Repeat Once"
            self.check_style_mode()
        else:
            self.playlist.setPlaybackMode(3)
            self.repeatonce = False
            self.mode = "Normal"
            self.check_style_mode()

    # Shuffle button
    def shuffle_btn(self):
        if not self.shuffle:
            self.playlist.setPlaybackMode(4)
            self.shuffle = True
            self.repeatonce = False
            self.repeat_this = False
            self.mode = "Shuffle"
            self.check_style_mode()
        else:
            self.playlist.setPlaybackMode(3)
            self.shuffle = False
            self.mode = "Normal"
            self.check_style_mode()

    def check_style_mode(self):
        if self.shuffle:
            self.ui.shuffleButton.setStyleSheet(shuffle_on_css)
        else:
            self.ui.shuffleButton.setStyleSheet(shuffle_off_css)

        if self.repeat_this and not self.repeatonce:
            self.ui.repeatThis.setStyleSheet(repeatthis_on_css)
        elif not self.repeat_this and self.repeatonce:
            self.ui.repeatThis.setStyleSheet(repeatonce_off_css)
        else:
            self.ui.repeatThis.setStyleSheet(repeatthis_off_css)

    def check_style_buttons(self):
        if self.isEnabled():
            if self.ui.dropListGear.underMouse():
                self.ui.dropListGear.setStyleSheet(gear_focus_css)
            else:
                self.ui.dropListGear.setStyleSheet(gear_css)
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

    def check_style_volume(self):
        if self.isEnabled():
            if self.ui.volumeButton.underMouse():
                if self.ui.volumeSlider.value() == 0:
                    self.ui.volumeButton.setStyleSheet(volume_mute_focus_css)
                elif 0 < self.ui.volumeSlider.value() <= 30:
                    self.ui.volumeButton.setStyleSheet(volume_low_focus_css)
                elif 30 < self.ui.volumeSlider.value() <= 70:
                    self.ui.volumeButton.setStyleSheet(volume_medium_focus_css)
                elif self.ui.volumeSlider.value() > 70:
                    self.ui.volumeButton.setStyleSheet(volume_max_focus_css)
            else:
                if self.ui.volumeSlider.value() == 0:
                    self.ui.volumeButton.setStyleSheet(volume_mute_css)
                elif 0 < self.ui.volumeSlider.value() <= 30:
                    self.ui.volumeButton.setStyleSheet(volume_low_css)
                elif 30 < self.ui.volumeSlider.value() <= 70:
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
    playlist_window = playlist.PlaylistWindow()
    sys.exit(app.exec())
