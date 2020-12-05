import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image





def callback(data):
    frame = bridge_object.imgmsg_to_cv2(data)
    print(type(frame))


bridge_object = CvBridge()
image_sub = rospy.Subscriber("camera_rgb", Image, callback)
rospy.spin()

