#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit

#more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# kit.servo[1].set_pulse_width_range(1000, 2000) ; use this to set the calibration min and max pwms, but by default its pretty spot on for our car


kit = ServoKit(channels = 16)


def callback(data): #called everytime topic is updated
    rospy.loginfo(data.data) # just for debug
    kit.servo[1].angle = 180 * data.data #data.data is a float from 0 - 1; it is a normalized scale of the full 180 range of the servo


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('steering_client', anonymous=True)
    rospy.Subscriber("steering", Float32, callback)
    rospy.spin()   # spin() simply keeps python from exiting until this node is stopped



if __name__ == '__main__':
    listener()