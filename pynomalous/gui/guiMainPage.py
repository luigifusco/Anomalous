from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import anomalousMainPageGUI
import math
import numpy as np
import matplotlib.style as mplstyle
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5 import QtCore, QtWidgets
import sys
mplstyle.use('fast')


class DSL(QtCore.QObject):
    dataChanged = pyqtSignal(list)

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

def onAnalysisClick():
    if(len(ui.filepathEdit.toPlainText()) == 0 or len(ui.ageEdit.toPlainText()) == 0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Invalid input!")
        msg.setInformativeText("You have to compile filepath and patient's age before start the analysis")
        msg.setWindowTitle("Invalid input")


if __name__ == '__main__':
    main_app = QApplication(sys.argv)
    ui = MainWindow()

    ui.analysisButton.clicked.connect(onAnalysisClick)

    dsl = DSL()
    dsl.dataChanged.connect(ui.graphWidget.update_plot)

    ui.show()
    main_app.exec()
