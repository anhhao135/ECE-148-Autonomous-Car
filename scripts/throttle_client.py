#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit
import os
import json
import time

THROTTLE_NODE_NAME = 'throttle_client'
THROTTLE_TOPIC_NAME = 'throttle'

# more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

# throttle servo is on channel 0

kit = ServoKit(channels=16)

throttle_scale = 1.0  # scale down sensitive throttle
#throttle_test = 0.098
#throttle_test = 0.255


def callback(data):  # called everytime topic is updated
    rospy.loginfo(data.data)  # just for debug
    # throttle takes values from -1 to 1; this is very sensitive so keep it below 0.2
    kit.continuous_servo[0].throttle = data.data * throttle_scale
    #kit.continuous_servo[0].throttle = throttle_test
    #print(throttle_test)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node(THROTTLE_NODE_NAME, anonymous=True)
    rospy.Subscriber(THROTTLE_TOPIC_NAME, Float32, callback)
    rospy.spin()   # spin() simply keeps python from exiting until this node is stopped

def calibration_values(): #used to retrieve the calibrated throttle values
    parent_path = os.path.dirname(os.getcwd()) #this assumes the script will be run from the .../scripts directory with the json file located in a directory, one directory above
    json_path = os.path.join(parent_path, 'json_files', 'car_config.json')
    f = open(json_path,"r") #open the car configuration file to get the most recent steering calibration values
    data = json.load(f)
    #assign the throttle values to be used by the throttle client script
    global max_throttle, neutral_throttle, reverse
    max_throttle = data['max_throttle']
    neutral_throttle = data['neutral_throttle']
    #reverse = data['reverse'] #This functionalist is unused as of 12/11/2020
    print(max_throttle)
if __name__ == '__main__':
    calibration_values() #call calibration values first to load the values into the throttle client
    time.sleep(1) #pause 1s to allow the values to be loaded by the calibration_values function
    listener()
