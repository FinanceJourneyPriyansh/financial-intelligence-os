import os
import sys
import subprocess
import time

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_src")
os.environ["PYTHONPATH"] = src_dir + os.pathsep + os.environ.get("PYTHONPATH", "")

def launch_fios():
    print("==================================================")
    print("   FIOS MINIMALIST MULTI-SERVER ORCHESTRATOR      ")
    print("   Server 1 (FIOS Core): http://127.0.0.1:8090   ")
    print("   Server 2 (Gold Intel): http://127.0.0.1:8091  ")
    print("==================================================")

    env = os.environ.copy()

    # Module paths updated to import relative to PYTHONPATH (01_src)
    s1 = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "web.app:app", "--port", "8090"
    ], env=env)

    s2 = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "web.gold_intelligence.app:app", "--port", "8091"
    ], env=env)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down FIOS servers...")
        s1.terminate()
        s2.terminate()

if __name__ == "__main__":
    launch_fios()
