# You should replace these 3 lines with the output in calibration step
import cv2
import numpy as np
import os
import glob
import math
from ObjectFinder import find
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import GUI






if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


