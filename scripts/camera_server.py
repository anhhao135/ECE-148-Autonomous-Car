#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge

NODE_NAME = 'camera_server'
PUBLISHER_NAME = 'camera_rgb'

cv2_video_capture = cv2.VideoCapture(0)

CAMERA_FREQUENCY = 10 # 20Hz


def talker():
    pub = rospy.Publisher(PUBLISHER_NAME, Image, queue_size=10)
    rospy.init_node(NODE_NAME, anonymous=True)
    rate = rospy.Rate(CAMERA_FREQUENCY)


    while not rospy.is_shutdown():
        ret, frame = cv2_video_capture.read()

        # construct msg
        bridge = CvBridge()
        rgb = bridge.cv2_to_imgmsg(frame)
        pub.publish(rgb)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
