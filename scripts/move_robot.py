import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class MoveCar(object):

    def __init__(self):
    
        self.steering_pub = rospy.Publisher('steering', Float32, queue_size=10)
        self.last_steering_command = Float32()
        self._steering_pub_rate = rospy.Rate(10)
        self.throttle_pub = rospy.Publisher('throttle', Float32, queue_size=10)
        self.last_throttle_command = Float32()
        self._throttle_pub_rate = rospy.Rate(10)
        self.shutdown_detected = False

    def move_robot(self, Float32_object):
        self.steering_pub.publish(Float32_object)
        self.throttle_pub.publish(Float32_object)
                                    
    def clean_class(self):
        # Stop Robot
        Float32_object = Float32()
        Float32_object.angular.z = 0.0
        self.move_robot(Float32_object)
        self.shutdown_detected = True

def main():
    rospy.init_node('move_robot_node', anonymous=True)
    MoveCar_object = MoveCar()
    Float32_object = Float32()
    # Make it start turning
    Float32_object.angular.z = 0.5
    rate = rospy.Rate(5)
    ctrl_c = False

    def shutdownhook():
        # works better than the rospy.is_shut_down()
        MoveCar_object.clean_class()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        MoveCar_object.move_robot(Float32_object)
        rate.sleep()
    

if __name__ == '__main__':
    main()