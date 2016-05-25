import sys
import os

from PyQt4 import QtGui
from PyQt4.QtGui import QLabel, QGroupBox, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QMessageBox, QLineEdit
from PyQt4.QtCore import Qt, QEvent

class OptionsDialog(QtGui.QDialog):

    def __init__(self, options):
        super(OptionsDialog, self).__init__()

        self.options = options

        self._init_ui()

    def _init_ui(self):
        """ Create the basic elements of the user interface.
        """
        self.setGeometry(100, 100, 350, 400)
        self.setWindowTitle('Options')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        # Slot scan debug output
        self.chk_slot_debug = QCheckBox("Save images of failed slot scans")
        self.chk_slot_debug.stateChanged.connect(self._slot_debug_clicked)
        self.chk_slot_debug.setTristate(False)
        state = 2 if self.options.slot_images else 0
        self.chk_slot_debug.setCheckState(state)

        # Set slot images directory
        self.txt_slot_files_dir = QLineEdit(self.options.slot_image_directory)

        # Shot slot images button
        btn_show_slot_files = QtGui.QPushButton('View Slot Image Files')
        btn_show_slot_files.setFixedWidth(200)
        btn_show_slot_files.clicked.connect(self._open_slot_image_files_dir)

        grp_debug = QGroupBox("Debugging Output")
        grp_debug_vbox = QVBoxLayout()
        grp_debug_vbox.addWidget(self.chk_slot_debug)
        grp_debug_vbox.addWidget(self.txt_slot_files_dir)
        grp_debug_vbox.addWidget(btn_show_slot_files)
        grp_debug_vbox.addStretch()
        grp_debug.setLayout(grp_debug_vbox)

        # ----- OK /CANCEL BUTTONS -------
        self._btn_cancel = QtGui.QPushButton("Cancel")
        self._btn_cancel.pressed.connect(self._dialog_close_cancel)
        self._btn_ok = QtGui.QPushButton("OK")
        self._btn_ok.pressed.connect(self._dialog_close_ok)

        hbox_ok_cancel = QtGui.QHBoxLayout()
        hbox_ok_cancel.addStretch(1)
        hbox_ok_cancel.addWidget(self._btn_cancel)
        hbox_ok_cancel.addWidget(self._btn_ok)
        hbox_ok_cancel.addStretch(1)

        # ----- MAIN LAYOUT -----
        vbox = QVBoxLayout()
        vbox.addWidget(grp_debug)
        vbox.addLayout(hbox_ok_cancel)

        self.setLayout(vbox)

    def getColorFromDialog(self):
        col = QtGui.QColorDialog.getColor()

        if col.isValid():
            print(col)

    def _slot_debug_clicked(self):
        self.options.slot_images = (self.chk_slot_debug.checkState() != 0)

    def _open_slot_image_files_dir(self):
        path = self.options.slot_image_directory
        path = os.path.abspath(path)

        if sys.platform == 'win32':
            try:
                os.startfile(path)
            except FileNotFoundError:
                QMessageBox.critical(self, "File Error", "Unable to find directory: '{}".format(path))
        else:
            QMessageBox.critical(self, "File Error", "Only available on Windows")

    def _dialog_close_ok(self):
        self.options.slot_images = (self.chk_slot_debug.checkState() != 0)
        self.options.slot_image_directory = self.txt_slot_files_dir.text()

        self.options.update_config_file()
        self.close()

    def _dialog_close_cancel(self):
        self.close()

