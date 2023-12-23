import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import serial

x_values = []
y_values = []


class Ui_MainWindow(object):
    signalCount = 0
    modeOperation = ''
    port = None
    serialPort = None

    def load_ports(self):
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            self.comboBox.addItem(port.portName())

    # connect to selected port in combobox
    def connect(self):
        self.port = self.comboBox.currentText()
        # self.serial = QSerialPort(port)
        self.serialPort = serial.Serial(self.port, 9600, timeout=1)
        # if self.serial is open

        if self.serialPort.isOpen():
            self.connectionLabel.setText("Connected")
            self.connectionLabel.setStyleSheet("color: green")
            self.signalGroup.setEnabled(True)
            self.signalInfoGroup.setEnabled(True)
            signalReadingThread = Thread(target=self.readingSerialPortThread, daemon=True, args=(self.serialPort,))
            signalReadingThread.start()
            self.connectBtn.setEnabled(False)
            self.disconnectBtn.setEnabled(True)
        else:
            self.connectionLabel.setText("Not connected")
            self.connectionLabel.setStyleSheet("color: red")
            self.signalGroup.setEnabled(False)
            self.signalInfoGroup.setEnabled(False)
            self.port = None
            self.connectBtn.setEnabled(True)
            self.disconnectBtn.setEnabled(False)
import serial.tools.list_ports

def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    serial_ports = [port.device for port in ports]
    return serial_ports

if __name__ == "__main__":
    serial_ports = get_serial_ports()

    if serial_ports:
        print("Serial Ports:")
        for port in serial_ports:
            print(f"Port: {port}")
    else:
        print("No serial ports found.")
