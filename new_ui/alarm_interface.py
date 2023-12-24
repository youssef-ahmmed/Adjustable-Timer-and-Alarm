# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QRect
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox
from qmaterialwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, BottomNavMaterialWindow,
                              SubtitleLabel, setFont, TimePicker, FilledPushButton)
from qmaterialwidgets import FluentIcon as FIF


class AlarmInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.alarm_set_group = QWidget(self)

        self.label = SubtitleLabel('Alarm', self.alarm_set_group)
        self.picker = TimePicker(self.alarm_set_group)
        self.setAlarmButton = FilledPushButton('Set Alarm', self.alarm_set_group)

        self.vBoxLayout = QVBoxLayout(self.alarm_set_group)
        self.hBoxLayout = QHBoxLayout(self.alarm_set_group)

        self.alarm_list_group = QWidget(self)
        

        self.alarm_set_group.setGeometry(-15, -50, 550, 300)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.picker.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.picker, 1, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.setAlarmButton, 1, Qt.AlignCenter)
        self.setObjectName('Alarm')