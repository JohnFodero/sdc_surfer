import os
from time import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import serial
import serial.tools.list_ports
import csv
import cv2
import numpy as np
from keras.models import load_model
from keras.models import Model

BAUD_RATE = 115200
RESOLUTION = (320, 240)
THROTTLE = 1
speed = THROTTLE

def signal_handler(signal, frame):
    # allows for clean interrupt of main control loop
    global interrupted
    interrupted = True
signal.signal(signal.SIGINT, signal_handler)
interrupted = False

def main():
    
    
    parser - argparse.ArgumentParser()
    parser.add_argument("-f", "--fps", type=int, default=10, help="image capture rate")
    parser.add_argument("-p", "--port", type=str, help="serial port name")
    parser.add_argument("-m", "--model", type=str, default="./models/model.hdf5", help="path to model")
    args = parser.parse_args()
    
    ports = list(serial.tools.list_ports.comports())
    if args.port is not None:
        port = args.port
    else:
        port = ports[0][0]
    
    # load model
    model = load_model(args.model)
    # start camera
    with PiCamera() as camera:
        camera.resolution = RESOLUION
        camera.framerate = args.fps
        rawCapture = PiRGBArray(camera, size=RESOLUTION)
        
        # open serial connection
        with serial.Serial(port, BAUD_RATE, timeout=10, rtscts=0) as ser:
            ser.setDTR(False)
            time.sleep(1)
            ser.flushInput()
            ser.setDTR(True)
            ser.flushOutput()
            ser.write(b'11111111')
            ser.flush()
            confirm = ser.readline().decode()
            if confirm != '11111111':
                print('Serial connection error. Terminating.')
                return        
            
            count = 0
            start_time = time()
            fps = args.fps
            for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
                image = np.reshape(frame.array, (1, RESOLUTION[0], RESOLUTION[1], 3))
                st_angle = model.predict(image)
                # map the steering angle
                #MAP
                print(st_angle)
                ser.write('{:4d}{:4d}'.format(speed, st_angle).encode())
                ser.flush()
                if ser.readline().decode() != '1':
                    print('Serial error')
                    # abort?
                if (count + 1) % 10 == 0:
                    fps = 10.0 / (time() - start_time)
                    start_time = time()
                print('Th: {0:4d} St: {1:4d} FPS: {2:2.2f}'.format(speed, st_angle, fps), end='\r')
                count += 1
                rawCapture.truncate(0)
                if interrupted:
                    print('\n\nExiting')
                    break
                    
# - - - - - - - - - - - - - - - - 

if __name__ == '__main__':
    main()