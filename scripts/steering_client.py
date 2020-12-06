#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from adafruit_servokit import ServoKit
import json
import os

STEERING_NODE_NAME = 'steering_client'
STEERING_TOPIC_NAME = 'steering'

# more documentation at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# kit.servo[1].set_pulse_width_range(1000, 2000) ; use this to set the calibration min and max pwms, but by default its pretty spot on for our car

# steering servo is on channel 1


kit = ServoKit(channels = 16)

global straight, max_right, max_left

def callback(data): #called everytime topic is updated
    normalized_steering = data.data #this is a value between -1 and 1, with -1 being fully left and 1 being fully right
    rospy.loginfo(data.data) # just for debug
    if normalized_steering < 0:
        angle_delta =  -1*(max_left - straight) * normalized_steering #maps the left turn value from 0 to -1 to the max left value allowed for the kit.servo object
    elif normalized_steering == 0:
        angle_delta = 0
    else:
        angle_delta =  (max_right - straight) * normalized_steering #maps the left turn value from 0 to -1 to the max left value allowed for the kit.servo object
   
    kit.servo[1].angle = straight + angle_delta  # add that difference to 90 to find the absolute degree steering; 0 is full left, 1 is full right.

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node(STEERING_NODE_NAME, anonymous=True)
    rospy.Subscriber(STEERING_TOPIC_NAME, Float32, callback)
    rospy.spin()   # spin() simply keeps python from exiting until this node is stopped

def calibration_values(): #used to retrieve the calibrated max L/R and straight steering values
    parent_path = os.path.dirname(os.getcwd()) #this assumes the script will be run from the .../scripts directory with the json file located in a directory, one directory above
    json_path = os.path.join(parent_path, 'json_files', 'car_config.json')
    f = open(json_path,"r") #open the car configuration file to get the most recent steering calibration values
    data = json.load(f)
    straight = data['straight']
    max_right = data['max_right']
    max_left = data['max_left']

if __name__ == '__main__':
    calibration_values() #call calibration values first to load the appropriate steering calibration
    time.sleep(1) #pause 1s to allow the values to be loaded by the calibration_values function
    listener()
