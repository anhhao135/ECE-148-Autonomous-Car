import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import
#from move_robot import MoveCar


steering_float = Float32()
throttle_float = Float32()

class LineFollower(object):

	def __init__(self):

		self.bridge_object = CvBridge()
		self.image_sub = rospy.Subscriber("camera_rgb", Image, self.camera_callback)

	def camera_callback(self, data):

		try:
			# We select bgr8 because its the OpneCV encoding by default
			cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
		except CvBridgeError as e:
			print(e)
		height, width, channels = cv_image.shape

		descentre = 160
		rows_to_watch = 20
		cv_image = cv_image[(height) / 2 + descentre:(height) / 2 + (descentre + rows_to_watch)][1:width]

		original = cv_image.copy()
		hsv2 = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

		# creating mask
		lower_yellow = np.array([0, 0, 0])
		upper_yellow = np.array([0, 0, 255])

		mask_yellow = cv2.inRange(hsv2, lower_yellow, upper_yellow)
		res_yellow = cv2.bitwise_and(cv_image, cv_image, mask=mask_yellow)
		gray = cv2.cvtColor(res_yellow, cv2.COLOR_BGR2GRAY)
		(thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

		# switch to edges
		edges = cv2.Canny(blackAndWhiteImage, 50, 150, apertureSize=3)
		kernel = np.ones((3, 3), np.uint8)
		dilation = cv2.dilate(edges, kernel, iterations=3)

		kernel = np.ones((15, 15), np.float32) / 25
		blurred = cv2.filter2D(dilation, -1, kernel)

		ret, thresh = cv2.threshold(blurred, 127, 255, 0)

		# identify contours in image
		imgage, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		centers = []
		cx_list = []
		cy_list = []
		for pic, contour in enumerate(contours):
			x, y, w, h = cv2.boundingRect(contour)
			cv_image = cv2.rectangle(cv_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
			m = cv2.moments(contour)  # Se obtiene el centro de masa de los marcadores enconrados.
			cx = int(m['m10'] / m['m00'])
			cy = int(m['m01'] / m['m00'])
			centers.append([cx, cy])
			cx_list.append(int(m['m10'] / m['m00']))
			cy_list.append(int(m['m01'] / m['m00']))
			cv2.circle(cv_image, (cx, cy), 7, (0, 255, 0), -1)

		try:
			mid_x = int(0.5 * (cx_list[0] + cx_list[1]))
			mid_y = int(0.5 * (cy_list[0] + cy_list[1]))
			cv2.circle(cv_image, (mid_x, mid_y), 7, (255, 0, 0), -1)
		except:
			#mid_y, mid_x = height / 2, width / 2
			throttle_float.data = 0.0 #stop if cannot locate 2 lines

		# plotting results
		cv2.imshow("res_yellow", res_yellow)
		cv2.imshow("cv_image", cv_image)
		cv2.imshow("blurred", blurred)
		cv2.imshow("original", original)
		cv2.waitKey(1)

		error_x = mid_x - width / 2


        rospy.loginfo("mid_x = "+str(mid_x))
		

		throttle_float.data = 1.0 #constant throttle
		steering_float.data = -error_x / 100 #normalized steering float from -1 to 1

	def clean_up(self):
		cv2.destroyAllWindows()


def main():
	rospy.init_node('line_following_node', anonymous=True)

	line_follower_object = LineFollower()

	steering_pub = rospy.Publisher('steering', Float32, queue_size=1)
	throttle_pub = rospy.Publisher('throttle', Float32, queue_size=1) #set up publishers


	steering_pub.publish(steering_float)
	throttle_pub.publish(throttle_float)


	rate = rospy.Rate(5)
	ctrl_c = False

	def shutdownhook():
		# works better than the rospy.is_shut_down()
		line_follower_object.clean_up()
		rospy.loginfo("shutdown time!")
		ctrl_c = True

	rospy.on_shutdown(shutdownhook)

	while not ctrl_c:
		rate.sleep()


if __name__ == '__main__':
	main()
