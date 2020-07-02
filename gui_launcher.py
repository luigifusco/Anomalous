import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys

from PySide2.QtCore import QFile, QObject, Signal, QTimer
from PySide2.QtWidgets import QApplication
import pynomalous

from pynomalous.gui.widgets import PlotWidget, AllData, MainWindow, FileSelectorWindow

import math
import numpy as np
import matplotlib.style as mplstyle
mplstyle.use('fast')

class DSL(QObject):
    dataChanged = Signal(list)

    def __init__(self, parent=None):
        # LOAD HMI
        super().__init__(parent)

        self.data = []
        self.offset = 0

    def mainLoop(self):
        self.offset += 0.1
        self.data = [math.sin(i) for i in np.arange(self.offset, self.offset+10, 0.1)]
        # Send data to graph
        self.dataChanged.emit(self.data)
        # LOOP repeater
        QTimer.singleShot(1000, self.mainLoop)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dsl = DSL()
    dsl.mainLoop()

    main_window = MainWindow()
    file_selector_window = FileSelectorWindow()
    file_selector_window.show()

    def main_window_launcher():
        file_selector_window.close()
        file_name = file_selector_window.file_input.text()
        age = file_selector_window.age_input.text()

        pyn = pynomalous.Pynomalous()

        main_window.show()

    file_selector_window.button.clicked.connect(main_window_launcher)

    sys.exit(app.exec_())
