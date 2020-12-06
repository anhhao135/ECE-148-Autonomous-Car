#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit

THROTTLE_NODE_NAME = 'throttle_client'
THROTTLE_SUBSCRIBER_NAME = 'throttle'

# more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

# throttle servo is on channel 0

kit = ServoKit(channels=16)

throttle_scale = 0.2  # scale down sensitive throttle


def callback(data):  # called everytime topic is updated
    rospy.loginfo(data.data)  # just for debug
    # throttle takes values from -1 to 1; this is very sensitive so keep it below 0.2
    kit.continuous_servo[0].throttle = data.data * throttle_scale


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node(THROTTLE_NODE_NAME, anonymous=True)
    rospy.Subscriber(THROTTLE_SUBSCRIBER_NAME, Float32, callback)
    rospy.spin()   # spin() simply keeps python from exiting until this node is stopped


if __name__ == '__main__':
    listener()
