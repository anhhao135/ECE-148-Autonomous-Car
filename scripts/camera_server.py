#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge

cap = cv2.VideoCapture(0)

camera_frequency = 10 # 20Hz

def talker():
    pub = rospy.Publisher('camera_rgb', Image, queue_size=10)
    rospy.init_node('camera_server', anonymous=True)
    rate = rospy.Rate(camera_frequency)


    while not rospy.is_shutdown():
        ret, frame = cap.read()



        #construct msg
        bridge = CvBridge()
        rgb = bridge.cv2_to_imgmsg(frame)
        pub.publish(rgb)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
