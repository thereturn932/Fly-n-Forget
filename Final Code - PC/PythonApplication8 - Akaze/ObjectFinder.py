#from __future__ import print_function
import cv2
import numpy as np
import os
import glob
import math
import time
#from dronekit import connect



def arm_and_takeoff(vehicle):

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
	#while not vehicle.is_armable:
        #print(" Waiting for vehicle to initialise...")
        #time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    #vehicle.mode    = VehicleMode("STABILIZE")
    vehicle.armed   = True


'''
	vehicle.channels.overrides = {'1':Roll} #Roll
	vehicle.channels.overrides = {'2':Pitch} #Pitch
	vehicle.channels.overrides = {'3':Throttle} #Throttle
	vehicle.channels.overrides = {'4':1500} #Yaw
'''

#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280,720))
cap = cv2.VideoCapture(0)
dst = None
def find(DIM, K, D, img_files, img_order = 0):
    '''
    print('Connecting to vehicle on: /dev/ttyAMA0')
    vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=921600)
    
    arm_and_takeoff(vehicle)
    '''
    differences = []
    img = cv2.imread(img_files[img_order],-1)
    akaze = cv2.AKAZE_create()
    kp_image, desc_image = akaze.detectAndCompute(img,None)
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    '''
    index_params = dict(algorithm=0,trees = 5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    '''

    try:
        while True:
            start = time.time()
            _,frame = cap.read()
            h,w = frame.shape[:2]
            map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
            undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            grayframe = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)
            kp_grayframe, desc_grayframe = akaze.detectAndCompute(grayframe,None)
            try:
                matches = matcher.knnMatch(desc_image, desc_grayframe, 2)
            except Exception as e:
                print(e)
                matches = []
            good_points=[]
            for m,n in matches:
                if m.distance < 0.8*n.distance:
                    good_points.append(m)

            #homography
            if len(good_points) > 10:
                query_points = np.float32([kp_image[m.queryIdx].pt for m in good_points]).reshape(-1,1,2)
                train_pts = np.float32([kp_grayframe[m.trainIdx].pt for m in good_points]).reshape(-1,1,2)

                matrix = np.array([])

                matrix, mask = cv2.findHomography(query_points, train_pts, cv2.RANSAC, 5.0)
                matches_mask = mask.ravel().tolist()

                h, w = img.shape[:-1]
                pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        

                try:
                    if np.any(matrix == None):
                        matrix = np.array([])
                    if not matrix.size == 0:
                        dst = cv2.perspectiveTransform(pts, matrix)
                    dst_1 = tuple(np.int32(dst[0]))
                    a = dst_1[0]
                    pt_1 = (a[0],a[1])

                    dst_2 = tuple(np.int32(dst[1]))
                    b = dst_2[0]
                    pt_2 = (b[0],b[1])

                    dst_3 = tuple(np.int32(dst[2]))
                    c = dst_3[0]
                    pt_3 = (c[0],c[1])

                    dst_4 = tuple(np.int32(dst[3]))
                    d = dst_4[0]
                    pt_4 = (d[0],d[1])

                    crn_1 = (np.int32((a[0]+b[0])/2),np.int32((a[1]+b[1])/2))
                    crn_2 = (np.int32((c[0]+d[0])/2),np.int32((c[1]+d[1])/2))

                    cv2.rectangle(frame, crn_1, crn_2, (255, 0, 0), 3)
                    rect1center = ((168+2)/2, (95+20)/2)
                    rect2center = ((366+40)/2, (345+522)/2)
                    center = ((crn_1[0]+crn_2[0])/2,(crn_1[1]+crn_2[1])/2)
                    m = np.int32(center[0])
                    n = np.int32(center[1])
                    i = (m,n)
                    cv2.circle(frame, i, 3, (255, 0, 0), 1)

                    cv2.circle(frame, (320,240), 3, (255, 0, 0), 1)
                    cv2.line(frame, i, (320,240), (255, 0, 0), 1)
                    difference = (i[0]-320,i[1]-240)

                    
                    if len(differences)==10:
                        for i in range(1,10):
                            differences[i-1]=differences[i]
                        differences[9]=difference
                    else:
                        differences.append(difference)

                    print(differences)
                    stand_dev = np.mean(np.std(np.array(differences), axis = 0))
                    print(stand_dev)
                    if stand_dev<70 and len(differences)>5:
                        if difference[0]<0:
                            print('left')
                    	    #vehicle.channels.overrides = {'1':1350} #Roll
                        elif difference[0]>0:
                            print('right')
                            #vehicle.channels.overrides = {'1':1650} #Roll
                        if difference[1]<0:
                            print('up')
                            #vehicle.channels.overrides = {'2':1650} #Pitch
                        elif difference[1]>0:
                            print('down')
                            #vehicle.channels.overrides = {'2':1350} #Pitch
                    
                        if abs(difference[0])<20 and abs(difference[1])<20:
                            print('Image Changed')
                            img_order += 1
                            img = cv2.imread(img_files[img_order],-1)
                            kp_image, desc_image = sift.detectAndCompute(img,None)
                            img = cv2.drawKeypoints(img,kp_image,img)
                            '''
                            vehicle.channels.overrides = {'1':None} #Roll
                            vehicle.channels.overrides = {'2':None} #Pitch
                            vehicle.channels.overrides = {'3':None} #Throttle
                            vehicle.channels.overrides = {'4':None} #Yaw
                            '''
                    cv2.imshow("Homography", frame)
                    end = time.time()
                    print(end-start)
                except Exception as e:
                     print(e)

            else:
                cv2.circle(frame, (640,320), 3, (255, 0, 0), 1)
                cv2.imshow("Homography", frame)
                #out.write(frame)
                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    except Exception as e:
        print('Video Finished')
    cap.release()
    cv2.destroyAllWindows()


