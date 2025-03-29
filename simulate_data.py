import time
import random
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# 🔁 Replace these with YOUR actual values
url = "http://localhost:8086"
token = "1hm5qCCEt8uPg55hSJ76cxlsiQzXiRBt7cClnnSs_dQxyamuj54hMTU0jImt3QBWCTP9tPqoKJGTLqd4SdtEkA=="
org = "iot_org"
bucket = "iot_sensors"

# InfluxDB client setup
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def simulate_sensor_data():
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)

        point = Point("sensor_data") \
            .tag("sensor_id", "sensor_01") \
            .field("temperature", temperature) \
            .field("humidity", humidity)

        write_api.write(bucket=bucket, record=point)
        print(f"✅ Written -> Temp: {temperature}°C | Humidity: {humidity}%")
        time.sleep(5)

if __name__ == "__main__":
    simulate_sensor_data()
