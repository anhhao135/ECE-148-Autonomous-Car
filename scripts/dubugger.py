import rospy # Import the Python library for ROS
from std_msgs.msg import Float32 # Import the Int32 message from the std_msgs package
 
def callback(msg): # Define a function called 'callback' that receives a parameter named 'msg'
  print msg.data # Print the value 'data' inside the 'msg' parameter
 
rospy.init_node('debug_subscriber') # Initiate a Node called 'debug_subscriber'
 
sub = rospy.Subscriber('debug', Float32, callback) # Create a Subscriber object that will listen to the /counter topic and will call the 'callback' function each time it reads something from the topic
 
rospy.spin() # Create a loop that will keep the program in execution