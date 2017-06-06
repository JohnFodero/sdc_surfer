import os
import time
import picamera
import argparse
import serial
import serial.tools.list_ports
import csv
import io
import cv2
def main():
	BAUD_RATE = 115200
	# argparse assignments
	# directory name
	# rate
	# port
	ports = list(serial.tools.list_ports.comports())
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--capture_rate", type=int, default=10, help="rate [Hz] at which images are captured")
	parser.add_argument("-d", "--dir", help="the directory name where the data will be stored", type=str)
	parser.add_argument("-p", "--port", help="port name", type=str)
	args = parser.parse_args()
	if args.port is not None:
		port = args.port
	else:
		port = ports[0][0]

	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		#camera.framerate = 80
		#camera.start_preview()
		time.sleep(2)
		print("Capturing rate: " + str(args.capture_rate) + " Hz")
		if not os.path.exists('./' + args.dir):
			os.mkdir(args.dir)
		os.chdir('./' + args.dir)
		if not os.path.exists('./img'):
			os.mkdir('img')
		# make csv
		with open('capture_log.csv', 'wb') as csv_file:
			wr = csv.writer(csv_file, delimiter=',')
			wr.writerow(['img', 'throttle', 'steering'])
			# make serial connection
			rawCapture = picamera.array.PiRGBArray(camera)
			time.sleep(1)
			camera.capture(rawCapture, format="bgr")
			image = rawCapture.array

"""			with serial.Serial(port, BAUD_RATE, timeout=10) as ser:
				print("connected")
				time.sleep(1)
				ser.reset_input_buffer()
				ser.reset_output_buffer()
				prev_time = time.time()
				count = 1
				stream = io.BytesIO()
				outputs = [io.BytesIO() for i in range(40)]
				start = time.time()
				camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
				finish = time.time()
				print('Captured 40 images at %2.ffps' % (40 / (finish - start)))
"""
'''				while True:
					# get latest input from arduino
					ser.write('00000000'.encode())
					ser.flush()
					data = ser.readline().strip()
					# print(data)
					sp_data = data.split(':')
					img_name = './img/{0}_{1:05d}.png'.format(args.dir, img_count)
					# capture image
					camera.capture(img_name)
					# write row of data to csv
					# ['image_file', 'throttle', 'steering']
			#		wr.writerow([img_name, sp_data[0], sp_data[1]])
					img_count += 1
					if img_count % 10 == 0:
						print("Loop time for 10 images: " + str(time.time() - prev_time))
						prev_time = time.time()
'''
if __name__ == '__main__':
	main()
