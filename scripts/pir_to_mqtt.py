#Import necessary modules and setting of the basic unit
import time
import datetime
import csv
from picamera import PiCamera
import cv2
import paho.mqtt.client as mqtt
import zero_settings

#When running print on console some informations about the script
print("""pir_to_mqtt.py - Detects movements in room and sends the detected
number of person in the room via MQTT to the Central Unit.
_______________________

Press Ctrl+C to exit!
_______________________
""")

#to check the connection to the broker is the variable connection set
connection=False

#MQTT functions
def on_connect(client, userdata, flags, rc):
    global connection
    if rc == 0:
        print("connected with result code " + str(rc));
        connection = True
    else:
        print("Error by connecting, check terminal")
        connection = False
    return (connection)


def on_disconnect(client, userdata, rc):
    global connection
    if rc != 0:
        print("Unexpected disconnection.")
        connection = False
        return (connection)

def on_publish(result, mid):
    if result == 0:
        print("pub")
    else:
        print("nopub")


#MQTT settings and main funciton
client = mqtt.Client()
client.username_pw_set(zero_settings.user, zero_settings.pwd)
client.connect(zero_settings.ip_root, 1883, 60)
client.on_connect = on_connect
client.on_disconnect = on_disconnect



# Initializing the HOG person detector
def detect_person():

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Reading the Image
    image = cv2.imread('/home/pi/IoT_Project/scripts/movement.jpg')
    scale=50
    height=min(400, image.shape[0]*scale/100)
    width=min(533, image.shape[1]*scale/100)
    dim=(width, height) #width=min(400, image.shape[1])

# Resizing the Image
    image = cv2.resize(image, dim,cv2.INTER_CUBIC)

# Detecting all the regions in the
# Image that has a pedestrians inside it
    (regions, _) = hog.detectMultiScale(image,winStride=(4, 4),padding=(8, 8),scale=1.05)

# Drawing the regions in the Image
    count_person=0
    for (x, y, w, h) in regions:
        count_person=count_person+1
        cv2.rectangle(image, (x, y),(x + w, y + h),(0, 0, 255), 2)

# Showing the output Image
    try:
        client.loop_start()
        client.publish("room" + zero_settings.room + "/pir/person", count_person)
        if connection==False:
            reconnect = client.reconnect()
            time.sleep(5);
        client.loop_stop()
    except Exception as e:
        print(e)
        time.sleep(5)
    cv2.destroyAllWindows()
    return()

##   PIR motion sensor  ###
camera = PiCamera()

#Camera should be mounted with cable on the top side, if mounted with cable on
#the bottom then set camera.rotation=0
camera.rotation=180
from grove.gpio import GPIO


def take_picture():
    camera.resolution = (1066, 800)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/IoT_Project/scripts/movement.jpg')
    camera.stop_preview()

class GroveMiniPIRMotionSensor(GPIO):
    def __init__(self, pin):
        super(GroveMiniPIRMotionSensor, self).__init__(pin, GPIO.IN)
        self._on_detect = None

    @property
    def on_detect(self):
        return self._on_detect

    @on_detect.setter
    def on_detect(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_detect = callback

    def _handle_event(self, pin, value):
        if value:
            if callable(self._on_detect):
                self._on_detect()

Grove = GroveMiniPIRMotionSensor

def main():
    import sys

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        sys.exit(1)

    pir = GroveMiniPIRMotionSensor(int(sys.argv[1]))

    def callback():
        global detected
        take_picture()
        time.sleep(1)
        detected=detect_person()
        time.sleep(2)

    pir.on_detect = callback

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
