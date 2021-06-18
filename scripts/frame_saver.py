#!/usr/bin/env python
import os
import sys
import time
import re
import socket
import rospy
import roslib
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

VERBOSE = False


class FrameSaver(object):

    def __init__(self, robot_host):
        """Configure subscriber."""
        # Create a subscriber with appropriate topic, custom message and name of
        # callback function.
        self.robot_host = robot_host
        self.sub = rospy.Subscriber(self.robot_host + '/raspicam/image/compressed', CompressedImage, self.callback, queue_size = 1)

        self.br = CvBridge()
        self.image = None
        self.data = None

        self.time = rospy.Time.now()
        
        self.i = 0
        self.name = "raspicam_node_%s_%s.jpg" % (self.time, self.i)

        # Initialize message variables.
        self.enable = False

        if self.enable:
            self.start()
        else:
            self.stop()

    def start(self):
        self.enable = True
        self.sub = rospy.Subscriber(self.robot_host + '/raspicam/image/compressed', CompressedImage, self.callback, queue_size = 1)

    def stop(self):
        """Turn off subscriber."""
        self.enable = False
        self.sub.unregister()
        cv2.destroyAllWindows()

    def callback(self, data):
        """Handle subscriber data."""
        # Simply print out values in our custom message.
        self.data = data

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(self.data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        #try:
        #    img = self.br.compressed_imgmsg_to_cv2(data, 'bgr8')
        #except CvBridgeError as e:
        #    print(e)
        
        cv2.imshow('cv_img', image_np)
        cv2.waitKey(25)

        self.i = self.i + 1
        self.name = "raspicam_node_%s_%s.jpg" % (self.time, self.i)

        msg = "Got frame %s" % (self.i)
        rospy.loginfo(rospy.get_caller_id() + msg)
        
        cv2.imwrite(self.name, image_np)
        
if __name__ == '__main__':
    # Initialize the node and name it.
    node_name = re.sub("-", "_", socket.gethostname()) + "_Raspicam_FrameSaver"
    rospy.init_node(node_name, anonymous=False)
    
    image = FrameSaver("robotcar")
    
    # Go to the main loop
    try:
        image.start()
        # Wait for messages on topic, go to callback function when new messages arrive.
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()
    # Stop with Ctrl + C
    except KeyboardInterrupt:
        image.stop()

        nodes = os.popen("rosnode list").readlines()
        for i in range(len(nodes)):
            nodes[i] = nodes[i].replace("\n","")

        for node in nodes:
            os.system("rosnode kill " + node_name)

        
        print("Node stopped")
    cv2.destroyAllWindows()
