# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout
from qmaterialwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, BottomNavMaterialWindow,
                              SubtitleLabel, setFont, TimePicker)
from qmaterialwidgets import FluentIcon as FIF


class AlarmInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel('Alarm', self)
        self.picker = TimePicker(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.picker.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.picker, 1, Qt.AlignCenter)
        self.setObjectName('Alarm')
