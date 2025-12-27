import redis
import os
import time
import json

# Redis config — this MUST be at the top level, not indented
REDIS_IP = "192.168.18.18"  # MASTER laptop IP
r = redis.Redis(host=REDIS_IP, port=6379, decode_responses=True)

# Local paths on MASTER laptop
AUDIO_DIR = r"C:\Users\nicheducan\Desktop\Cluster\audio_in"
RESULT_DIR = r"C:\Users\nicheducan\Desktop\Cluster\results"

os.makedirs(RESULT_DIR, exist_ok=True)

print("MASTER ready. Watching for audio files...")

seen = set()

while True:
    try:
        # Scan for new .wav files
        for file in os.listdir(AUDIO_DIR):
            if file.lower().endswith(".wav") and file not in seen:
                # Correct network path — share name is "audio_in"
                network_path = rf"\\192.168.18.18\audio_in\{file}"

                job = {
                    "file": file,
                    "path": network_path
                }

                r.lpush("jobs", json.dumps(job))
                seen.add(file)
                print(f"Queued: {file}")
                print(f"   Network path sent: {network_path}")

    except Exception as e:
        print(f"Error while scanning or queuing: {e}")

    time.sleep(1)