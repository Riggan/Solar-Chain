import serial # you need to install the pySerial :pyserial.sourceforge.net
import time
# your Serial port should be different!
arduino = serial.Serial('COM5', 90000)



def onOffFunction():
    command = 'on'
    if command == 'on':
    	print("The LED is on...")
    	time.sleep(1)
    	arduino.write(True)
    	onOffFunction()
    elif command =="off":
    	print("The LED is off...")
    	time.sleep(1)
    	arduino.write(False)
    	onOffFunction()
    elif command =="bye":
    	print("See You!...")
    	time.sleep(1)
    	arduino.close()
    else:
    	print("Sorry..type another thing..!")
    	onOffFunction()

    time.sleep(2) #waiting the initialization...

onOffFunction()
