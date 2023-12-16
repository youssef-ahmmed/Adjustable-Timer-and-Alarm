import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QTimeEdit, QPushButton, QListWidget, QListWidgetItem, QHBoxLayout, QLabel


class AlarmWidget(QWidget):
    def __init__(self, alarm_time, list_widget, parent=None):
        super().__init__(parent)
        self.alarm_time = alarm_time
        self.list_widget = list_widget
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        time_label = QLabel(self.alarm_time.toString("hh:mm AP"))
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_alarm)

        layout.addWidget(time_label)
        layout.addWidget(delete_btn)

        self.setLayout(layout)

    def delete_alarm(self):
        item = self.find_item()
        if item is not None:
            row = self.list_widget.row(item)
            self.list_widget.takeItem(row)

    def find_item(self):
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            if item.widget() == self:
                return item
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Alarm Widget")
        self.setGeometry(200, 200, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.create_alarm_tab()

    def create_alarm_tab(self):
        alarm_tab = QWidget()
        alarm_layout = QVBoxLayout()

        time_edit = QTimeEdit()
        add_button = QPushButton("Set Alarm")
        list_widget = QListWidget()

        add_button.clicked.connect(lambda: self.add_alarm(time_edit.time(), list_widget))

        alarm_layout.addWidget(time_edit)
        alarm_layout.addWidget(add_button)
        alarm_layout.addWidget(list_widget)

        alarm_tab.setLayout(alarm_layout)
        self.tab_widget.addTab(alarm_tab, "Alarms")

    def add_alarm(self, alarm_time, list_widget):
        alarm_item = AlarmWidget(alarm_time, list_widget)
        list_item = QListWidgetItem(list_widget)
        list_item.setSizeHint(alarm_item.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, alarm_item)


def run_app():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
