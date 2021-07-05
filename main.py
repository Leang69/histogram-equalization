import sys

import cv2 as cv
from PySide2.QtGui import QImage
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QIODevice, Slot

from ImageProcessing import ImageProcessing


class Mainwindow:
    def __init__(self):
        ui_file_name = "mainwindow.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        if not self.window :
            print(loader.errorString())
            sys.exit(-1)
        self.window.show()
        self.myImageProcessing = ImageProcessing(self.window)

        self.window.stackedWidget.setCurrentIndex(0)

        self.window.actionExport_FIle.setEnabled(0)
        self.window.actionGray_Image.setEnabled(0)
        self.window.actionRGB_Image.setEnabled(0)
        self.window.Histogram_EqualizationNo.setEnabled(0)
        self.window.Histogram_EqualizationYes.setEnabled(0)

        self.window.actionImport_File.triggered.connect(self.importImage)
        self.window.actionExport_FIle.triggered.connect(self.exportImage)
        self.window.actionGray_Image.triggered.connect(self.grayScale)
        self.window.actionRGB_Image.triggered.connect(self.rgbScale)
        self.window.Histogram_EqualizationNo.triggered.connect(self.histogramEqualizationOff)
        self.window.Histogram_EqualizationYes.triggered.connect(self.histogramEqualizationOn)

    @Slot()
    def importImage(self):
        self.myImageProcessing.setImg(self.window)


    def exportImage(self):
        self.myImageProcessing.exportImage(self.window)

    def rgbScale(self):
        self.myImageProcessing.displayImage(self.myImageProcessing.imgRGB, QImage.Format_RGB888, self.window)
        self.myImageProcessing.outputImage = cv.cvtColor(self.myImageProcessing.imgRGB, cv.COLOR_BGR2RGB)

    def grayScale(self):
        self.myImageProcessing.setGrayImage(self.window)

    def histogramEqualizationOff(self):
        self.myImageProcessing.histogramImage(self.window)

    def histogramEqualizationOn(self):
        self.myImageProcessing.histogramEqualization(self.window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_main_window = Mainwindow()
    sys.exit(app.exec_())
