from typing import List

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTimeEdit, QPushButton, QListWidget, QListWidgetItem

from HardwareCommunicator import HardwareCommunicator
from alarm_widget import AlarmWidget


class AlarmTab(QWidget):
    def __init__(self):
        super().__init__()
        self.hardwareCommunicator = HardwareCommunicator()
        self.errors: List[str] = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        set_alarm_label = QLabel('Set Alarm', self)
        layout.addWidget(set_alarm_label)

        alarm_time_edit = QTimeEdit(self)
        layout.addWidget(alarm_time_edit)

        set_alarm_button = QPushButton('Set Alarm', self)
        set_alarm_button.pressed.connect(lambda:
                                         self.hardwareCommunicator.
                                         send_alarm_time(alarm_time_edit.time(), self.errors))
        set_alarm_button.pressed.connect(lambda: print(self.errors))
        layout.addWidget(set_alarm_button)

        remove_alarm_label = QLabel('Remove Alarm', self)
        layout.addWidget(remove_alarm_label)

        self.alarm_list = QVBoxLayout()

        layout.addLayout(self.alarm_list)


        show_alarms_button = QPushButton('Show Alarms', self)
        # show_alarms_button.pressed.connect(lambda :self.show_alarms(self.hardwareCommunicator.get_alarms()))
        layout.addWidget(show_alarms_button)

    def show_alarms(self):
        alarms_raw_value: List[str] = self.hardwareCommunicator.get_alarms()
        # 1533

