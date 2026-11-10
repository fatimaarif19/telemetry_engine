# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from collections import deque
from datetime import datetime
from ml.pipeline import TelemetryDetector

app = FastAPI(title="Edge Telemetry Engine")
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("static/index.html")

detector = TelemetryDetector()
telemetry_log = deque(maxlen=100)

class TelemetryPacket(BaseModel):
    cpu_usage: float = Field(..., ge=0, le=100)
    memory_usage: float = Field(..., ge=0, le=100)
    network_throughput_mbps: float = Field(..., ge=0)
    request_rate_rps: int = Field(..., ge=0)

@app.get("/")
def health_check():
    return {"status": "online", "engine": "IsolationForest Inference Pipeline"}

@app.post("/api/v1/telemetry")
def process_telemetry(packet: TelemetryPacket):
    packet_data = packet.model_dump()
    result = detector.predict(packet_data)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": packet_data,
        "analysis": result
    }
    telemetry_log.appendleft(entry)
    return {"status": "processed", "result": result}

@app.get("/api/v1/logs")
def get_recent_logs():
    return list(telemetry_log)