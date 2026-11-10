# stream_generator.py
import time
import random
import threading
import requests

SERVER_URL = "http://127.0.0.1:8000/api/v1/telemetry"

def generate_telemetry_packet(is_anomaly=False):
    if is_anomaly:
        return {
            "cpu_usage": round(random.uniform(90.0, 100.0), 2),
            "memory_usage": round(random.uniform(85.0, 99.0), 2),
            "network_throughput_mbps": round(random.uniform(500.0, 1000.0), 2),
            "request_rate_rps": random.randint(5000, 10000)
        }
    return {
        "cpu_usage": round(random.uniform(10.0, 60.0), 2),
        "memory_usage": round(random.uniform(20.0, 65.0), 2),
        "network_throughput_mbps": round(random.uniform(10.0, 100.0), 2),
        "request_rate_rps": random.randint(100, 1000)
    }

def stream_worker(worker_id):
    while True:
        inject_anomaly = random.random() < 0.15
        packet = generate_telemetry_packet(is_anomaly=inject_anomaly)
        try:
            requests.post(SERVER_URL, json=packet, timeout=1)
        except Exception:
            pass
        time.sleep(0.8)

if __name__ == "__main__":
    print("[+] Starting multi-threaded stream producer...")
    for i in range(2):
        t = threading.Thread(target=stream_worker, args=(i,), daemon=True)
        t.start()
    while True:
        time.sleep(1)