import serial
import time

mode = 0
def main():
    port = '/dev/ttyACM0'
    baud_rate = 115200

    with serial.Serial(port, baud_rate) as ser:
        if mode == 0:
            # command the arduino to report esc and servo positions at 20 Hz
            ser.write('11110020'.encode())
            while True:
                print(ser.read(8))
        elif mode == 1:
            # command esc and servo position
            ser.write('00000000'.encode())
            while True:
                command = str(input('Enter command (8 bits)'))
                ser.write(command.encode())

                time.sleep(0.2)


if __name__ == '__main__':
    main()
