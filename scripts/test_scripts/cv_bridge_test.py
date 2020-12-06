import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from decoder import decodeImage


def callback(data):
    #before we would put:
    #frame = bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
    #but imgmsg_to_cv2 function throws error on our environment
    #too much to fix so i just made the decode function from scratch its not that much anyways
    #so import it as shown above in your line detection stuff to decode the camera_rgb messages
    
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

