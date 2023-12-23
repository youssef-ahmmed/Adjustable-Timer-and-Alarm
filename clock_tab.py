from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTimeEdit, QPushButton, QCheckBox
from serial_communication import SerialCommunication
from datetime import datetime

class ClockTab(QWidget):

    def __init__(self):
        super().__init__()

        self.time_edit = QTimeEdit(self)
        self.set_clock_button = QPushButton('Set Clock', self)
        self.set_current_time_checkbox = QCheckBox('Set Current Time', self)

        self.serial = SerialCommunication.get_instance()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.time_edit)
        layout.addWidget(self.set_current_time_checkbox)
        layout.addWidget(self.set_clock_button)

        self.set_clock_button.clicked.connect(self.get_clock_data)
        self.set_current_time_checkbox.stateChanged.connect(self.toggle_editability)

    def toggle_editability(self, state):
        # If the checkbox is checked, make the QTimeEdit non-editable; otherwise, make it editable
        self.time_edit.setReadOnly(state == 2)

    def get_clock_data(self):
        if self.set_current_time_checkbox.isChecked():
            hours = str(datetime.now().hour)
            minutes = str(datetime.now().minute)
        else:
            hours = str(self.time_edit.time().hour())
            minutes = str(self.time_edit.time().minute())

        hours = '0' + hours if len(hours) == 1 else hours
        minutes = '0' + minutes if len(minutes) == 1 else minutes

        clock_time = hours + minutes + '00'

        print(clock_time)

        self.send_clock_data(clock_time)


    def send_clock_data(self, clock_time):
        self.serial.open_connection()
        self.serial.write_data('1' + clock_time + '0')
        self.serial.close_connection()
