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



img_files = ['test4.jpg','test5.jpg', 'test6.jpg', 'test7.jpg']
img_order = 0

img = cv2.imread(img_files[img_order],-1)
cap = cv2.VideoCapture(0)


DIM=(1280, 720)
K=np.array([[825.0763589590928, 0.0, 636.7751804064267], [0.0, 820.6514295548574, 352.12861013691986], [0.0, 0.0, 1.0]])
D=np.array([[-0.057929442590365775], [-0.31759936963789637], [0.7760044711088516], [-0.6029921125137964]])


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


'''
while True:
        if find(img, cap, DIM, K ,D) == True:
            img_order += 1

            cap.release()
            cv2.destroyAllWindows()
'''

