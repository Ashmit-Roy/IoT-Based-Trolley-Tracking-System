# 🚀 IoT-Based Airport Trolley Tracking System
An IoT-based Airport Trolley Tracking System developed using **ESP32 BLE**, **MQTT**, **Python**, **SQLite**, and **Streamlit** to monitor airport trolley locations in real time.
---
# 📌 Overview
This project provides real-time tracking of airport trolleys by using ESP32 devices as BLE scanners. The scanners detect nearby BLE-enabled trolleys, send the information through MQTT, and store it in an SQLite database. A Streamlit dashboard allows airport staff to monitor trolley availability, locations, and system status.
---
# ✨ Features
- Real-time trolley tracking
- BLE RSSI-based detection
- MQTT communication
- SQLite database
- Streamlit dashboard
- Admin login system
- Zone-wise monitoring
- Automatic data updates
---
# 🛠 Technologies Used
- Python
- ESP32
- Bluetooth Low Energy (BLE)
- MQTT
- SQLite
- Streamlit
---
# 📂 Project Structure
```
IoT-Based-Trolley-Tracking-System
│
├── backend/
├── dashboard/
├── docs/
├── firmware/
├── images/
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```
---
# 🚀 Installation
```bash
pip install -r requirements.txt
```
Start the backend:

```bash
python backend/backend.py
```
Run the dashboard:

```bash
streamlit run backend/app.py
```
---
# 📌 Future Improvements

- LoRaWAN Integration
- AWS Cloud Deployment
- GPS Tracking
- AI-based Trolley Demand Prediction
- Mobile Application

---

# 👨‍💻 Author
**Ashmit Roy**