#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from std_msgs.msg import Float32, Int32


global steering_float, throttle_float
steering_float = Float32()
throttle_float = Float32()


def LineFollower(msg):
    global steering_float, throttle_float
    steering_float = Float32()
    throttle_float = Float32()
    width = 600
    if (msg.data == 0):
        error_x = 0
    else:
        error_x = float((msg.data) - width / 2)

    # rospy.loginfo("mid_x = "+str(msg.data))
    throttle_float = 0.3
    steering_float = float(-error_x / 100)
    return steering_float, throttle_float


def main():
    rospy.init_node('line_following_node1', anonymous=True)
    centroid_subscriber = rospy.Subscriber('/centroid', Int32, LineFollower)
    steering_pub = rospy.Publisher('steering', Float32, queue_size=1)
    throttle_pub = rospy.Publisher('throttle', Float32, queue_size=1)
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        steering_pub.publish(steering_float)
        throttle_pub.publish(throttle_float)
        rate.sleep()


if __name__ == '__main__':
    main()
