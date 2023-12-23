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

    # disconnect from serial port
    def disconnect(self):
        self.serialPort.close()
        self.port = None
        self.connectionLabel.setText("No connection")
        self.connectionLabel.setStyleSheet("color: red")
        self.signalGroup.setEnabled(False)
        self.signalInfoGroup.setEnabled(False)
        self.connectBtn.setEnabled(True)
        self.disconnectBtn.setEnabled(False)

    # refreshBtn ports
    def refresh_ports(self):
        self.comboBox.clear()
        self.load_ports()
        if len(y_values) > 0:
            self.animate()

    def send_to_memory(self, data):
        self.serialPort.write(data.encode())

    def receive_data(self, serialPort):
        data = serialPort.readall()
        return data

    def animate(self):
        plt.cla()
        plt.plot(x_values, y_values)
        plt.show()
        try:
            self.avgFrequencyValue.setText(str(round(float(len(x_values) / sum(x_values)), 2)) + " MHz")
        except ZeroDivisionError:
            print("ZeroDivisionError")
            self.avgFrequencyValue.setText("ERROR")
        try:
            self.pulseWidthValue.setText(str(round(x_values[1] - x_values[0], 3)) + " sec")
        except IndexError:
            print("IndexError")
            self.pulseWidthValue.setText("ERROR")
        x_values.clear()
        y_values.clear()

    def readingSerialPortThread(self, serialPort):
        print("readingSerialPortThread")
        while True:
            if serialPort.isOpen() & serialPort.inWaiting() > 0:
                data = self.receive_data(serialPort)
                for i in range(60):
                    y_values.append(((int(data[i * 7 + 1:i * 7 + 2].hex(), 16) / 255) * 5))
                    x_values.append(int(data[(i * 7) + 2:(i * 7) + 6].hex(), 16) * 0.000001)
                # print table of x and y values
                # print("x_values: ", x_values)
                # print("y_values: ", y_values)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 756)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.connectionGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.connectionGroup.setGeometry(QtCore.QRect(20, 20 + 421 + 91 + 20, 760, 181))
        self.connectionGroup.setObjectName("connectionGroup")
        self.disconnectBtn = QtWidgets.QPushButton(self.connectionGroup)
        self.disconnectBtn.setGeometry(QtCore.QRect(450, 120, 93, 28))
        self.disconnectBtn.setObjectName("disconnectBtn")
        self.disconnectBtn.setEnabled(False)
        self.connectionStatusLabel = QtWidgets.QLabel(self.connectionGroup)
        self.connectionStatusLabel.setGeometry(QtCore.QRect(250, 30, 111, 16))
        self.connectionStatusLabel.setObjectName("connectionStatusLabel")
        self.connectBtn = QtWidgets.QPushButton(self.connectionGroup)
        self.connectBtn.setGeometry(QtCore.QRect(350, 120, 93, 28))
        self.connectBtn.setObjectName("connectBtn")
        self.connectionLabel = QtWidgets.QLabel(self.connectionGroup)
        self.connectionLabel.setGeometry(QtCore.QRect(450, 30, 100, 16))
        self.connectionLabel.setObjectName("connectionLabel")
        self.comboBox = QtWidgets.QComboBox(self.connectionGroup)
        self.comboBox.setGeometry(QtCore.QRect(250, 70, 291, 31))
        self.comboBox.setObjectName("comboBox")
        self.refreshBtn = QtWidgets.QPushButton(self.connectionGroup)
        self.refreshBtn.setGeometry(QtCore.QRect(250, 120, 93, 28))
        self.refreshBtn.setObjectName("refreshBtn")
        self.signalGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.signalGroup.setEnabled(False)
        self.signalGroup.setGeometry(QtCore.QRect(20, 210 - 181, 760, 421))
        self.signalGroup.setObjectName("signalGroup")
        self.signalWidget = QtWidgets.QWidget(self.signalGroup)
        self.signalWidget.setGeometry(QtCore.QRect(10, 30, 351, 381))
        self.signalWidget.setObjectName("signalWidget")
        self.signalInfoGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.signalInfoGroup.setEnabled(False)
        self.signalInfoGroup.setGeometry(QtCore.QRect(20, 640 - 181, 760, 91))
        self.signalInfoGroup.setObjectName("signalInfoGroup")
        self.avgFrequencyLabel = QtWidgets.QLabel(self.signalInfoGroup)
        self.avgFrequencyLabel.setGeometry(QtCore.QRect(20, 30, 121, 16))
        self.avgFrequencyLabel.setObjectName("avgFrequencyLabel")
        self.pulseWidthLabel = QtWidgets.QLabel(self.signalInfoGroup)
        self.pulseWidthLabel.setGeometry(QtCore.QRect(20, 60, 111, 16))
        self.pulseWidthLabel.setObjectName("pulseWidthLabel")
        self.avgFrequencyValue = QtWidgets.QLabel(self.signalInfoGroup)
        self.avgFrequencyValue.setGeometry(QtCore.QRect(220, 30, 55, 16))
        self.avgFrequencyValue.setText("")
        self.avgFrequencyValue.setObjectName("avgFrequencyValue")
        self.pulseWidthValue = QtWidgets.QLabel(self.signalInfoGroup)
        self.pulseWidthValue.setGeometry(QtCore.QRect(220, 60, 55, 16))
        self.pulseWidthValue.setText("")
        self.pulseWidthValue.setObjectName("pulseWidthValue")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.load_ports()
        self.connectBtn.clicked.connect(self.connect)
        self.disconnectBtn.clicked.connect(self.disconnect)
        self.refreshBtn.clicked.connect(self.refresh_ports)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Oscilloscope"))
        self.connectionGroup.setTitle(_translate("MainWindow", "Connection"))
        self.disconnectBtn.setText(_translate("MainWindow", "Disconnect"))
        self.connectionStatusLabel.setText(_translate("MainWindow", "Connection status:"))
        self.connectBtn.setText(_translate("MainWindow", "Connect"))
        self.connectionLabel.setText(_translate("MainWindow", "No connection"))
        self.refreshBtn.setText(_translate("MainWindow", "Refresh"))
        self.signalGroup.setTitle(_translate("MainWindow", "Signal"))
        self.signalInfoGroup.setTitle(_translate("MainWindow", "Signal information"))
        self.avgFrequencyLabel.setText(_translate("MainWindow", "Average frequency:"))
        self.pulseWidthLabel.setText(_translate("MainWindow", "Pulse width:"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())