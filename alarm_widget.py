from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton


class AlarmWidget(QWidget):
    def __init__(self, alarm_text):
        super().__init__()

        self.alarm_text = alarm_text

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        alarm_label = QLabel(self.alarm_text, self)
        layout.addWidget(alarm_label)

        delete_button = QPushButton('Delete', self)
        delete_button.clicked.connect(self.deleteAlarm)
        layout.addWidget(delete_button)

    def deleteAlarm(self):
        self.setParent(None)
        self.deleteLater()
