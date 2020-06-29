from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox
from anomalousMainPageGUI import Ui_MainWindow

def onAnalysisClick():
    if(len(ui.filepathEdit.toPlainText()) == 0 or len(ui.ageEdit.toPlainText()) == 0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Invalid input!")
        msg.setInformativeText("You have to compile filepath and patient's age before start the analysis")
        msg.setWindowTitle("Invalid input")


'Show the application main page'
main_app = QApplication([])
main_window = QWidget()
ui = Ui_MainWindow()
ui.setupUi(main_window)

ui.analysisButton.clicked.connect(onAnalysisClick)

main_window.show()
main_app.exec()
