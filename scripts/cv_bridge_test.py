#!/usr/bin/env python


import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import decoder


'''
def decodeImage(data, height, width): #function to replace self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
    decoded = np.fromstring(data, dtype=np.uint8)
    decoded = decoded.reshape((height, width, 3))
    return decoded
'''

def callback(data):
    frame = decodeImage(data.data, data.height, data.width) #take in data.data, with the height and width, and spit out a cv-workable np array
    #print(type(frame))
    #print(frame.shape)
    #print(frame)
    cv2.imshow("name", frame)
    cv2.waitKey(1)
    print("loop")



try:

    #bridge_object = CvBridge()
    rospy.init_node('cv_bridge_test_node', anonymous=True)
    image_sub = rospy.Subscriber("camera_rgb", Image, callback)
    rospy.spin()

except KeyboardInterrupt:
    cv2.destroyAllWindows()

