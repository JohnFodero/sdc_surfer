from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640,480))

time.sleep(0.1)
count = 1
for frame in camera.capture_continuous(rawCapture, format='rgb', use_video_port=True):
	image = frame.array
	cv2.imshow('frame', image)
	key = cv2.waitKey(1) & 0xFF
	cv2.imwrite('img{0}.jpeg'.format(count), image)
	rawCapture.truncate(0)
	if key == ord('q'):
		break
	count += 1
