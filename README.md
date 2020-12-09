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

## Dependencies

### [cv2](https://opencv.org/)

Description TBD

### [adafruit_servokit](https://circuitpython.readthedocs.io/projects/servokit/en/latest/)

Description TBD
## Structure

### Nodes

#### **throttle_client**

Associated file: throttle_client.py

Subscribes to [throttle](#topic_throttle) topic.

Uses the [adafruit_servokit](#adafruit_servokit) module on **channel 0** for converting high-level topic float to low-level PWM for ESC which controls motor.

#### **steering_client**

Associated file: steering_client.py

Subscribes to [steering](#topic_steering) topic.

Uses the [adafruit_servokit](#adafruit_servokit) module on **channel 1** for converting high-level topic float to low-level PWM for steering servo.

#### **camera_server**

Associated file: camera_server.py

Publishes to [camera_rgb](#topic_camera_rgb) topic.

Uses [cv2](#cv2) module to read USB camera frames at a fixed rate. Then converts cv2-format image to ROS-format image message for publishing using [cv_bridge](#cv_bridge) module.

#### **lane_detection_node**

Associated file: lane_detection.py

Subscribes to [camera_rgb](#topic_camera_rgb) topic.
Publishes to [centroid](#topic_centroid) topic.

#### **lane_guidance_node**

Associated file: lane_guidance.py

Subscribes to [centroid](#topic_centroid) topic.
Publishes to [throttle](#topic_thorttle) and [steering](#topic_steering) topics.

### Topics

| Name                                  | Msg Type                  | Info                                              |
| ------------------------------------- | --------------------- | ------------------------------------------------- |
| <a id="topic_throttle">throttle</a>   | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling throttle |
| <a id="topic_steering">steering</a>| std_msgs.msg.Float32  | Float value from -1 to 1 for controlling steering |
| camera_rgb                            | sensor_msgs.msg.Image | Image last read from USB camera |
| centroid                              | std_msgs.msg.Int32    | Integer for x coordinate of centroid in camera image space |
