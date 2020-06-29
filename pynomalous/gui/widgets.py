from PySide2.QtCore import Slot
import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QFormLayout, QLineEdit, QPushButton
from PySide2.QtWidgets import QGridLayout, QDial, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class PlotWidget(QWidget):
    def __init__(self, parent=None, w=400, h=350, toolbar=False):
        super().__init__(parent)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.lay = QVBoxLayout(self)
        if toolbar:
            self.toolbar = NavigationToolbar(self.canvas, self)
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
        self.fig.tight_layout()
        self.canvas.draw()


class ComboPlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo = QComboBox()
        self.combo.setFixedWidth(150)
        self.lay.insertWidget(0, self.combo, alignment=QtCore.Qt.AlignCenter)
        self.lay.setMargin(0)
        self.lay.setSpacing(0)

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
        self.lay.setSpacing(0)

        self.setLayout(self.lay)


class AllPlotsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.derivations = DerivationsWidget()
        self.lay = QVBoxLayout()
        self.lay.addWidget(self.derivations)

        self.setLayout(self.lay)


class Indicators(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lay = QGridLayout()
        self.button_names = [
            "A",
            "F",
            "Q",
            "n",
            "R",
            "B",
            "S",
            "j",
            "+",
            "V"
        ]
        self.buttons = {
            "A": QPushButton("A"),
            "F": QPushButton("F"),
            "Q": QPushButton("Q"),
            "n": QPushButton("n"),
            "R": QPushButton("R"),
            "B": QPushButton("B"),
            "S": QPushButton("S"),
            "j": QPushButton("j"),
            "+": QPushButton("+"),
            "V": QPushButton("V")
        }

        self.quality_label = QLabel("text")
        self.beat_label = QLabel("text")


        self.lay.addWidget(self.quality_label, 0, 0)
        self.lay.addWidget(self.beat_label, 0, 1)

        for i, b in zip(range(len(self.button_names)), self.button_names):
            self.lay.addWidget(self.buttons[b], i/2 + 1, i%2)

        self.setLayout(self.lay)


class AllData(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lay = QHBoxLayout()
        self.plots = AllPlotsWidget()
        self.indicators = Indicators()
        self.lay.addWidget(self.plots)
        self.lay.addWidget(self.indicators)

        self.setLayout(self.lay)


class FileSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lay = QHBoxLayout()
        self.file_input = QLineEdit()
        self.age_input = QLineEdit()
        self.button = QPushButton("Analyze")

        self.lay.addWidget(self.file_input)
        self.lay.addWidget(self.age_input)
        self.lay.addWidget(self.button)

        self.setLayout(self.lay)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lay = QVBoxLayout()
        self.file_selector = FileSelector()
        self.all_data = AllData()

        self.lay.addWidget(self.file_selector)
        self.lay.addWidget(self.all_data)

        self.setLayout(self.lay)
