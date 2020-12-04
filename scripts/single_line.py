mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

minV = 30
        maxV = 100
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)

try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
        except ZeroDivisionError:
            cy, cx = height/2, width/2

cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)