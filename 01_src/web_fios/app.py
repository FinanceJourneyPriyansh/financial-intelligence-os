from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import os, time, psutil
from datetime import datetime
import pytz

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
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>FIOS Core Web Server Active</h1>")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "fios_core"}

@app.get("/api/telemetry")
async def get_telemetry():
    tz_ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(tz_ist)
    now_utc = datetime.now(pytz.utc)
    
    uptime_seconds = int(time.time() - START_TIME)
    cpu_usage = psutil.cpu_percent(interval=None)
    ram_mb = int(psutil.virtual_memory().used / (1024 * 1024))
    
    return {
        "ist_time": now_ist.strftime("%H:%M:%S IST"),
        "utc_time": now_utc.strftime("%H:%M:%S UTC"),
        "date_str": now_ist.strftime("%Y-%m-%d"),
        "uptime": f"{uptime_seconds}s",
        "cpu": f"{cpu_usage}%",
        "ram": f"{ram_mb} MB",
        "latency": "1 ms",
        "automation_status": "Active"
    }

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)
