from __future__ import division

import os

from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLabel, QGroupBox, QVBoxLayout


class ImageFrame(QGroupBox):

    def __init__(self):
        super(ImageFrame, self).__init__()

        self.setTitle("Scan Image")
        self._init_ui()

    def _init_ui(self):
        # Image frame - displays image of the currently selected scan record
        self._frame = QLabel()
        self._frame.setStyleSheet("background-color: black; color: red; font-size: 30pt; text-align: center")
        self._frame.setFixedWidth(600)
        self._frame.setFixedHeight(600)
        self._frame.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self._frame)

        self.setLayout(vbox)

    def clear_frame(self):
        self._frame.clear()
        self._frame.setText("No Scan Selected")

    def display_puck_image(self, image):
        """ Called when a new row is selected on the record table. Displays the specified
        image (image of the highlighted scan) in the image frame
        """
        self._frame.clear()
        self._frame.setAlignment(Qt.AlignCenter)

        if image is not None:
            pixmap = image.to_qt_pixmap(self._frame.size())
            self._frame.setPixmap(pixmap)
        else:
            self._frame.setText("Image Not Found")
