#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
 
# Define a function called 'callback' that receives a parameter named 'msg'
def callback(msg):
  # Print the value 'data' inside the 'msg' parameter
  print(msg.data)
 
# Initiate a Node called 'debug_subscriber'
rospy.init_node('debug_subscriber')
 
# Create a Subscriber object that will listen to the /counter topic and will call the 'callback' function each time it reads something from the topic
sub = rospy.Subscriber('debug', Float32, callback)
 
# Create a loop that will keep the program in execution
rospy.spin()
