#!/usr/bin/env python

def decodeImage(data, height, width): #function to replace self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
    decoded = np.fromstring(data, dtype=np.uint8)
    decoded = decoded.reshape((height, width, 3))
    return decoded
