import serial
from serial.serialutil import SerialException


class SerialCommunication:

    _instance = None

    def __init__(self, port, baudrate):
        if not SerialCommunication._instance:
            self.port = port
            self.baudrate = baudrate
            self.serial = None
            SerialCommunication._instance = self
        else:
            print("An instance of SerialCommunication already exists.")

    @classmethod
    def get_instance(cls, port='COM1', baudrate=9600):
        if not cls._instance:
            cls._instance = cls(port, baudrate)
        return cls._instance

    def open_connection(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate)
        except SerialException as e:
            print(f"Error opening serial connection: {e}")

    def close_connection(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Serial connection closed.")

    def write_data(self, data):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(data.encode())
                print(f"Sent: {data}")
            except SerialException as e:
                print(f"Error writing data: {e}")

    def read_data_by_bytes(self, num_bytes):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.read(num_bytes).decode()
                print(f"Received: {data}")
                return data
            except SerialException as e:
                print(f"Error reading data: {e}")
        return None

    def read_all_data(self):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.readline().decode('utf-8')
                print(f"Received: {data}")
                return data
            except SerialException as e:
                print(f"Error reading data: {e}")
        return None
