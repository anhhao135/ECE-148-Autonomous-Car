# potatoInside

A ROS package using openCV on an RC car to do autonomous laps around a track using a line following algorithm

## Table of Contents

- [potatoInside](#potatoinside)
  - [Table of Contents](#table-of-contents)
  - [Dependencies](#dependencies)
    - [cv2](#cv2)
    - [adafruit_servokit](#adafruit_servokit)
  - [Structure](#structure)
    - [Nodes](#nodes)
      - [**throttle_client**](#throttle_client)
      - [**steering_client**](#steering_client)
      - [**camera_server**](#camera_server)
      - [**(line detection node)**](#line-detection-node)
      - [**(line following node)**](#line-following-node)
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

Subscribe to [throttle](#topic_throttle) topic, uses the
[adafruit_servokit](#adafruit_servokit) module on **channel 0** for sending
signals to the servo.

#### **steering_client**

Associated file: steering_client.py

Subscribe to [steering](#topic_steering) topic, uses the
[adafruit_servokit](#adafruit_servokit) module on **channel 1** for sending
signals to the servo.

#### **camera_server**

Associated file: camera_server.py

TODO

#### **lane_detection_node**

Associated file: lane_detection.py

TODO

#### **lane_guidance_node**

Associated file: lane_guidance.py

TODO

### Topics

| Name                                  | Msg Type                  | Info                                              |
| ------------------------------------- | --------------------- | ------------------------------------------------- |
| <a id="topic_throttle"></a> throttle  | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling throttle |
| <a name="topic_throttle"></a>steering | std_msgs.msg.Float32  | Float value from -1 to 1 for controlling steering |
| camera_rgb                            | sensor_msgs.msg.Image | Image last read from USB camera |
| centroid                              | std_msgs.msg.Int32    | Integer for x coordinate of centroid in camera image space |
