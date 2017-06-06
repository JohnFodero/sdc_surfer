import os
import time
import picamera
import argparse
import serial
import serial.tools.list_ports
import csv

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
		camera.resolution = (1024, 768)
		time.sleep(2)
		print("Capturing rate: " + str(args.capture_rate) + " Hz")
		if not os.path.exists('./' + args.dir):
			os.mkdir(args.dir)
		os.chdir('./' + args.dir)
		if not os.path.exists('./img'):
			os.mkdir('img')

#		camera.capture('test.jpg')

		# make csv
		with open('capture_log.csv', 'wb') as csv_file:
			wr = csv.writer(csv_file, delimiter=',')
			wr.writerow(['img', 'throttle', 'steering'])
			# make serial connection
			with serial.Serial(port, BAUD_RATE, timeout=10) as ser:
				print("connected")
				time.sleep(1)
				init_capture_cmd = '0000{0:04d}'.format(args.capture_rate)
				ser.reset_input_buffer()
				ser.write(init_capture_cmd.encode())
				ser.flush()
				mode_check = ser.readline()
				delay_check = ser.readline()
				print("Verify: " + mode_check + " " + str(delay_check))
				img_count = 1
				while True:
					# get latest input from arduino

					data = ser.readline()
					print(data)
					throttle = data[0:4]
					steering = data[5:9]
					img_name = './img/{0}_{1:05d}.jpg'.format(args.dir, img_count)
					# capture image
					camera.capture(img_name)
					# write row of data to csv
					# ['image_file', 'throttle', 'steering']
					wr.writerow([img_name, throttle, steering])
					img_count += 1

if __name__ == '__main__':
	main()
