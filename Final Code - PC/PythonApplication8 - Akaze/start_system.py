from ObjectFinder import find
import numpy as np


DIM=(1280, 720)
K=np.array([[825.0763589590928, 0.0, 636.7751804064267], [0.0, 820.6514295548574, 352.12861013691986], [0.0, 0.0, 1.0]])
D=np.array([[-0.057929442590365775], [-0.31759936963789637], [0.7760044711088516], [-0.6029921125137964]])
dir = '/home/pi/FlynForget/images'
filelist = os.listdir(dir)

find(DIM, K ,D, img_files = filelist)