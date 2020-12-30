# raspicam_node_saver


Gives an example how you can use the [raspicam_node](https://github.com/Michdo93/raspicam_node/) for saving the video broadcast as video or image frames. The [raspicam_node](https://github.com/Michdo93/raspicam_node/) are used from the [RobotCar](https://github.com/Michdo93/robotcar). At first you have to make sure that the roscore is running and the [robotcar-pkg](https://github.com/Michdo93/robotcar-pkg) is publishing the sensor informations.

The String variable `robot_host` uses the hostname of one RobotCar. As example it could be `robotcar`.

A raspicam_node video or its image frames could be used as for training a neuronal network which could be used as informations for an ADAS.

The [raspicam_node](https://github.com/Michdo93/raspicam_node/) is forked from here: https://github.com/UbiquityRobotics/raspicam_node

ROS node for the Raspberry Pi Camera Module. Works with both the V1.x and V2.x versions of the module. We recommend using the v2.x cameras as they have better auto gain, and the general image quality is better.

Available for ROS Melodic on Raspbian Buster.

You can use it on different ROS robots in the same network. It will seperate the robots by its hostname. So please make sure, that the robots have different hostnames.

You can subscribe as example from `/<hostname>/raspicam/image/compressed` instead of `/raspicam_node/image/compressed`.

If you use the original [raspicam_node](https://github.com/UbiquityRobotics/raspicam_node) which will not seperate robots by its hostname, the String variable `robot_host` could be empty and raspicam should change to raspicam_node again.


## Raspicam_FrameSaver Node

It subscribes the compressed image informations from the [raspicam_node](https://github.com/Michdo93/raspicam_node) respectively the raspicam and save its content as jpeg image frames.

|                 Topic Address                |            Message Type       |
|--------------------------------------------- | ------------------------------|
|robot_host + /raspicam/image/compressed       | [sensor_msgs/CompressedImage](http://docs.ros.org/en/api/sensor_msgs/html/msg/CompressedImage.html)  |

You can run it with `rosrun raspicam_node_saver frame_saver.py`


## Raspicam_VideoSaver Node

It subscribes the compressed image informations from the [raspicam_node](https://github.com/Michdo93/raspicam_node) respectively the raspicam and save its content as avi video.

|                 Topic Address                |            Message Type       |
|--------------------------------------------- | ------------------------------|
|robot_host + /raspicam/image/compressed       | [sensor_msgs/CompressedImage](http://docs.ros.org/en/api/sensor_msgs/html/msg/CompressedImage.html)  |

You can run it with `rosrun raspicam_node_saver video_saver.py`
