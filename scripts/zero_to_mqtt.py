#import necessary modules and setting files
import csv
import datetime
import time
import paho.mqtt.client as mqtt
import zero_settings
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont

#when running print on console
print("""Running
_______________________

Press Ctrl+C to exit!
_______________________
""")

# MQTT Transmission set up
connection = False


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


client = mqtt.Client()
client.username_pw_set(zero_settings.user, zero_settings.pwd)
client.connect(zero_settings.ip_root, 1883, 60)
client.on_connect = on_connect
client.on_disconnect = on_disconnect


# Prepare local log file
def date_now():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today = str(today)
    return (today)


def time_now():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    now = str(now)
    return (now)


def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
    with open('/home/pi/IoT_Project/log/log_zero.csv', mode='a')as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([date_now(), time_now(), enviro_script.enviro_get_temperature(),
                                              enviro_script.enviro_get_humidity(), enviro_script.enviro_get_pressure(),
                                              enviro_script.enviro_get_luminosity(), enviro_script.enviro_get_proximity(),
                                              enviro_script.enviro_get_reducing(), enviro_script.enviro_get_oxidising(),
                                              enviro_script.enviro_get_nh3(), enviro_script.enviro_get_pm1(),
                                              enviro_script.enviro_get_pm2_5(), enviro_script.enviro_get_pm10(),
                                              sgp30_script.sgp30_get_voc(), sgp30_script.sgp30_get_eco2(), scd30_script.read_data()])
        return (write_to_log)


# LCD Set Up
import ST7735

disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=90,
    spi_speed_hz=10000000
)

# Initialize display
disp.begin()
time_send = str(0)


# Display Raspberry Pi serial and Wi-Fi status on LCD
def display_status(status, status_expl):
    global connection
    global time_send
    text_colour = (255, 255, 255)
    back_colour = (0, 170, 170)
    if connection:
        time_send = time_now()
    message = ("In room " + zero_settings.room + status + '\n' + status_expl + '\n last send:' + time_send)
    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    size_x, size_y = draw.textsize(message, font)
    x = (WIDTH - size_x) / 2
    y = (HEIGHT / 2) - (size_y / 2)
    draw.rectangle((0, 0, 160, 80), back_colour)
    draw.text((x, y), message, font=font, fill=text_colour)
    disp.display(img)


# Width and height to calculate text position
WIDTH = disp.width
HEIGHT = disp.height

# Text settings
font_size = 16
font = ImageFont.truetype(UserFont, font_size)

# MQTT topic path setting
client.enable_logger(logger=None)
path_enviro = str("room" + zero_settings.room + "/enviro/")
path_sgp30 = str("room" + zero_settings.room + "/sgp30/")

#Import necessery module as defined in the setting script
if zero_settings.enviro:
        import enviro_script

if zero_settings.sgp30:
        import sgp30_script
if zero_settings.scd30:
        from scd30_i2c import SCD30

        scd30 = SCD30()

        scd30.set_measurement_interval(2)
        scd30.start_periodic_measurement()

        time.sleep(2)

        def read_data():
            if scd30.get_data_ready():
                m = scd30.read_measurement()
            if m is not None:
                client.publish("room" + zero_settings.room + "/scd30/co2", m[0]);
                client.publish("room" + zero_settings.room + "/scd30/temperature", m[1]);
                client.publish("room" + zero_settings.room + "/scd30/humidity", m[2]);
            else:
                time.sleep(0.2)

#function that sends MQTT messages
def send_messages():
    if zero_settings.enviro:
        client.publish(path_enviro+"temperature", (enviro_script.enviro_get_temperature()), qos=1, retain=False)
        client.publish(path_enviro+"humidity", enviro_script.enviro_get_humidity(), qos=1, retain=False)
        client.publish(path_enviro+"pressure", enviro_script.enviro_get_pressure(), qos=1, retain=False)
        client.publish(path_enviro+"luminosity", enviro_script.enviro_get_luminosity(), qos=1, retain=False)
        client.publish(path_enviro+"proximity", enviro_script.enviro_get_proximity(), qos=1, retain=False)
        client.publish(path_enviro+"reducing", enviro_script.enviro_get_reducing(), qos=1, retain=False)
        client.publish(path_enviro+"oxidising", enviro_script.enviro_get_oxidising(), qos=1, retain=False)
        client.publish(path_enviro+"nh3", enviro_script.enviro_get_nh3(), qos=1, retain=False)
        client.publish(path_enviro+"pm1", enviro_script.enviro_get_pm1(), qos=1, retain=False)
        client.publish(path_enviro+"pm2_5", enviro_script.enviro_get_pm2_5(), qos=1, retain=False)
        client.publish(path_enviro+"pm10", enviro_script.enviro_get_pm10(), qos=1, retain=False)

    if zero_settings.sgp30:
        client.publish(path_sgp30+"voc", sgp30_script.sgp30_get_voc(), qos=1, retain=False)
        client.publish(path_sgp30 + "eco2", sgp30_script.sgp30_get_eco2(), qos=1, retain=False)

    if zero_settings.scd30:
        read_data()


#Infinite loop to send measurement and check operativity
while True:
    try:
        client.loop_start()
        send_messages()
        if connection:
            status = "  all good"
            status_expl = "...sending data"
            #write_to_csv()
            display_status(status, status_expl)
            time.sleep(15)
        else:
            reconnect = client.reconnect()
            status_expl = str(reconnect)
            status = "Error, Check terminal"
            display_status(status, status_expl)
            time.sleep(15);
        client.loop_stop()
    except Exception as e:
        status = "check terminal"
        display_status(status, str(e))
        print(e)
        time.sleep(15)
