from typing import Callable

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import QRect

from alarm_communicator import AlarmCommunicator


class AlarmSlot(QWidget):
    def __init__(self, alarm_time, idx, show_cb: Callable, shrink_cb: Callable):
        super().__init__()

        self.alarm_text = alarm_time
        self.alarm_idx = idx + 1
        self.alarm_communicator = AlarmCommunicator.get_instance()
        self.show_callback = show_cb
        self.shrink_callback = shrink_cb
        self.init_ui()

    def init_ui(self):
        self.widget = QWidget(self)
        layout = QHBoxLayout(self.widget)
        self.widget.setLayout(layout)
        self.widget.setGeometry(QRect(0, 0, 430, 50))
        alarm_label = QLabel(self.alarm_text, self)
        layout.addWidget(alarm_label)

        delete_button = QPushButton("Delete", self)
        delete_button.clicked.connect(self.delete_alarm)
        delete_button.clicked.connect(
            lambda: self.alarm_communicator.delete_alarm(self.alarm_idx)
        )
        delete_button.clicked.connect(self.shrink_callback)

        layout.addWidget(delete_button)

    def delete_alarm(self):
        self.setParent(None)
        self.deleteLater()

    def delete_and_show(self):
        self.shrink_callback()
        self.delete_alarm()
        # self.alarm_communicator.delete_alarm(self.alarm_idx)
        self.show_callback()
