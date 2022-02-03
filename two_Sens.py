# This is the code to run the MLX90614 Infrared Thermal Sensor
# You'll need to import the package "Adafruit Blinka"
# You'll need to import the package "adafruit-circuitpython-mlx90614/"
# You'll need to enable i2c on the pi https://pimylifeup.com/raspberry-pi-i2c/
# Reboot after enabling i2C
# Sensor is connected to 3.3V, GND and the i2C pins 3(SDA) and 5(SCL)
import pyrebase
import board
import busio as io
import adafruit_mlx90614
import serial
import time
import string
import pynmea2


from time import sleep

firebaseConfig = {
  "apiKey": "AIzaSyBi496FjKADa2pJ9EiUm3uVAogzml0gJHM",
  "authDomain": "text-to-cloud.firebaseapp.com",
  "databaseURL": "https://text-to-cloud-default-rtdb.firebaseio.com",
  "projectId": "text-to-cloud",
  "storageBucket": "text-to-cloud.appspot.com",
  "messagingSenderId": "1015634844431",
  "appId": "1:1015634844431:web:841b5cdb27480066643c7a",
  "measurementId": "G-XHN3407DQN"
}
firebase=pyrebase.initialize_app(firebaseConfig)



i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

while True:

    ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
    targetTemp = "{:.2f}".format(mlx.object_temperature)

    sleep(1)

    print("Ambient Temperature:", ambientTemp, "°C")
    print("Target Temperature:", targetTemp,"°C")
    BPM=[]
    for i in range (90,110,2):
        BPM.append(i)
#         BPM[5]=115
#         BPM[8]=80
#         BPM[4]=93
#         BPM[1]=97
    print(BPM)

    while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline()

        newdata=str(newdata,'utf-8','ignore')
    #     print(newdata)

        while newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            print(newmsg)
    #         break
        db=firebase.database()
        data =  { 'Temperature': ambientTemp,
              'ambient T': targetTemp,
              'gps':newmsg,
              'BPM':BPM
              }
        db.child("Reading").update(data)
    #         break
    #             lat=newmsg.latitude
    #             lng=newmsg.longitude
    #             gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
    #             print(gps)
    #           


