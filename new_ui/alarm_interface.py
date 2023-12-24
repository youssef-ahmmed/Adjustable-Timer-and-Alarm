# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl, QRect
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QLabel,
)
from qmaterialwidgets import (
    NavigationItemPosition,
    MessageBox,
    setTheme,
    Theme,
    BottomNavMaterialWindow,
    SubtitleLabel,
    setFont,
    TimePicker,
    FilledPushButton,
)
from qmaterialwidgets import FluentIcon as FIF
from typing import Callable, List
from alarm_communicator import AlarmCommunicator
from util import Util


class AlarmSlot(QWidget):
    def __init__(self, alarm_time, idx, show_cb: Callable, shrink_cb: Callable):
        super().__init__()

        self.alarm_text = alarm_time
        self.alarm_idx = idx + 1
        self.alarm_communicator = AlarmCommunicator.get_instance()
        self.show_callback = show_cb
        self.shrink_callback = shrink_cb

        self.widget = QWidget(self)
        layout = QHBoxLayout(self.widget)
        self.widget.setLayout(layout)
        self.widget.setGeometry(0, 0, 450, 80)
        alarm_label = QLabel(self.alarm_text, self.widget)
        layout.addWidget(alarm_label)
        alarm_label.setStyleSheet("color: white;")
        setFont(alarm_label, 24)

        delete_button = FilledPushButton("Delete", self.widget)
        delete_button.setGeometry(0, 0, 430, 50)
        layout.addWidget(delete_button)

        delete_button.clicked.connect(self.delete_alarm)
        delete_button.clicked.connect(
            lambda: self.alarm_communicator.delete_alarm(self.alarm_idx)
        )

    def delete_alarm(self):
        self.setParent(None)
        self.deleteLater()

    def delete_alarm(self):
        self.setParent(None)
        self.deleteLater()

    def delete_and_show(self):
        self.shrink_callback()
        self.delete_alarm()
        self.show_callback()


class AlarmInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.alarm_communicator = AlarmCommunicator.get_instance()
        self.alarm_list_height = 320

        self.alarm_set_group = QWidget(self)
        self.picker = TimePicker(self.alarm_set_group)
        self.setAlarmButton = FilledPushButton("Set Alarm", self.alarm_set_group)

        self.vBoxLayout = QVBoxLayout(self.alarm_set_group)
        self.hBoxLayout = QHBoxLayout(self.alarm_set_group)

        self.alarm_set_group.setGeometry(-15, 0, 550, 300)

        self.picker.setAlignment(Qt.AlignCenter)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.picker, 1, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.setAlarmButton, 1, Qt.AlignCenter)
        self.setObjectName("Alarm")

        self.alarm_list_group = QWidget(self)

        self.alarm_list_group.setGeometry(20, 220, 550, self.alarm_list_height)
        self.setAlarmButton.pressed.connect(
            lambda: self.alarm_communicator.send_alarm_time(
                self.picker.time, ''
            )
        )
        self.setAlarmButton.pressed.connect(lambda: self.show_alarms())
        self.alarmListLayout = QVBoxLayout(self.alarm_list_group)

        self.getterButton = FilledPushButton("Show Alarms", self.alarm_set_group)
        self.getterButton.pressed.connect(lambda: self.show_alarms())
        self.vBoxLayout.addWidget(self.getterButton, 1, Qt.AlignCenter)

    def show_alarms(self):
        Util.remove_widgets(self.alarmListLayout)
        alarms_raw_value: List[str] = self.alarm_communicator.get_alarms()
        self.number_of_alarms = len(alarms_raw_value)
        for idx, alarm_value in enumerate(alarms_raw_value):
            if alarm_value is not None:
                raw_hour = "".join(alarm_value[:2])
                hour, daynight = (
                    (raw_hour, "AM")
                    if int(raw_hour) <= 12
                    else (Util.add_trailing_zero(str(int(raw_hour) - 12)), "PM")
                )
                time = hour + ":" + alarm_value[-2:] + " " + daynight
                self.alarmListLayout.addWidget(
                    AlarmSlot(time, idx, self.show_alarms, self.shrink_alarm_list)
                )

    def shrink_alarm_list(self):
        print("shrinking :", self.alarm_list_height)
