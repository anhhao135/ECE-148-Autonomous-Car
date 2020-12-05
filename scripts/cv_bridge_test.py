#!/usr/bin/env python


import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image





def callback(data):
    frame = bridge_object.imgmsg_to_cv2(data)
    print(type(frame))
    print(type(data))


bridge_object = CvBridge()
rospy.init_node('cv_bridge_test_node', anonymous=True)
image_sub = rospy.Subscriber("camera_rgb", Image, callback)
rospy.spin()

