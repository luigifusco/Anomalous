# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dectionZoom.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectionZoom(object):
    def setupUi(self, DetectionZoom):
        DetectionZoom.setObjectName("DetectionZoom")
        DetectionZoom.resize(535, 489)
        self.graphWidget = QtWidgets.QWidget(DetectionZoom)
        self.graphWidget.setGeometry(QtCore.QRect(10, 10, 511, 471))
        self.graphWidget.setObjectName("graphWidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.graphWidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 511, 441))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.detectionSpinBox = QtWidgets.QSpinBox(self.graphWidget)
        self.detectionSpinBox.setGeometry(QtCore.QRect(250, 450, 111, 22))
        self.detectionSpinBox.setObjectName("detectionSpinBox")
        self.label = QtWidgets.QLabel(self.graphWidget)
        self.label.setGeometry(QtCore.QRect(190, 450, 51, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(DetectionZoom)
        QtCore.QMetaObject.connectSlotsByName(DetectionZoom)

    def retranslateUi(self, DetectionZoom):
        _translate = QtCore.QCoreApplication.translate
        DetectionZoom.setWindowTitle(_translate("DetectionZoom", "Form"))
        self.label.setText(_translate("DetectionZoom", "DETECTION"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DetectionZoom = QtWidgets.QWidget()
    ui = Ui_DetectionZoom()
    ui.setupUi(DetectionZoom)
    DetectionZoom.show()
    sys.exit(app.exec_())
