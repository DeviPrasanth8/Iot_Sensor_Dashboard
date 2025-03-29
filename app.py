from flask import Flask, jsonify
from influxdb_client import InfluxDBClient

app = Flask(__name__)

# InfluxDB config (same as in simulate_data.py)
url = "http://localhost:8086"
token = "1hm5qCCEt8uPg55hSJ76cxlsiQzXiRBt7cClnnSs_dQxyamuj54hMTU0jImt3QBWCTP9tPqoKJGTLqd4SdtEkA=="
org = "iot_org"
bucket = "iot_sensors"

client = InfluxDBClient(url=url, token=token, org=org)

@app.route('/api/sensor_data')
def get_sensor_data():
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "sensor_data")
    '''
    tables = client.query_api().query(query)

    data = []
    for table in tables:
        for record in table.records:
            data.append({
                "sensor_id": record.values.get("sensor_id"),
                "time": record.get_time().isoformat(),
                "field": record.get_field(),
                "value": record.get_value()
            })
    return jsonify(data)

from flask import Response
import csv
import io

@app.route('/api/export_csv')
def export_csv():
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "sensor_data")
    '''
    tables = client.query_api().query(query)

    # Prepare CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['sensor_id', 'time', 'field', 'value'])

    for table in tables:
        for record in table.records:
            writer.writerow([
                record.values.get("sensor_id"),
                record.get_time().isoformat(),
                record.get_field(),
                record.get_value()
            ])

    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=sensor_data.csv"}
    )


if __name__ == '__main__':
    app.run(debug=True)
