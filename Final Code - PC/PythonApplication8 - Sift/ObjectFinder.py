import cv2
import numpy as np
import os
import glob
import math

img_order = 0
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280,720))

def find(cap, DIM, K, D, img_files):
    global img_order
    img = cv2.imread(img_files[img_order],-1)
    sift = cv2.xfeatures2d.SIFT_create()
    kp_image, desc_image = sift.detectAndCompute(img,None)
    img = cv2.drawKeypoints(img,kp_image,img)

    #matching
    index_params = dict(algorithm=0,trees = 5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    try:
        while True:
        
            _,frame = cap.read()
            h,w = frame.shape[:2]
            map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
            undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            grayframe = cv2.cvtColor(undistorted_img, cv2.COLOR_BGR2GRAY)
            kp_grayframe, desc_grayframe = sift.detectAndCompute(grayframe,None)
            grayframe = cv2.drawKeypoints(grayframe, kp_grayframe, grayframe)
            try:
                matches = flann.knnMatch(desc_image, desc_grayframe, k=2)
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
                print(matrix)
                matches_mask = mask.ravel().tolist()

                h, w = img.shape[:-1]
                pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        

                try:
                    if np.any(matrix == None):
                        matrix = np.array([])
                    if not matrix.size == 0:
                        dst = cv2.perspectiveTransform(pts, matrix)
                    #homography = cv2.polylines(frame, [np.int32(dst)], True, (255, 0, 0), 3)
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

                    cv2.circle(frame, (640,360), 3, (255, 0, 0), 1)
                    cv2.line(frame, i, (640,360), (255, 0, 0), 1)
                    difference = (i[0]-640,i[1]-620)

            
                    if difference[0]<0:
                        cv2.putText(frame, 'go left', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
                    elif difference[0]>0:
                        cv2.putText(frame, 'go right', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
                    if difference[1]<0:
                        cv2.putText(frame, 'go up', (10,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
                    elif difference[1]>0:
                        cv2.putText(frame, 'go down', (10,350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
   
                    cv2.imshow("Homography", frame)
                    #out.write(frame)
                    if abs(difference[0])<20 and abs(difference[1])<20:
                        print('Image Changed')
                        img_order += 1
                        img = cv2.imread(img_files[img_order],-1)
                        kp_image, desc_image = sift.detectAndCompute(img,None)
                        img = cv2.drawKeypoints(img,kp_image,img)
                except Exception as e:
                     print(e)

            else:
                cv2.circle(frame, (640,320), 3, (255, 0, 0), 1)
                cv2.imshow("Homography", frame)
                #out.write(frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
    except Exception as e:
        print('Video Finished')
    cap.release()
    #out.release()
    cv2.destroyAllWindows()



