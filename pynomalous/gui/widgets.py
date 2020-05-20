from PySide2.QtCore import Slot
from PySide2.QtWidgets import QVBoxLayout, QWidget, QComboBox, QFormLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        fig = Figure(figsize=(7, 5), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.lay = QVBoxLayout(self)
        self.lay.addWidget(self.toolbar)
        self.lay.addWidget(self.canvas)

        self.ax = fig.add_subplot(111)
        self.line, *_ = self.ax.plot([])

        self.setLayout(self.lay)

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
