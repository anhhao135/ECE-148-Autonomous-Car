import numpy as np
import cv2
from simple_pid import PID


pid = PID(1, 0.1, 0.05, setpoint=0)
pid.output_limits = (-1, 1)

cap = cv2.VideoCapture("test.mov")


crop_height = 300

print("hello")

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()



    width = len(frame[1])
    height = len(frame[0]) - crop_height

    frame = frame[crop_height:height, 0:width]
    frame_color = frame

    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    '''



    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    frame = cv2.inRange(frame, (10, 0,100), (30,60,200))








    '''

    ret, frame = cv2.threshold(frame, 210, 255, cv2.THRESH_BINARY_INV)

    frame = np.invert(frame)

    try:

        M = cv2.moments(frame)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # put text and highlight the center
        cv2.circle(frame_color, (cX, cY), 5, (0, 255, 255), -1)
    except:
        pass

    # Our operations on the frame come here
    #print(0.5 - cX / width)
    print(pid(0.5 - cX / width))
    # Display the resulting frame
    cv2.imshow("cv_image", frame_color)
    cv2.imshow("thresh", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
