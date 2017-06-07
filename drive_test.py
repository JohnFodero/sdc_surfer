import os
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import serial
import serial.tools.list_ports
import csv
import cv2

def main():
	BAUD_RATE = 115200
	# argparse assignments
	# directory name
	# rate
	# port
	ports = list(serial.tools.list_ports.comports())
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--fps", type=int, default=10, help="image capture rate")
	parser.add_argument("-p", "--port", help="serial port name", type=str)
	args = parser.parse_args()
	# assign port to arg, otherwise get the first available COM port
	if args.port is not None:
		port = args.port
	else:
		port = ports[0][0]
        # start camera
	with PiCamera() as camera:
		camera.resolution = (320,240)
		camera.framerate = args.fps
		rawCapture = PiRGBArray(camera, size=(320,240))
		time.sleep(2)
		# make serial connection
		with serial.Serial(port, BAUD_RATE, timeout=10, rtscts=0) as ser:
			ser.setDTR(False)
			time.sleep(1)
			ser.flushInput()
			ser.setDTR(True)

			ser.flushOutput()
			ser.flushInput()
			# capture frames
			count = 0
			ser.write(b'11111111')
			ser.flush()
			confirm = ser.readline().decode('utf-8')
			print('Confirm: ' + confirm)
			for i in range(5):
				ser.write(b'15001600')
				ser.flush()
				conf = ser.readline().decode()
				print(conf)
				time.sleep(0.5)
				ser.write(b'15001400')
				ser.flush()
				conf = ser.readline().decode()
				print(conf)
				time.sleep(0.5)
			"""
			for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
				image = frame.array
				ser.write(b'00000000')
				ser.flush()
				if data:
					cv2.imwrite(img_path, image)
					print(data)
					sp_data = data.strip().split(':')	
					wr.writerow([img_path, sp_data[0], sp_data[1]])
					count += 1
				rawCapture.truncate(0)
			"""		
		
if __name__ == '__main__':
	main()
