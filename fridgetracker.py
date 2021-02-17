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
    print("Button was pressed")

    button.wait_for_press()
    endtime = time.time()
    time_taken = endtime - starttime
    print("Button was pressed for"+str(time_taken))
    json_data = [{
        "measurement": "doorOpenEvents",
        "time": str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')),
        "duration": int(time_taken)
    }]
    print(json_data)
    client.write_points(json_data)







