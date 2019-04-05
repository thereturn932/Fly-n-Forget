from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(606, 402)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 131, 23))
        self.pushButton.setObjectName("pushButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 70, 221, 301))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 20, 161, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.browse)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 50, 61, 16))
        self.label_2.setObjectName("label_2")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(250, 70, 221, 301))
        self.listWidget_2.setObjectName("listWidget_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 340, 81, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 606, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionImport_Waypoints = QtWidgets.QAction(MainWindow)
        self.actionImport_Waypoints.setObjectName("actionImport_Waypoints")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionGuide = QtWidgets.QAction(MainWindow)
        self.actionGuide.setObjectName("actionGuide")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionImport_Waypoints)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionGuide)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fly'n'Forget"))
        self.pushButton.setText(_translate("MainWindow", "Import Waypoint Visuals"))
        self.label.setText(_translate("MainWindow", "Waypoints"))
        self.pushButton_2.setText(_translate("MainWindow", "Import Waypoint Coordinates"))
        self.label_2.setText(_translate("MainWindow", "Waypoints"))
        self.pushButton_3.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport_Waypoints.setText(_translate("MainWindow", "Import Waypoints"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionGuide.setText(_translate("MainWindow", "Guide"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def browse(self):
        filePaths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 
                                                       'Multiple File',
                                                       "~/Desktop",
                                                      '*.txt')
        for filePath in filePaths:
            print('filePath',filePath, '\n')
            fileHandle = open(filePath, 'r')
            lines = fileHandle.readlines()
            for line in lines:
                print(line)



