from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
import cv2
import numpy as np
import ssh
from shutil import copy
from ObjectFinder import find

cnt = 1

img_files = []
coordinates = []
img_order = 0

#cap = cv2.VideoCapture('vid.mp4')



wp_loc = None


class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(606, 402)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.import_Waypoints = QtWidgets.QPushButton(self.centralwidget)
        self.import_Waypoints.setGeometry(QtCore.QRect(20, 20, 131, 23))
        self.import_Waypoints.setObjectName("import_Waypoints")
        self.import_Waypoints.clicked.connect(self.browse_way)
        self.Waypoint_List = QtWidgets.QListWidget(self.centralwidget)
        self.Waypoint_List.setGeometry(QtCore.QRect(20, 70, 221, 301))
        self.Waypoint_List.setObjectName("Waypoint_List")
        self.label_waypoints = QtWidgets.QLabel(self.centralwidget)
        self.label_waypoints.setGeometry(QtCore.QRect(20, 50, 61, 16))
        self.label_waypoints.setObjectName("label_waypoints")
        self.import_Coordinates = QtWidgets.QPushButton(self.centralwidget)
        self.import_Coordinates.setGeometry(QtCore.QRect(250, 20, 161, 23))
        self.import_Coordinates.setObjectName("import_Coordinates")
        self.import_Coordinates.clicked.connect(self.browse_coor)
        self.label_waypoint_coordinates = QtWidgets.QLabel(self.centralwidget)
        self.label_waypoint_coordinates.setGeometry(QtCore.QRect(250, 50, 131, 16))
        self.label_waypoint_coordinates.setObjectName("label_waypoint_coordinates")
        self.Coordinate_List = QtWidgets.QListWidget(self.centralwidget)
        self.Coordinate_List.setGeometry(QtCore.QRect(250, 70, 221, 301))
        self.Coordinate_List.setObjectName("Coordinate_List")
        self.Start_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Start_Button.setGeometry(QtCore.QRect(500, 340, 81, 31))
        self.Start_Button.setObjectName("Start_Button")
        self.Start_Button.clicked.connect(self.Search)
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
        self.textbox = QtWidgets.QLineEdit(MainWindow)
        self.textbox.move(500, 80)
        self.textbox.resize(100,20)
        self.textbox2 = QtWidgets.QLineEdit(MainWindow)
        self.textbox2.move(500, 120)
        self.textbox2.resize(100,20)
        self.password = QtWidgets.QLineEdit(MainWindow)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.move(500, 160)
        self.password.resize(100,20)
        self.label_IP_Address = QtWidgets.QLabel(self.centralwidget)
        self.label_IP_Address.setGeometry(QtCore.QRect(500, 42, 131, 16))
        self.label_IP_Address.setObjectName("label_IP_Address")
        self.label_User_Name = QtWidgets.QLabel(self.centralwidget)
        self.label_User_Name.setGeometry(QtCore.QRect(500, 82, 131, 16))
        self.label_User_Name.setObjectName("label_User_Name")
        self.label_Password = QtWidgets.QLabel(self.centralwidget)
        self.label_Password.setGeometry(QtCore.QRect(500, 122, 131, 16))
        self.label_Password.setObjectName("label_Password")
        '''
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.pixmap = QtGui.QPixmap("Logo.png")
        self.logo.setPixmap(self.pixmap)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 67, 24))
        '''
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.import_Waypoints.setText(_translate("MainWindow", "Import Waypoint Visuals"))
        self.label_waypoints.setText(_translate("MainWindow", "Waypoints"))
        self.import_Coordinates.setText(_translate("MainWindow", "Import Waypoint Coordinates"))
        self.label_waypoint_coordinates.setText(_translate("MainWindow", "Waypoint Coordinates"))
        self.label_IP_Address.setText(_translate("MainWindow", "IP Address"))
        self.label_User_Name.setText(_translate("MainWindow", "User Name"))
        self.label_Password.setText(_translate("MainWindow", "Password"))
        self.Start_Button.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport_Waypoints.setText(_translate("MainWindow", "Import Waypoints"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionGuide.setText(_translate("MainWindow", "Guide"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


    def browse_coor(self):
        filePaths, _ = QtWidgets.QFileDialog.getOpenFileNames(None, 
                                                       'Single File',
                                                       "C:/Users/Burak/Desktop/text",'*.txt')    
        global wp_loc
        for filePath in filePaths:
            print(filePath)
            wp_loc = filePath
            print('filePath',filePath, '\n')
            fileHandle = open(filePath, 'r', encoding='utf-8-sig')
            lines = fileHandle.readlines()
            for line in lines:
                self.Coordinate_List.addItem(line)
                coordinates.append(line)
                print(line)

    def browse_way(self):
        filePaths, _ = QtWidgets.QFileDialog.getOpenFileNames(None, 
                                                       'Multiple File',
                                                       "C:/Users/Burak/source/repos/PythonApplication8/PythonApplication8",
                                                      '*.jpg')
        global cnt
        for filePath in filePaths:
            itm = QtWidgets.QListWidgetItem( "Waypoint " + str(cnt) );
            itm.setIcon(QtGui.QIcon(filePath));
            img_files.append(filePath)
            self.Waypoint_List.addItem(itm);
            cnt = cnt + 1
            print(img_files)

    def Search(self):
        global wp_loc
        filelist = os.listdir('images')
        for fileName in filelist:
            os.remove("images/"+fileName)
        for img in img_files:
            copy(img,'images')
        if os.path.exists('waypoints.txt'):
            os.remove('waypoints.txt')
        print(wp_loc)
        copy(wp_loc, 'waypoints.txt')
        ssh.start_search(selif.label_IP_Address.test(),self.label_Password.text(), self.label_Password.text())

        DIM=(1280, 720)
        K=np.array([[825.0763589590928, 0.0, 636.7751804064267], [0.0, 820.6514295548574, 352.12861013691986], [0.0, 0.0, 1.0]])
        D=np.array([[-0.057929442590365775], [-0.31759936963789637], [0.7760044711088516], [-0.6029921125137964]])
        dir = 'images'
        filelist = os.listdir(dir)
        print(filelist)
        find(DIM, K ,D, filelist, coordinates)


