import serial
import time
import urllib.request
# specify the port below (e.g., serial.Serial('com4')).
# to know which port we are using, go to the arduino, click Tools
arduinoData = serial.Serial('com4')

# url to download from
URL = 'http://127.0.0.1:5000/download'
t = 5 # delay time (in seconds)
while True:
    # download from url, save to command_info.txt
    urllib.request.urlretrieve(URL,'command_info.txt')
    # read line by line (the 3 angles) from the .txt
    file_object = open(r"command_info.txt", "r")
    for i, line in enumerate(file_object):
        angle = str(int(line))
        print(type(angle),angle)
        arduinoData.write(angle)

    time.sleep(5)
