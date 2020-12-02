#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveKobuki
import argparse
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.movekobuki_object = MoveKobuki()

    def camera_callback(self,data):
        
        try:
            # We select bgr8 because its the OpneCV encoding by default
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        # We get image dimensions and crop the parts of the image we don't need
        # Bear in mind that because the first value of the image matrix is start and second value is down limit.
        # Select the limits so that it gets the line not too close and not too far, and the minimum portion possible
        # To make process faster.
        height, width, channels = cv_image.shape
        descentre = 160
        rows_to_watch = 20
        crop_img = cv_image[(height)/2+descentre:(height)/2+(descentre+rows_to_watch)][1:width]
        
        # image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        crop_img3 = cv2.resize(cv_image,(300,300))
        crop_img2 = cv_image[200:600, 500:1500]        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (17, 17), 0)

        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])

        # Threshold the HSV image to get only yellow colors
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
        
        # my mask
        mask_yellow = cv2.inRange(hsv2, lower_yellow, upper_yellow)
        res_yellow = cv2.bitwise_and(crop_img2,crop_img2,mask=mask_yellow)
        gray = cv2.cvtColor(res_yellow, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        minV = 30
        maxV = 100
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)
        m2 = cv2.moments(mask_yellow, False)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cy, cx = height/2, width/2
        
        try:
            cx2, cy2 = m2['m10']/m2['m00'], m2['m01']/m2['m00']
        except ZeroDivisionError:
            cy2, cx2 = height/2, width/2
 
        # Draw the centroid in the resultut image
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) 
        cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)
        
        # simulate lanes (line is really thick)
        # Draw the centroid in the resultut image

        # edges = cv2.Canny(res_yellow,minV,maxV) 
        edges = cv2.Canny(blackAndWhiteImage,50,150,apertureSize = 3) 
        kernel = np.ones((3,3),np.uint8)
        dilation = cv2.dilate(edges,kernel, iterations = 3)
        
        kernel = np.ones((15,15),np.float32)/25
        blurred = cv2.filter2D(dilation,-1,kernel)

        cv2.circle(dilation,(int(cx2), int(cy2)), 30, (255,0,0), -1)

        minLineLength = 2
        maxLineGap = 1
        lines = cv2.HoughLinesP(blurred,1,np.pi/180,100,minLineLength,maxLineGap)
        try:
            for line in lines:
                
                for x3,y3,x4,y4 in line:
                    cv2.line(crop_img2,(x3,y3),(x4,y4),(0,255,0),5)
                    xA = abs(x3) + 0.5 * abs(x4 - x3)
                    yA = abs(y3) + 0.5 * abs(y4 - y3)
        except:
            pass
        
        # show results
        cv2.imshow('dilation lines', dilation)
        cv2.imshow('crop_img2 lines', crop_img2)
        cv2.imshow("blurred dilation", blurred)
        cv2.imshow("Original", crop_img3)
        cv2.imshow("blackAndWhiteImage", blackAndWhiteImage)
        
        cv2.waitKey(1)
        # cm of lines
        if (cy == height/2 and cx == width/2):
            error_x = cx - width / 2;   
            rospy.loginfo("cx = "+str(cx))
        else:
            # error_x = (cx-300) - width / 2;
            error_x = (xA) - width / 2;
            rospy.loginfo("xA = "+str(xA))
             
        twist_object = Twist();
        twist_object.linear.x = 0.8;
        twist_object.angular.z = -error_x / 100;
        
        # Make it start turning
        self.movekobuki_object.move_robot(twist_object)
        
    def clean_up(self):
        self.movekobuki_object.clean_class()
        cv2.destroyAllWindows()
        
        

def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()
   
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        line_follower_object.clean_up()
        rospy.loginfo("shutting down")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()

    
    
if __name__ == '__main__':
    main()