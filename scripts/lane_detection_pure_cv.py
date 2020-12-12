#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from std_msgs.msg import Float32

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter('bull_potato.avi', cv2.VideoWriter_fourcc('M','J','P','G'),20,(400,100))

while (True):
    ret, frame = cap.read()
    height, width, channels = frame.shape
    out.write(frame)

    #translate = 0
    #rows_to_watch = 100
    #img = frame[(height/2 + translate):(height/2 + translate+rows_to_watch), 0:width]
    frame = frame[200:300, 0:width]

    img = cv2.resize(frame, (400, 300))
    orig = img.copy()
    # get rid of white noise from grass

    kernel = np.ones((5, 5), np.float32)/15
    blurred = cv2.filter2D(img, -1, kernel)
    dilation = cv2.dilate(blurred, kernel, iterations=7)

    # changing colorspace to HSV
    hsv = cv2.cvtColor(dilation, cv2.COLOR_BGR2HSV)

    # setting threshold limits for color filter
    # lower = np.array([36, 25, 25])
    # upper = np.array([70, 255,255])
    lower = np.array([35, 0, 0])
    upper = np.array([85, 255, 255])
    #lower = np.array([60, 0, 0])
    #upper = np.array([100, 255, 255])

    # creating mask
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(dilation, dilation, mask=mask)
    res = cv2.bitwise_not(res)

    # changing to gray colorspace
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # changing to black and white color space
    (thresh, blackAndWhiteImage) = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY)

    # edges = cv2.Canny(blackAndWhiteImage,10,100,apertureSize = 3)

    # locating contours in image
    ret, thresh = cv2.threshold(blackAndWhiteImage, 127, 255, 0)
    contours, dummy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    cx_list = []
    cy_list = []
    # plotting contours and their centroids
    for contour in contours:
        area = cv2.contourArea(contour)
        print(area)
        if(area > 2000 and area < 50000):
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            m = cv2.moments(contour)
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
            centers.append([cx, cy])
            cx_list.append(int(m['m10'] / m['m00']))
            cy_list.append(int(m['m01'] / m['m00']))
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), -1)
    # print(centers)
 
    try:
        mid_x.data = int(0.5 * (cx_list[0] + cx_list[1]))
        mid_y.data = int(0.5 * (cy_list[0] + cy_list[1]))
        cv2.circle(img, (mid_x.data, mid_y.data), 7, (255, 0, 0), -1)
        # print(mid_x)
    except:
        pass

    if (len(cx_list) == 0):
        mid_x.data = 0

    elif (len(cx_list) == 1):
        mid_x.data = (cx_list[0])
        mid_y.data = cy_list[0]
        cv2.circle(img, (mid_x.data, mid_y.data), 7, (255, 0, 0), -1)

    pub.publish(mid_x)
    
    try:

        # plotting results
        #cv2.imshow("original", orig)
        #cv2.imshow("dilation", dilation)
        cv2.imshow("blackAndWhiteImage", res)
        cv2.imshow("contours_img", img)
        cv2.waitKey(1)

cap.release()
out.release()
