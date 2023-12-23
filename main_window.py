import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from qmaterialwidgets import TimePicker

from qt_material import apply_stylesheet

from alarm_tab import AlarmTab
from clock_tab import ClockTab


class AdjustableTimerAndAlarmApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Adjustable Timer and Alarm')
        self.setGeometry(100, 100, 500, 600)


        main_widget = QWidget(self)

        self.picker = TimePicker(main_widget)
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout(main_widget)

        self.tab_widget = QTabWidget()

        self.clock_tab = ClockTab()
        self.alarm_tab = AlarmTab()

        self.tab_widget.addTab(self.clock_tab, 'Clock')
        self.tab_widget.addTab(self.alarm_tab, 'Alarm')

        self.tab_widget.tabBarClicked.connect(self.show_content)

        self.layout.addWidget(self.tab_widget)

    def show_content(self, index):
        if index == 1:
            self.alarm_tab.show_alarms()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = AdjustableTimerAndAlarmApp()
    timer_app.show()
    sys.exit(app.exec_())
