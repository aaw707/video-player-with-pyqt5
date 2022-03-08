# import needed modules
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
 QStyle, QSlider, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys

# please install this decoder in order to play videos other than .avi
'''https://www.codecguide.com/download_k-lite_codec_pack_basic.htm'''

# number of seconds for forward/backward button
global SECONDS
SECONDS = 3

# create Window class
class Window(QWidget):

    # constructor
    def __init__(self):
        super().__init__()

        # set icon
        self.setWindowIcon(QIcon("player.ico"))
        # set title
        self.setWindowTitle("Video Player - Angel Wang")
        # set size
        self.setGeometry(350, 100, 700, 500)

        # set background color
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.create_player()

    # create player
    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()

        # button to open the file
        self.openBtn = QPushButton('Open Video')
        # open file when clicked
        self.openBtn.clicked.connect(self.open_file)

        # button to play video
        self.playBtn = QPushButton()
        # not enabled initially
        self.playBtn.setEnabled(False)
        # update the icon as play state changes
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # play the video when button clicked
        self.playBtn.clicked.connect(self.play_video)

        # create a slider to set play progress
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        # set function
        self.slider.sliderMoved.connect(self.set_position)

        # button to forward video
        self.forwardBtn = QPushButton()
        # icon
        self.forwardBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        # function
        self.forwardBtn.clicked.connect(self.forward)

        # button to backward video
        self.backwardBtn = QPushButton()
        # icon
        self.backwardBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        # function
        self.backwardBtn.clicked.connect(self.backward)

        # set the horizontal layout of the window
        hbox = QHBoxLayout()
        # margins
        hbox.setContentsMargins(0, 0, 0, 0)

        # add the buttons and slider to the window
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.backwardBtn)
        hbox.addWidget(self.forwardBtn)
        hbox.addWidget(self.slider)

        # set the vertical layout of the window
        vbox = QVBoxLayout()
        # add the video playing field
        vbox.addWidget(videowidget)
        # add vertical layout on top of the horizontal layout
        vbox.addLayout(hbox)

        # set video output
        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(vbox)

        # link the playing state and position
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    # open file 
    def open_file(self):
        # get filename
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video')

        # open the file 
        if filename != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    # play the video
    def play_video(self):
        # get play state
        # if playing, pause, vice versa
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # change icon
    # if playing, use pause icon, vice versa
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # change playing position by slider
    def position_changed(self, position):
        self.slider.setValue(position)

    # change playing duration by slider
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # change playing position
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    # forward button
    def forward(self):
        # get position in millisecond
        position = self.mediaPlayer.position()
        # change position by set seconds
        position += SECONDS * 1000
        self.mediaPlayer.setPosition(position)

    # backward button
    def backward(self):
        # get position in millisecond
        position = self.mediaPlayer.position()
        # change position by set seconds
        position -= SECONDS * 1000
        self.mediaPlayer.setPosition(position)

# run the program
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())