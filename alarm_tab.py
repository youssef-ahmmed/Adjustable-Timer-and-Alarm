from typing import List

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTimeEdit, QPushButton

from alarm_communicator import AlarmCommunicator
from alarm_slot import AlarmSlot


def add_trailing_zero(text):
    return '0' + text if len(text) == 1 else text


def remove_widgets(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()


class AlarmTab(QWidget):
    def __init__(self):
        super().__init__()
        self.AlarmCommunicator = AlarmCommunicator()
        self.errors: List[str] = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        set_alarm_label = QLabel('Set Alarm', self)
        layout.addWidget(set_alarm_label)

        alarm_time_edit = QTimeEdit(self)
        layout.addWidget(alarm_time_edit)

        set_alarm_button = QPushButton('Set Alarm', self)
        set_alarm_button.pressed.connect(lambda:
                                         self.AlarmCommunicator.
                                         send_alarm_time(alarm_time_edit.time(), self.errors))
        set_alarm_button.pressed.connect(self.show_alarms)
        set_alarm_button.pressed.connect(lambda: print(self.errors))
        layout.addWidget(set_alarm_button)

        self.alarm_list = QVBoxLayout()

        layout.addLayout(self.alarm_list)

    def show_alarms(self):
        remove_widgets(self.alarm_list)
        alarms_raw_value: List[str] = self.AlarmCommunicator.get_alarms()
        for alarm_value in alarms_raw_value:
            raw_hour = ''.join(alarm_value[:2])
            hour, daynight = (raw_hour, 'AM') if int(raw_hour) <= 12 else (
            add_trailing_zero(str(int(raw_hour) - 12)), 'PM')
            time = hour + ':' + alarm_value[-2:] + ' ' + daynight
            self.alarm_list.addWidget(AlarmSlot(time))
