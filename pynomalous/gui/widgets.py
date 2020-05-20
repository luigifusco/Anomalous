from PySide2.QtCore import Slot
from PySide2.QtWidgets import QVBoxLayout, QWidget, QComboBox, QFormLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class PlotWidget(QWidget):
    def __init__(self, parent=None, w=450, h=350):
        super().__init__(parent)

        fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.toolbar)
        self.lay.addWidget(self.canvas)

        self.line, *_ = self.ax.plot([])

        self.setLayout(self.lay)
        self.setFixedSize(w, h)

    @Slot(list)
    def update_plot(self, data):
        self.line.set_data(range(len(data)), data)

        self.ax.set_xlim(0, len(data))
        self.ax.set_ylim(min(data), max(data))
        self.canvas.draw()


class ComboPlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo = QComboBox()
        self.lay.insertWidget(0, self.combo)

    @Slot(list)
    def update_combo_box(self, data):
        self.combo.clear()
        for item in data:
            self.combo.addItem(item)


class DerivationsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plots = [ComboPlotWidget() for _ in range(4)]
        self.lay = QFormLayout()
        self.lay.addRow(self.plots[0], self.plots[1])
        self.lay.addRow(self.plots[2], self.plots[3])

        self.setLayout(self.lay)


class AllPlotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.derivations = DerivationsWidget()
        self.bpm = PlotWidget(w=900)
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.derivations)
        self.lay.addWidget(self.bpm)

        self.setLayout(self.lay)
