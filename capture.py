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
	parser.add_argument("-d", "--dir", help="the directory name where the data will be stored", type=str)
	parser.add_argument("-p", "--port", help="serial port name", type=str)
	#parser.add_argument("-s", "--show", default=False, help="show the camera feed")
	args = parser.parse_args()
	# assign port to arg, otherwise get the first available COM port
	if args.port is not None:
		port = args.port
	else:
		port = ports[0][0]

	with PiCamera() as camera:
		camera.resolution = (320,240)
		camera.framerate = args.fps
		rawCapture = PiRGBArray(camera, size=(320,240))
		print('Camera Started. Capturing @ %d fps' % args.fps)
		time.sleep(2)
		
		# make dirs
		if not os.path.exists('./' + args.dir):
			os.mkdir(args.dir)
		os.chdir('./' + args.dir)
		if not os.path.exists('./img'):
			os.mkdir('img')
		# make csv
		with open('capture_log.csv', 'wt') as csv_file:
			wr = csv.writer(csv_file, delimiter=',')
			wr.writerow(['img', 'throttle', 'steering'])
			# make serial connection
			with serial.Serial(port, BAUD_RATE, timeout=10) as ser:
				ser.flushOutput()
				ser.flushInput()
				# capture frames
				count = 0
				prev_time = time.time()
				fps = args.fps
				for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
					image = frame.array
					#if args.show:
					#	cv2.imshow('frame', image)
					img_path = './img/img{:04d}.jpeg'.format(count)
					ser.write(b'00000000')
					ser.flush()
					data = ser.readline().decode('utf-8')
					if data:
						cv2.imwrite(img_path, image)
						sp_data = data.strip().split(':')	
						print('Th: {0: <4} St: {1: <4} FPS: {2:2.2f}'.format(sp_data[0], sp_data[1], fps), end='\r')
						wr.writerow([img_path, sp_data[0], sp_data[1]])
						count += 1
					rawCapture.truncate(0)
					if (count + 1) % 10 == 0:
						fps = 10.0 / (time.time() - prev_time)
						prev_time = time.time()
						
		
if __name__ == '__main__':
	main()
