#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit

#more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

#throttle servo is on channel 0



kit = ServoKit(channels = 16)


def callback(data): #called everytime topic is updated
    rospy.loginfo(data.data) # just for debug
    kit.servo[0].angle = data.data # throttle takes values from -1 to 1; this is very sensitive so keep it below 0.2


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('throttle_client', anonymous=True)
    rospy.Subscriber("throttle", Float32, callback)
    rospy.spin()   # spin() simply keeps python from exiting until this node is stopped



if __name__ == '__main__':
    listener()