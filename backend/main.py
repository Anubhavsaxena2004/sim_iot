from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_data = {
    "message": "No data yet"
}

@app.get("/")
def home():
    return {"status": "running"}

# ESP32 + SIM7600X sends data via GET
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

    # Accident detection
    accident = False
    if ax:
        try:
            if abs(float(ax)) > 15000:
                accident = True
                print("🚨 ACCIDENT DETECTED")
        except:
            pass

    latest_data = {
        "timestamp": datetime.now().isoformat(),
        "gps": {
            "latitude": lat,
            "longitude": lon
        },
        "mpu6050": {
            "accel": {"ax": ax, "ay": ay, "az": az},
            "gyro":  {"gx": gx, "gy": gy, "gz": gz}
        },
        "accident_detected": accident,   # ← frontend uses this
        "sim": {
            "network": "4G",
            "status": "connected"
        }
    }

    print("📡 Received:", latest_data)
    return {"success": True}

# Frontend fetches this
@app.get("/api/get")
def get_data():
    return latest_data