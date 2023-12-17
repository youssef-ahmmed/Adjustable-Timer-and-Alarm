import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget

from alarm_tab import AlarmTab
from clock_tab import ClockTab


class AdjustableTimerAndAlarmApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Adjustable Timer and Alarm')
        self.setGeometry(100, 100, 500, 500)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        tab_widget = QTabWidget()

        clock_tab = ClockTab()
        alarm_tab = AlarmTab()

        tab_widget.addTab(clock_tab, 'Clock')
        tab_widget.addTab(alarm_tab, 'Alarm')

        layout.addWidget(tab_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = AdjustableTimerAndAlarmApp()
    timer_app.show()
    sys.exit(app.exec_())
