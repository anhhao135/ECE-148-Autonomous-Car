#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np


cap = cv2.VideoCapture(0)

camera_frequency = 20 # 20Hz


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

def talker():
    pub = rospy.Publisher('camera_rgb', Image, queue_size=10)
    rospy.init_node('camera_server', anonymous=True)
    rate = rospy.Rate(camera_frequency)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        height = frame.shape[0]
        width = frame.shape[1]
        flattened_rgb = frame.flatten()

        #construct msg
        rgb = Image()
        rgb.width = width
        rgb.height = height
        rgb.data = flattened_rgb


        rospy.loginfo(rgb)
        pub.publish(rgb)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
