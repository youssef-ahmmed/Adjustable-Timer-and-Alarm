from typing import List

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTimeEdit,
    QPushButton,
    QGroupBox,
)

from alarm_communicator import AlarmCommunicator
from alarm_slot import AlarmSlot
from util import Util


class AlarmTab(QWidget):
    def __init__(self):
        super().__init__()
        self.alarmCommunicator = AlarmCommunicator.get_instance()
        self.errors: List[str] = []
        self.alarm_list_height = 250
        self.init_ui()

    def init_ui(self):
        set_alarm_group_box = QGroupBox(self)

        set_alarm_group_box.setGeometry(20, 20, 430, 100)
        set_alarm_label = QLabel("Set Alarm", set_alarm_group_box)

        set_alarm_label.setGeometry(QRect(10, 0, 560, 40))

        alarm_time_edit = QTimeEdit(set_alarm_group_box)
        alarm_time_edit.setGeometry(QRect(20, 55, 200, 30))

        set_alarm_button = QPushButton("Set Alarm", set_alarm_group_box)
        set_alarm_button.setGeometry(QRect(300, 55, 100, 30))
        set_alarm_button.pressed.connect(
            lambda: self.alarmCommunicator.send_alarm_time(
                alarm_time_edit.time(), self.errors
            )
        )
        set_alarm_button.pressed.connect(self.show_alarms)
        set_alarm_button.pressed.connect(lambda: print(self.errors))

        self.alarm_list = QVBoxLayout(self)

        self.alarm_list.setDirection(QVBoxLayout.BottomToTop)
        alarm_list_group = QGroupBox(self)
        alarm_list_group.setStyleSheet("background-color: transparent;")
        alarm_list_group.setTitle("Alarms")
        self.alarm_list_virtual_group = QGroupBox(self)

        alarm_list_group.setStyleSheet("background-color: transparent;")
        alarm_list_group.setGeometry(20, 140, 430, self.alarm_list_height)
        self.alarm_list_virtual_group.setGeometry(20, 140, 430, self.alarm_list_height)

        self.alarm_list.addSpacing(10)
        self.alarm_list.addStretch()
        alarm_list_group.setLayout(self.alarm_list)
        self.alarm_list_virtual_group.setLayout(self.alarm_list)

        # list_width = 300  # Replace with your desired width
        # list_height = 100  # Replace with your desired height
        # self.alarm_list.setGeometry(QRect(20, 270, list_width, list_height))
        # self.alarm_list.setFixedSize(list_width, list_height)
        # self.setLayout(self.alarm_list)

    def show_alarms(self):
        Util.remove_widgets(self.alarm_list)
        alarms_raw_value: List[str] = self.alarmCommunicator.get_alarms()
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
                if self.alarm_list_height < 250:
                    self.alarm_list_height += 60
                    self.alarm_list_virtual_group.setGeometry(
                        20, 140, 430, self.alarm_list_height
                    )
                self.alarm_list.addWidget(
                    AlarmSlot(time, idx, self.show_alarms, self.shrink_alarm_list)
                )

    def shrink_alarm_list(self):
        self.alarm_list_height -= 60
        if self.alarmCommunicator.get_nums_of_alarms() == 0:
            self.alarm_list_height = 0
        self.alarm_list_virtual_group.setGeometry(20, 140, 430, self.alarm_list_height)
        print("shrinking :", self.alarm_list_height)
