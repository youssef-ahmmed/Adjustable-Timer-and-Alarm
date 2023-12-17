from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton


class AlarmSlot(QWidget):
    def __init__(self, alarm_time):
        super().__init__()

        self.alarm_text = alarm_time

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        alarm_label = QLabel(self.alarm_text, self)
        layout.addWidget(alarm_label)

        delete_button = QPushButton('Delete', self)
        delete_button.clicked.connect(self.delete_alarm)
        layout.addWidget(delete_button)

    def delete_alarm(self):
        self.setParent(None)
        self.deleteLater()
