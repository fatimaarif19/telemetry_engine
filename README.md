# Edge Telemetry & Threat Detection Engine
A lightweight, concurrent realtime telemetry ingestion and ML powered anomaly detection pipeline.

## Tech Stack
* **Backend:** FastAPI, Python `asyncio`, Multi-threading
* **Machine Learning:** Scikit-Learn (`IsolationForest`)
* **Frontend:** Tailwind CSS, Live REST Polling
* **Deployment:** Docker Containerized

## Architecture Flow
1. **Producer:** Multi-threaded workers stream simulated hardware metrics (CPU, RAM, Network, RPS).
2. **Inference:** FastAPI backend scores incoming payloads against an unsupervised Isolation Forest model in real time.
3. **Dashboard:** Operator UI visualizes data streams and flags security anomalies instantly.

## Quick Start

**Install dependencies:**
pip install -r requirements.txt

**Train model artifact:**
python ml/pipeline.py

**Start backend server:**
python -m uvicorn main:app --port 8000

**Run stream generator (in a second terminal):**
python stream_generator.py

**View Dashboard:**
Open http://127.0.0.1:8000/dashboard in your browser.

**Docker Build:**
docker build -t telemetry-engine .
docker run -p 8000:8000 telemetry-engine
