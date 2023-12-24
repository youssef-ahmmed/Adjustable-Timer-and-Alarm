# coding:utf-8
import sys
from datetime import datetime

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout
from qmaterialwidgets import (NavigationItemPosition, CheckBox, FilledPushButton, MessageBox, setTheme, Theme, BottomNavMaterialWindow,
                              SubtitleLabel, setFont, TimePicker)
from qmaterialwidgets import FluentIcon as FIF

from serial_communication import SerialCommunication


class ClockInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel('Clock', self)
        self.picker = TimePicker(self)
        self.currentTimeCheck = CheckBox('Current Time', self)
        self.setClockButton = FilledPushButton('Set Clock', self)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.picker.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.picker, 3, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.currentTimeCheck, 1, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.setClockButton, 1, Qt.AlignCenter)
        self.setObjectName('Clock')

        self.serial = SerialCommunication.get_instance()


        self.setClockButton.clicked.connect(self.get_clock_data)
        self.currentTimeCheck.stateChanged.connect(self.toggle_editability)


    def toggle_editability(self, state):
        self.picker.setReadOnly(state == 2)

    def get_clock_data(self):
        print(f'get_clock_data')
        if self.currentTimeCheck.isChecked():
            hours = str(datetime.now().hour)
            minutes = str(datetime.now().minute)
        else:
            print(self.picker.time)
            hours = str(self.picker.time.hour())
            minutes = str(self.picker.time.minute())

        hours = '0' + hours if len(hours) == 1 else hours
        minutes = '0' + minutes if len(minutes) == 1 else minutes

        clock_time = hours + minutes + '00'

        print(clock_time)

        self.send_clock_data(clock_time)


    def send_clock_data(self, clock_time):
        print(f'send_clock_data {clock_time}')
        self.serial.open_connection()
        self.serial.write_data('1' + clock_time + '0')
        self.serial.close_connection()
        print(f'send_clock_data {clock_time}')
