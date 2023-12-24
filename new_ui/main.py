# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout
from qmaterialwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, BottomNavMaterialWindow,
                              SubtitleLabel, setFont, TimePicker)
from qmaterialwidgets import FluentIcon as FIF

from alarm_interface import AlarmInterface
from clock_interface import ClockInterface


class Window(BottomNavMaterialWindow):

    def __init__(self):
        super().__init__()
        # create sub interface
        self.clockInterface = ClockInterface(self)
        self.alarmInterface = AlarmInterface(self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.clockInterface, FIF.DATE_TIME, 'Clock', FIF.DATE_TIME)
        self.addSubInterface(self.alarmInterface, FIF.CALENDAR, 'Alarm', FIF.CALENDAR)

        self.navigationInterface.setCurrentItem(self.clockInterface.objectName())

    def initWindow(self):
        self.resize(500, 700)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
