import os 
import time
import configparser
from datetime import datetime
from gpiozero import Button
from influxdb import InfluxDBClient

dir_path = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(dir_path+'/config.ini')

client = InfluxDBClient(
    host=config['influxDB']['Host'], 
    port=config['influxDB']['Port'])

client.switch_database(config['influxDB']['Database'])

button = Button(2)

print('Service Started, waiting for interactions')

while True:
    button.wait_for_press()
    starttime = time.time()
    starttimestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print("Door was opened")
    client.write_points([{
        "measurement": "doorStatus",
        "tags": {
            "fridge": "Korbis Fridge"
        },
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "open": 1
        }
        
    }])

    button.wait_for_release()
    endtime = time.time()
    time_taken = endtime - starttime
    print("Door was closed - was open for "+str(time_taken))
    client.write_points([{
        "measurement": "doorStatus",
        "tags": {
            "fridge": "Korbis Fridge"
        },
        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "fields": {
            "open": 0
        }
        
    }])
    json_data = [{
        "measurement": "doorOpenDurations",
        "tags": {
            "fridge": "Korbis Fridge"
        },
        "time": starttimestamp,
        "fields": {
            "duration": int(time_taken)
        }
        
    }]
    client.write_points(json_data)