import redis
import json
import os
import time
from whisper import load_model

# Redis config
REDIS_IP = "192.168.18.18"  # MASTER IP
r = redis.Redis(host=REDIS_IP, port=6379, decode_responses=True)

# Paths on WORKER - NO LOCAL TEMP NEEDED ANYMORE
LOCAL_RESULT_DIR = r"Z:\results"  # network share mapped for results
os.makedirs(LOCAL_RESULT_DIR, exist_ok=True)

# Load Whisper
print("Loading Whisper model (tiny)...")
model = load_model("tiny")
print("Model loaded!")
print("WORKER online, waiting for jobs...")

while True:
    job = r.brpop("jobs", timeout=5)
    if not job:
        continue  # Timeout — just loop again

    try:
        job_data = json.loads(job[1])
        network_path = job_data["path"]
        filename = job_data["file"]

        print(f"\nNew job received: {filename}")
        print(f"Processing directly from network: {network_path}")

        # Safety check: verify network file exists and has size
        if not os.path.exists(network_path):
            print(f"ERROR: Source file not accessible: {network_path}")
            continue

        network_size = os.path.getsize(network_path)
        print(f"Network file confirmed: {network_size:,} bytes")

        print(f"Processing with Whisper directly from network: {network_path}")
        result = model.transcribe(network_path)  # DIRECT PROCESSING - NO COPY!
        text = result["text"].strip()

        # Save result to mapped results drive
        out_file = os.path.join(LOCAL_RESULT_DIR, filename + ".txt")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Transcription saved: {out_file}")
        print(f"📝 Length: {len(text)} characters")
        print(f"🔊 Text preview: {text[:100]}{'...' if len(text) > 100 else ''}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid job data received (JSON error): {e}")

    except redis.RedisError as e:
        print(f"Redis connection error: {e}")

    except Exception as e:
        print(f"❌ Unexpected error processing {network_path}: {e}")
        print(f"   Tip: If '[WinError 2]' appears, install ffmpeg:")
        print(f"   1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
        print(f"   2. Extract to C:\\ffmpeg")
        print(f"   3. Add C:\\ffmpeg\\bin to System PATH")
        print(f"   4. Restart terminal & run: ffmpeg -version")