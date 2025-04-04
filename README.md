# 🌡️ IoT Sensor Dashboard

This project simulates IoT sensor data and displays it in a dynamic dashboard using **InfluxDB**, **Flask**, and **Plotly Dash**.

---

## 📁 Project Structure


---

## ⚙️ Technologies Used

- Python 🐍  
- Flask 🌐  
- Dash 📊  
- InfluxDB 📡  
- Plotly 📈  

---

## ▶️ How It Works

1. `simulate_data.py` writes random temperature and humidity data to InfluxDB  
2. `app.py` serves the data as an API  
3. `dashboard.py` pulls data via Flask and displays it in a graph  
4. You can view the graph on `http://localhost:8050`

---

## 💻 How to Run It

```bash
# 1. Clone the repo
git clone https://github.com/your-username/iot_sensor_dashboard.git

# 2. Navigate into the project
cd iot_sensor_dashboard

# 3. Create a virtual environment (optional but recommended)
python -m venv env
.\env\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run InfluxDB separately using influxd.exe
# Ensure your token, org, and bucket match simulate_data.py

# 6. Run data simulation
python simulate_data.py

# 7. Run backend API
python app.py

# 8. Run the dashboard
python dashboard.py
