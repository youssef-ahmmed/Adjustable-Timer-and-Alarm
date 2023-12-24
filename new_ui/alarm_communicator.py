from typing import List, Dict, Literal, Optional

from PyQt5.QtWidgets import QTimeEdit

from serial_communication import SerialCommunication
from util import Util

AlarmNumbers = Literal["1", "2", "3", "4"]


class AlarmCommunicator:
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not AlarmCommunicator._instance:
            self.serial = SerialCommunication.get_instance()
            self.alarms: Dict[AlarmNumbers, Optional[str]] = {
                "1": None,
                "2": None,
                "3": None,
                "4": None,
            }
            AlarmCommunicator._instance = self

    def get_first_available_alarm_slot(self) -> Optional[AlarmNumbers]:
        return next((k for k, v in self.alarms.items() if v is None), None)

    def send_alarm_time(self, time: QTimeEdit, errors: List[str]):
        hour, minute = str(time.hour()), str(time.minute())
        hour = Util.add_trailing_zero(hour)
        minute = Util.add_trailing_zero(minute)
        alarm_time = hour + minute
        self.serial.open_connection()
        self.serial.write_data("2" + alarm_time)
        self.serial.close_connection()

        print(self.alarms)

    def delete_alarm(self, idx):
        self.serial.open_connection()
        self.serial.write_data(f"3{idx}0")
        self.serial.close_connection()

    def get_alarms(self) -> List[str]:
        self.serial.open_connection()
        self.serial.write_data("4")
        # all_alarms = self.serial.read_data_by_bytes(16)
        all_alarms = "FFFF0314FFFF0941"

        print(all_alarms)

        print("get_alarms: ", all_alarms)
        for c in range(0, 4):
            alarm = all_alarms[c * 4 : c * 4 + 4]
            if alarm == "FFFF":
                self.alarms[str(c + 1)] = None
            else:
                self.alarms[str(c + 1)] = alarm
        self.serial.close_connection()
        return [v for v in self.alarms.values()]

    def get_nums_of_alarms(self) -> int:
        return len([v for v in self.alarms.values() if v is not None])
