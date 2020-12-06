#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit
import json
import os

THROTTLE_NODE_NAME = 'throttle_client'
THROTTLE_TOPIC_NAME = 'throttle'

# more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython

# throttle servo is on channel 0

kit = ServoKit(channels=16)

global max_throttle, neutral_throttle, reverse

throttle_scale = 0.2  # scale down sensitive throttle


def callback(data): #called everytime topic is updated
    rospy.loginfo(data.data) # just for debug
    normalized_throttle = data.data
    if normalized_throttle < 0:
        throttle_delta = 0 #value currently set to make the car go into neutral when the car wants to break. Replace with this to mess with the "reverse throttle":
                           # -1 * (reverse - neutral_throttle) * normalized_throttle  # maps the left turn value from 0 to -1 to the max left value allowed for the kit.servo object
    elif normalized_throttle == 0:
        throttle_delta = 0
    else:
        throttle_delta = (max_throttle - neutral_throttle) * normalized_throttle  # maps the left turn value from 0 to -1 to the max left value allowed for the kit.servo object

    kit.continuous_servo[0].throttle = (neutral_throttle + throttle_delta) * throttle_scale # throttle takes values from -1 to 1; this is very sensitive so keep it below 0.2

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
    max_throttle = data['max_throttle']
    neutral_throttle = data['neutral_throttle']
    reverse = data['reverse']

if __name__ == '__main__':
    calibration_values() #call calibration values first to load the values into the throttle client
    time.sleep(1) #pause 1s to allow the values to be loaded by the calibration_values function
    listener()
