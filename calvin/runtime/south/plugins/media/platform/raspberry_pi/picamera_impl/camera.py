# -*- coding: utf-8 -*-

# Copyright (c) 2016 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import cv2
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

from io import BytesIO

width = 100
height = 100

class Camera(object):

    """
    Capture image from device
    """

    def __init__(self, device, width, height):
        """
        Initialize camera
        """
	print "initialize picamera"
#        self.cap = cv2.VideoCapture(device)
#        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
#        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
	self.camera = PiCamera()
#	self.camera.resolution = (width, height)
	#allow the camera to warm up
	time.sleep(0.1)

    def get_image(self):
        """
        Captures an image
        returns: Image as jpeg encoded binary string, None if no frame
        """
	print "Hakan, taking picture"
	rawCapture = PiRGBArray(self.camera)
	self.camera.capture(rawCapture, format="bgr")
        frame = rawCapture.array
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),50]
        ret, jpeg = cv2.imencode(".jpg", frame, encode_param)
        if ret:
            data = numpy.array(jpeg)
            return data.tostring()

#        my_stream = BytesIO()
#	self.camera.capture(my_stream, 'jpeg')
#        data = numpy.array(my_stream)
#        return data.tostring()

    def close(self):
        """
        Uninitialize camera
        """
        self.cap.release()
