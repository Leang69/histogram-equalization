import os

import cv2 as cv
import numpy as np
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QFileDialog, QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.subplots()
        super(MplCanvas, self).__init__(self.fig)


class ImageProcessing:

    def __init__(self, mainWindow):
        self.sc = MplCanvas(self, width=5, height=5, dpi=100)
        self.toolbar = NavigationToolbar(self.sc, mainWindow)
        self.mainWindow = mainWindow
        self.canvaslayout = QVBoxLayout()
        self.canvaslayout.addWidget(self.toolbar)
        self.canvaslayout.addWidget(self.sc)
        self.canvasWidget = QWidget()
        self.canvasWidget.setFixedSize(500, 500)
        self.canvasWidget.setLayout(self.canvaslayout)
        self.mainWindow.page_2.layout().addWidget(self.canvasWidget)

    def setImg(self, central_widget):
        path_to_file, _ = QFileDialog.getOpenFileName(central_widget, "Select Image", os.path.dirname(__file__),
                                                      "Images (*.jpg *.bmp *.png *.tif)")
        if path_to_file != '':
            self.imgRGB = cv.imread(path_to_file)
            self.outputImage = self.imgRGB
            self.imgRGB = cv.cvtColor(self.imgRGB, cv.COLOR_BGR2RGB)
            self.displayImage(self.imgRGB, QImage.Format_RGB888, central_widget)
            central_widget.actionExport_FIle.setEnabled(1)
            central_widget.actionGray_Image.setEnabled(1)
            central_widget.actionRGB_Image.setEnabled(1)
            central_widget.Histogram_EqualizationNo.setEnabled(1)
            central_widget.Histogram_EqualizationYes.setEnabled(1)

    def exportImage(self, central_widget):
        path_to_file, _ = QFileDialog.getSaveFileName(central_widget, "Select location",os.path.dirname(__file__),"Images (*.jpg")
        if path_to_file != '':
            cv.imwrite(path_to_file, self.outputImage)

    def setGrayImage(self, central_widget):
        central_widget.stackedWidget.setCurrentIndex(0)
        imgR = np.array(self.imgRGB[:, :, 0])
        imgG = np.array(self.imgRGB[:, :, 1])
        imgB = np.array(self.imgRGB[:, :, 2])
        self.imgGray = np.uint8(np.add(np.add(0.299 * np.float16(imgR), 0.587 * np.float16(imgG)), 0.114 * np.float16(imgB)))
        self.outputImage = self.imgGray
        self.displayImage(self.imgGray, QImage.Format_Grayscale8, central_widget)

    def displayImage(self, img, fromatImage, central_widget):
        central_widget.stackedWidget.setCurrentIndex(0)
        img = QImage(img, img.shape[1], img.shape[0], img.strides[0], fromatImage)
        central_widget.label.setPixmap(QPixmap.fromImage(img.scaled(888, 500, Qt.KeepAspectRatio)))

    def histogramImage(self, centralWidget):
        centralWidget.stackedWidget.setCurrentIndex(1)
        imgR = np.array(self.imgRGB[:, :, 2])
        imgG = np.array(self.imgRGB[:, :, 1])
        imgB = np.array(self.imgRGB[:, :, 0])
        imgGray = np.uint8(np.add(np.add(0.299 * np.float16(imgR), 0.587 * np.float16(imgG)), 0.114 * np.float16(imgB)))
        hist, bin_edges = np.histogram(imgGray, bins=np.arange(257), density=True)
        self.sc.axes.cla()
        self.sc.axes.bar(np.arange(256), hist)
        self.sc.axes.figure.canvas.draw()
        img = QImage(imgGray, imgGray.shape[1], imgGray.shape[0], imgGray.strides[0], QImage.Format_Grayscale8)

        self.outputImage = imgGray

        centralWidget.label_2.setPixmap(QPixmap.fromImage(img.scaled(888, 500, Qt.KeepAspectRatio)))

    def histogramEqualization(self, centralWidget):
        centralWidget.stackedWidget.setCurrentIndex(1)
        imgR = np.array(self.imgRGB[:, :, 2])
        imgG = np.array(self.imgRGB[:, :, 1])
        imgB = np.array(self.imgRGB[:, :, 0])
        imgGray = np.uint8(np.add(np.add(0.299 * np.float16(imgR), 0.587 * np.float16(imgG)), 0.114 * np.float16(imgB)))
        hist, bin_edges = np.histogram(imgGray, bins=np.arange(257), density=True)

        cumsum = np.cumsum(hist) * 255
        outImg = np.zeros(imgGray.shape)


        for i in range(0, imgGray.shape[0]):
            for j in range(0, imgGray.shape[1]):
                outImg[i][j] = cumsum[imgGray[i][j]]

        outImg = np.uint8(np.round(outImg))

        outhist, newbin_edges = np.histogram(outImg, bins=np.arange(257), density=True)

        self.sc.axes.cla()
        self.sc.axes.bar(np.arange(256), outhist)
        self.sc.axes.figure.canvas.draw()

        self.outputImage = outImg

        img = QImage(np.uint8(outImg), np.uint8(outImg).shape[1], np.uint8(outImg).shape[0], np.uint8(outImg).strides[0], QImage.Format_Grayscale8)
        centralWidget.label_2.setPixmap(QPixmap.fromImage(img.scaled(888, 500, Qt.KeepAspectRatio)))



