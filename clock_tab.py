from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTimeEdit, QPushButton


class ClockTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        time_edit = QTimeEdit(self)
        layout.addWidget(time_edit)

        set_clock_button = QPushButton('Set Clock', self)
        layout.addWidget(set_clock_button)
