from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTimeEdit, QPushButton

from serial_communication import SerialCommunication


def send_clock_data(clock_time):
    SerialCommunication.get_instance().write_data(clock_time)


class ClockTab(QWidget):

    def __init__(self):
        super().__init__()

        self.time_edit = QTimeEdit(self)
        self.set_clock_button = QPushButton('Set Clock', self)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.time_edit)
        layout.addWidget(self.set_clock_button)

        self.set_clock_button.clicked.connect(self.get_clock_data)

    def get_clock_data(self):
        hours = str(self.time_edit.time().hour())
        minutes = str(self.time_edit.time().minute())
        hours = '0' + hours if len(hours) == 1 else hours
        minutes = '0' + minutes if len(minutes) == 1 else minutes
        clock_time = hours + minutes + '00'

        send_clock_data(clock_time)
