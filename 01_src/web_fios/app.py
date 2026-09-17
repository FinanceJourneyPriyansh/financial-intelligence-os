from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import os, time, psutil
from datetime import datetime

app = FastAPI(title="FIOS Core Web Server")
START_TIME = time.time()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "fios_core"}

@app.get("/api/telemetry")
async def get_telemetry():
    now = datetime.now()
    uptime = int(time.time() - START_TIME)
    cpu = psutil.cpu_percent(interval=None)
    ram = int(psutil.virtual_memory().used / (1024 * 1024))
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "uptime": f"{uptime}s",
        "cpu": f"{cpu}%",
        "ram": f"{ram} MB",
        "latency": "1 ms",
        "automation_status": "Active"
    }

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)
