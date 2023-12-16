from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTimeEdit, QPushButton, QListWidget, QListWidgetItem

from alarm_widget import AlarmWidget


class AlarmTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        set_alarm_label = QLabel('Set Alarm', self)
        layout.addWidget(set_alarm_label)

        alarm_time_edit = QTimeEdit(self)
        layout.addWidget(alarm_time_edit)

        set_alarm_button = QPushButton('Set Alarm', self)
        layout.addWidget(set_alarm_button)

        remove_alarm_label = QLabel('Existing Alarms', self)
        layout.addWidget(remove_alarm_label)

        alarm_list_widget = QListWidget(self)
        layout.addWidget(alarm_list_widget)

        alarm1 = AlarmWidget("Alarm 1")
        alarm2 = AlarmWidget("Alarm 2")

        # Add items to the QListWidget
        self.addAlarmToWidget(alarm_list_widget, alarm1)
        self.addAlarmToWidget(alarm_list_widget, alarm2)

        # remove_alarm_button = QPushButton('Remove Selected', self)
        # layout.addWidget(remove_alarm_button)

        show_alarms_button = QPushButton('Show Alarms', self)
        layout.addWidget(show_alarms_button)

    def addAlarmToWidget(self, alarm_list_widget, alarm_widget):
        item = QListWidgetItem()
        alarm_list_widget.addItem(item)
        alarm_list_widget.setItemWidget(item, alarm_widget)
