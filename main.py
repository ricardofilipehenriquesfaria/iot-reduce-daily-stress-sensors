#!/usr/bin/env python
from sense_hat import SenseHat
import time
import MySQLdb

database = MySQLdb.connect("localhost", "root", "admin", "sensors")
cursor = database.cursor();

sense = SenseHat()

blue = (0, 0, 255)
yellow = (255, 255, 255)

speed = 0.08

while True:
    
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()
    orientation = sense.get_orientation()

    pitch = orientation['pitch']
    roll = orientation['roll']
    yaw = orientation['yaw']
    print (yaw)

    try:
        cursor.execute("""INSERT INTO sensors (temperature, pressure, humidity) values (%s, %s, %s)""", (temperature, pressure, humidity))
        database.commit()
        print "Data comitted"
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

    try:
        cursor.execute("""INSERT INTO orientation (pitch, roll, yaw) values (%s, %s, %s)""", (pitch, roll, yaw))
        database.commit()
        print "Data comitted"
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)

    message = "pitch = {0}, roll = {1}, yaw = {2}".format(pitch, yaw, roll)

    sense.show_message(message, speed, text_colour=yellow, back_colour=blue)

    time.sleep(60)

database.close()
