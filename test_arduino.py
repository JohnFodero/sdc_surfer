import serial
import time

mode = 0
def main():
    port = '/dev/ttyACM0'
    baud_rate = 115200

    with serial.Serial(port, baud_rate, timeout=20) as ser:
	time.sleep(1)
        if mode == 0:
            # command the arduino to report esc and servo positions at ____ Hz
            ser.reset_input_buffer()
	    ser.write('00000005'.encode())
	    ser.flush()
	    mode_ret = ser.readline()
	    print("Mode: " + mode_ret)
	    delay_ret = ser.readline()
            print("Delay: " + str(delay_ret))
            while True:
		inc = time.time()
		incoming = ser.readline()
                print('{0:05f}->{1}'.format(time.time() - inc, incoming))
		
        elif mode == 1:
            # command esc and servo position
            ser.reset_input_buffer()
	    ser.write('11110000'.encode())
	    ser.flush()
            mode_ret = ser.readline()
	    print("Mode: " + mode_ret)
            while True:
                command = str(input('Enter command (8 bits)'))
                ser.write(command.encode())

                time.sleep(0.2)


if __name__ == '__main__':
    main()
