import sys

from PySide2.QtCore import QFile, QObject, Signal, QTimer
from PySide2.QtWidgets import QApplication

from pynomalous.gui.widgets import DerivationsWidget

import math
import numpy as np


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

    matplotlib_widget = DerivationsWidget()
    matplotlib_widget.show()

    dsl.dataChanged.connect(matplotlib_widget.plots[0].update_plot)
    sys.exit(app.exec_())