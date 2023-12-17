from typing import List, Dict, Literal, Optional

from PyQt5.QtWidgets import QTimeEdit

from serial_communication import SerialCommunication
from util import Util

AlarmNumbers = Literal['1', '2', '3', '4']


class AlarmCommunicator:

    def __init__(self):
        self.serial = SerialCommunication.get_instance()
        self.alarms: Dict[AlarmNumbers, Optional[str]] = {
            '1': None,
            '2': None,
            '3': None,
            '4': None
        }

    def get_first_available_alarm_slot(self) -> Optional[AlarmNumbers]:
        return next((k for k, v in self.alarms.items() if v is None), None)

    def send_alarm_time(self, time: QTimeEdit, errors: List[str]):
        hour, minute = str(time.hour()), str(time.minute())
        hour = Util.add_trailing_zero(hour)
        minute = Util.add_trailing_zero(minute)
        alarm_time = hour + minute
        if self.get_first_available_alarm_slot() is None:
            errors.append('No available alarms!')
        else:
            self.alarms[self.get_first_available_alarm_slot()] = alarm_time

        print(self.alarms)

    def get_alarms(self) -> List[str]:
        self.serial.open_connection()
        self.serial.write_data('40')
        # self.serial.close_connection()

        # self.serial.open_connection()
        all_alarms = self.serial.read_data_by_bytes(16)
        self.serial.close_connection()
        print('after send 4', all_alarms)
        return [v for v in self.alarms.values() if v is not None]
