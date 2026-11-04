import subprocess
import time
import urllib.request
import json
import base64
import os
import websockets.sync.client

PAGES = [
    ("screenshot-limit-full.png", "http://localhost:8501/limit_approach"),
    ("screenshot-tangent-full.png", "http://localhost:8501/tangent"),
    ("screenshot-riemann-full.png", "http://localhost:8501/riemann"),
    ("screenshot-substitution-full.png", "http://localhost:8501/substitution"),
    ("screenshot-area-full.png", "http://localhost:8501/area_between"),
    ("screenshot-volume-full.png", "http://localhost:8501/volume_revolution"),
    ("screenshot-improper-full.png", "http://localhost:8501/improper_integrals"),
    ("screenshot-quiz-full.png", "http://localhost:8501/quiz"),
    ("screenshot-solver-full.png", "http://localhost:8501/solver"),
]

OUT_DIR = "/home/kitti/Documents/GitHub/calculus-integration-app/docs/defense/figures"
os.makedirs(OUT_DIR, exist_ok=True)

def run_capture():
    cmd = [
        "/usr/sbin/chromium",
        "--headless=new",
        "--disable-gpu",
        "--remote-debugging-port=9228",
        "--user-data-dir=/tmp/cdp_capture_profile3"
    ]
    env = os.environ.copy()
    env["TMPDIR"] = "/tmp"
    
    proc = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    try:
        for fname, url in PAGES:
            print(f"Opening {url} ...", flush=True)
            req = urllib.request.Request(f"http://127.0.0.1:9228/json/new?{url}", method="PUT")
            res = urllib.request.urlopen(req)
            tab = json.loads(res.read())
            tab_id = tab["id"]
            ws_url = tab["webSocketDebuggerUrl"]
            
            with websockets.sync.client.connect(ws_url) as ws:
                # Set initial wide viewport
                ws.send(json.dumps({
                    "id": 1,
                    "method": "Emulation.setDeviceMetricsOverride",
                    "params": {
                        "width": 1280,
                        "height": 1000,
                        "deviceScaleFactor": 1,
                        "mobile": False
                    }
                }))
                ws.recv()
                
                # Wait for Streamlit to finish running and plot graphs
                time.sleep(5)
                
                # Expand details if any and get actual main content height
                ws.send(json.dumps({
                    "id": 2,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": """
                        (() => {
                            const main = document.querySelector('section.main') || document.querySelector('[data-testid=\"stAppViewContainer\"]');
                            const h = main ? main.scrollHeight : document.body.scrollHeight;
                            return {
                                scrollHeight: h,
                                numImages: document.querySelectorAll('img, svg, canvas').length
                            };
                        })()
                        """,
                        "returnByValue": True
                    }
                }))
                eval_res = json.loads(ws.recv())
                val = eval_res.get("result", {}).get("result", {}).get("value", {})
                scroll_height = val.get("scrollHeight", 2000)
                num_imgs = val.get("numImages", 0)
                print(f"  Detected full height: {scroll_height}px, images/plots: {num_imgs}", flush=True)
                
                total_h = max(int(scroll_height) + 60, 1600)
                
                # Apply full height so entire page fits in one single continuous viewport
                ws.send(json.dumps({
                    "id": 3,
                    "method": "Emulation.setDeviceMetricsOverride",
                    "params": {
                        "width": 1280,
                        "height": total_h,
                        "deviceScaleFactor": 1,
                        "mobile": False
                    }
                }))
                ws.recv()
                time.sleep(1)
                
                # Capture full screenshot
                ws.send(json.dumps({
                    "id": 4,
                    "method": "Page.captureScreenshot",
                    "params": {
                        "format": "png",
                        "captureBeyondViewport": True
                    }
                }))
                shot_res = json.loads(ws.recv())
                b64_data = shot_res["result"]["data"]
                
                out_path = os.path.join(OUT_DIR, fname)
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(b64_data))
                print(f"  Saved {fname} ({os.path.getsize(out_path)} bytes, height={total_h}px)", flush=True)
                
            # Close tab
            req_close = urllib.request.Request(f"http://127.0.0.1:9228/json/close/{tab_id}", method="GET")
            urllib.request.urlopen(req_close)
            time.sleep(0.5)
            
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    run_capture()
