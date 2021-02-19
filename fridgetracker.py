import time
import configparser
from datetime import datetime
from gpiozero import Button
from influxdb import InfluxDBClient

config = configparser.ConfigParser()
config.read('config.ini')

client = InfluxDBClient(
    host=config['influxDB']['Host'], 
    port=config['influxDB']['Port'])

client.switch_database(config['influxDB']['Database'])

button = Button(2)

while True:
    button.wait_for_release()
    starttime = time.time()
    starttimestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    print("Door was opened")

    button.wait_for_press()
    endtime = time.time()
    time_taken = endtime - starttime
    print("Door was closed - was open for "+str(time_taken))
    json_data = [{
        "measurement": "doorOpenEvents",
        "tags": {
            "fridge": "Korbi's Kühlschrank"
        },
        "time": starttimestamp,
        "duration": int(time_taken)
    }]
    print(json_data)
    client.write_points(json_data)







