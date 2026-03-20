from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

latest_data = {
    "message": "No data yet"
}

@app.get("/")
def home():
    return {"status": "running"}

# Arduino sends data
@app.get("/api/data")
def receive_data(
    lat: str = None,
    lon: str = None,
    ax: str = None,
    ay: str = None,
    az: str = None,
    gx: str = None,
    gy: str = None,
    gz: str = None
):
    global latest_data

    latest_data = {
        "timestamp": datetime.now().isoformat(),
        "gps": {
            "latitude": lat,
            "longitude": lon
        },
        "mpu6050": {
            "accel": {"ax": ax, "ay": ay, "az": az},
            "gyro": {"gx": gx, "gy": gy, "gz": gz}
        },
        "sim": {
            "network": "4G",
            "status": "connected"
        }
    }

    print("📡 Received:", latest_data)

    # 🚨 simple alert
    if ax and abs(int(ax)) > 15000:
        print("🚨 ACCIDENT DETECTED")

    return {"success": True}

# frontend fetch
@app.get("/api/get")
def get_data():
    return latest_data
