# potatoInside

A ROS package using openCV on an RC car to do autonomous laps around a track using a line following algorithm

## Table of Contents

- [potatoInside](#potatoinside)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
    - [cv2](#cv2)
    - [adafruit_servokit](#adafruit_servokit)
    - [cv_bridge](#cv_bridge)
    - [simple-pid](#simple-pid)
  - [Structure](#structure)
    - [Nodes](#nodes)
      - [**throttle_client**](#throttle_client)
      - [**steering_client**](#steering_client)
      - [**camera_server**](#camera_server)
      - [**lane_detection_node**](#lane_detection_node)
      - [**lane_guidance_node**](#lane_guidance_node)
  - [Topics](#topics)
  - [Issues and Fixes](#issues-and-fixes)

## Wiring Schematic

![Wiring schematic](schematic.png "Wiring Schematic")

## Dependencies

### [cv2](https://opencv.org/)

Description TBD

### [adafruit_servokit](https://circuitpython.readthedocs.io/projects/servokit/en/latest/)


### [cv_bridge](http://wiki.ros.org/cv_bridge)

Description TBD

### [simple-pid](https://pypi.org/project/simple-pid/)

Description TBD

## Structure

### Nodes

#### **throttle_client**

Associated file: throttle_client.py

This node subscribes to the [throttle](#Topics) topic. We use subscriber callback function
to validate and normalize throttle value, and then use the [adafruit_servokit](#adafruit_servokit)
module on **channel 0** for sending signals to the hardware.

This node is also responsible for reading and setting the throttle calibration values.

#### **steering_client**

Associated file: steering_client.py

Similar to [throttle_client](#throttle_client), this node subscribes to the [steering](#Topics)
topic and pass the singals to the hardware.

#### **camera_server**

Associated file: camera_server.py

This node simply reads from the camera with cv2's interface and publish the image to the
[camera_rgb](#Topics) topic.

#### **lane_detection_node**

Associated file: lane_detection.py

In this node, we read from [camera_rgb](#Topics) topic and use opencv to identify line
information from the image, and publish the information of the middle point between
all identified lines to the [centroid](#Topics) topic.

#### **lane_guidance_node**

Associated file: lane_guidance.py

This node subscribes to the [centroid](#Topics) topic, calculates the throttle and steering
based on the centroid value, and then publish them to their corresponding topics.

## Topics

| Name       | Msg Type              | Info                                                       |
| ---------- | --------------------- | ---------------------------------------------------------- |
| throttle   | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling throttle          |
| steering   | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling steering          |
| camera_rgb | sensor_msgs.msg.Image | Image last read from USB camera image                      |
| centroid   | std_msgs.msg.Int32    | Integer for x coordinate of centroid in camera image space |

## Issues and Fixes


