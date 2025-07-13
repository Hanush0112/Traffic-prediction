# 🚦 Traffic Congestion Detection & Smart Route Navigator

A real-time AI-based traffic prediction and navigation system that detects traffic congestion using computer vision and automatically suggests alternate routes via **Google Maps API**. This solution is ideal for smart city infrastructure, traffic management systems, and driver assistance platforms.

📍 Combines CV-based detection + Google Maps Routing API  
🚗 Recommends less congested paths in real-time

---

## 🎯 Objective

To reduce commute delays and urban traffic by:
- Detecting traffic congestion using surveillance or roadside cameras
- Identifying if vehicles are stationary for long durations
- Notifying users about congestion with an alternate route suggestion via Google Maps API

---

## 🧠 How It Works

1. **Video Feed Input**: Real-time or recorded traffic camera footage.
2. **Congestion Detection**:
   - Virtual boundaries/zones are drawn in the frame.
   - If vehicles remain within the zone (stationary) for a specific time threshold, it flags a traffic jam.
3. **Trigger Route Suggestion**:
   - The system fetches an alternate, faster route using **Google Maps Directions API**.
   - Sends it to nearby users or displays it on a dashboard.

---

## 🧪 Technologies Used

| Tech/Library       | Purpose                                      |
|--------------------|----------------------------------------------|
| Python             | Core programming                            |
| OpenCV             | Vehicle detection & virtual boundary logic  |
| Google Maps API    | Route navigation and traffic data           |
| Streamlit  | Web interface (optional)                            |
| NumPy              | Frame operations                            |
| Time & Geometry    | For delay and distance calculations         |

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hanush0112/traffic-predictor.git
cd traffic-predictor
