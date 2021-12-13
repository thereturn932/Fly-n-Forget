#from __future__ import print_function
import cv2
import numpy as np
import os
import glob
import math
import time
#from dronekit import connect
#from droneapi.lib import VehicleMode
#import serial


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



cap = cv2.VideoCapture(0)
dst = None

LIFTING_THROTTLE = 1700
HOVER_THROTTLE = 1500

def get_altitude(vehicle):
    return vehicle.rangefinder.distance
'''
def take_off(vehicle):
    altitude = get_altitude()-9.5
    while altitude<2:
        #vehicle.channels.overrides = {'3':LIFTING_THROTTLE} #Throttle
    #vehicle.channels.overrides = {'3':HOVER_THROTTLE} #Throttle
    #vehicle.mode = VehicleMode("ALTHOLD")
    '''
def get_rotation(current_pos, target_pos):
    off_x = target_pos[0] - current_pos[0]
    off_y = target_pos[1] - current_pos[1]
    rotation = 90.00 + math.atan2(-off_y, off_x) * 57.2957795
    if rotation < 0:
        rotation += 360.00
    return rotation

def get_distance_metres(aLocation1, aLocation2):

    dlat = target_pos[0] - current_pos[0]
    dlong = target_pos[1] - current_pos[1]
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
'''
def rotate(vehicle, heading, relative=True):
    if relative:
        is_relative=1
    else:
        is_relative=0
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)
    vehicle.flush()

def turn(vehicle,wp1,wp2):
    rot = get_rotation(wp1,wp2)
    rotate(vehicle,rot,True)
    '''
def find(DIM, K, D, img_files, waypoints, img_order = 0, wp_order = 0):
    '''
    print('Connecting to vehicle on: /dev/ttyAMA0')
    vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=921600)
    
    arm_and_takeoff(vehicle)
    '''
    #turn(vehicle, waypoints[wp_order], waypoints[wp_order+1])
    differences = []
    img = cv2.imread(img_files[img_order],-1)
    print(img_files[img_order])
    akaze = cv2.ORB_create()
    kp_image, desc_image = akaze.detectAndCompute(img,None)
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)
    #take_off()
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

                    #cv2.rectangle(frame, crn_1, crn_2, (255, 0, 0), 3)
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


                    stand_dev = np.mean(np.std(np.array(differences), axis = 0))

                    if stand_dev<70 and len(differences)>5:
                        if difference[0]<0:
                            cv2.putText(frame, 'go left', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
                            print('left')
                    	    #vehicle.channels.overrides = {'1':1350} #Roll
                        elif difference[0]>0:
                            print('right')
                            cv2.putText(frame, 'go right', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
                            #vehicle.channels.overrides = {'1':1650} #Roll
                        if difference[1]<0:
                            cv2.putText(frame, 'go up', (10,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                            print('up')
                            #vehicle.channels.overrides = {'2':1650} #Pitch
                        elif difference[1]>0:
                            cv2.putText(frame, 'go down', (10,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                            print('down')
                            #vehicle.channels.overrides = {'2':1350} #Pitch
                    
                        if abs(difference[0])<50 and abs(difference[1])<50:
                            cv2.putText(frame, 'Image Changed', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 126, 255), 2, cv2.LINE_AA)
                            print('Image Changed')
                            img_order += 1
                            img = cv2.imread(img_files[img_order],-1)
                            kp_image, desc_image = akaze.detectAndCompute(img,None)
                            img = cv2.drawKeypoints(img,kp_image,img)
                            wwp_order += 1
                            #turn(vehicle, waypoints[wp_order], waypoints[wp_order+1])
                            #vehicle.channels.overrides = {'2':1800} #Pitch
                            road_time = time.time()

                    cv2.imshow("Homography", frame)
                    end = time.time()
                    print(end-start)
                except Exception as e:
                     print(e)

            else:
                cv2.circle(frame, (640,320), 3, (255, 0, 0), 1)
                cv2.imshow("Homography", frame)

                pass
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                print('OK')
                break
    except Exception as e:
        print('Video Finished')
        cap.release()
    cv2.destroyAllWindows()


