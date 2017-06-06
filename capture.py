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
		with open('capture_log', 'wb') as csv_file:
			wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
			wr.writerow(mylist)
			# make serial connection
			with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
				print("connected")
				while True:
					# get latest input from arduino

					data = ser.read(9)
				# capture image

				# write row of data to csv
				# ['image_file_location', 'throttle', 'steering']

if __name__ == '__main__':
	main()
