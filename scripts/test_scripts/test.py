import numpy as np
import cv2

cap = cv2.VideoCapture(0)

start_height = 325
crop_height = 275


p = 0.6

relative_offset = 0
print("hello")

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()


	width = len(frame[1])
	height = len(frame[0])

	frame = cv2.GaussianBlur(frame, (5,5), 0)



	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	'''
	


	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


	frame = cv2.inRange(frame, (10, 0,100), (30,60,200))








	'''

	

	ret, frame = cv2.threshold(frame, 140, 255, cv2.THRESH_BINARY_INV)

	frame = np.invert(frame)



	try:

		M = cv2.moments(frame)

		# calculate x,y coordinate of center
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		print(cX/width)

		cX = cX + relative_offset

		# put text and highlight the center
		cv2.circle(frame, (cX, cY), 5, (0, 255, 255), -1)
	except:
		pass

	# Our operations on the frame come here

	# Display the resulting frame
	cv2.imshow("cv_image", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
