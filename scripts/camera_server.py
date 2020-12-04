#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np


cap = cv2.VideoCapture(0)

camera_frequency = 20 # 20Hz

def talker():
    pub = rospy.Publisher('camera_rgb', Image, queue_size=10)
    rospy.init_node('camera_server', anonymous=True)
    rate = rospy.Rate(camera_frequency)


    while not rospy.is_shutdown():
        ret, frame = cap.read()
        print("hello")
        cv2.imshow('frame', frame)
        height = frame.shape[0]
        width = frame.shape[1]
        flattened_rgb = frame.flatten()

        '''

        #construct msg
        rgb = Image()
        rgb.width = width
        rgb.height = height
        rgb.data = flattened_rgb


        rospy.loginfo(rgb)
        pub.publish(rgb)
        '''
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
