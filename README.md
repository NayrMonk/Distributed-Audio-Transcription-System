# Distributed Audio Transcription System

This repository implements a distributed audio transcription system using **Redis** as a job queue and **Whisper (Tiny model)** for automatic speech recognition (ASR). The system supports a **MASTER-WORKER architecture**, where the MASTER queues audio files and WORKERS process them to produce text transcriptions.

---

## Table of Contents

- [System Overview](#system-overview)  
- [Requirements](#requirements)  
- [Setup Instructions](#setup-instructions)  
  - [1. Redis Setup](#1-redis-setup)  
  - [2. MASTER Setup](#2-master-setup)  
  - [3. WORKER Setup](#3-worker-setup)  
- [Usage](#usage)  
- [File Structure](#file-structure)  
- [Troubleshooting](#troubleshooting)  
- [License](#license)  

---

## System Overview

- **MASTER**: Monitors a local folder for new `.wav` audio files, queues them into Redis for processing by workers, and optionally collects results.  
- **WORKER**: Listens for jobs from Redis, processes audio files using Whisper, and writes transcription results to a network-shared folder.

**Key points:**

- Redis is used as a lightweight, centralized job queue.  
- Whisper Tiny model is used for CPU-friendly transcription.  
- Supports network paths: MASTER exposes shared folders, WORKER reads audio from MASTER and writes results back to a shared drive.  

---

## Requirements

- Python 3.10+ (virtual environment recommended)  
- Redis server (Windows build or Linux/Mac)  
- Python packages (install via `pip install -r requirements.txt`):
  ```text
  redis
  whisper
  torch
  ```

* ffmpeg (required by Whisper):

  * Download: https://www.gyan.dev/ffmpeg/builds/

  * Extract to C:\ffmpeg

  * Add C:\ffmpeg\bin to System PATH

  * Verify: ffmpeg -version

* Network-shared folders configured:

  * Audio input folder on MASTER (audio_in) shared with read access.

  * Result folder on WORKER (results) mapped to a network drive.

## Setup Instructions

### 1. Redis Setup

1. Install Redis:

   * Redis for Windows

   * Or on Linux/Mac: sudo apt install redis

2. Create a redis.conf file:

   ```
   bind 0.0.0.0
   protected-mode no
   port 6379
   ```

3. Start Redis:

   ```
   redis-server.exe C:\path\to\redis.conf
   ```

   Ensure port 6379 is accessible from WORKER machines.

### 2. MASTER Setup

1. Clone this repository.

2. Configure Python environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Update master.py with your paths:

   ```
   AUDIO_DIR = r"C:\Users\nicheducan\Desktop\Cluster\audio_in"
   RESULT_DIR = r"C:\Users\nicheducan\Desktop\Cluster\results"
   REDIS_IP = "192.168.18.18"  # MASTER IP
   ```

4. Share the audio_in folder on the network (read access for WORKERS).

5. Run MASTER:

   ```
   python master.py
   ```

   * MASTER will continuously watch audio_in for .wav files and queue jobs to Redis.

### 3. WORKER Setup

1. Clone this repository on the WORKER machine.

2. Configure Python environment and install dependencies.

3. Map network shares:

   * Y: drive pointing to MASTER audio folder (if needed).

   * Z: drive pointing to results folder.

4. Update worker.py paths:

   ```
   REDIS_IP = "192.168.18.18"  # MASTER IP
   LOCAL_RESULT_DIR = r"Z:\results"
   ```

5. Run WORKER:

   ```
   python worker.py
   ```

6. WORKER behavior:

   * Waits for jobs in Redis.

   * Processes audio files using Whisper Tiny.

   * Saves .txt transcriptions to Z:\results.

## Usage

1. Place any .wav audio files into the MASTER audio_in folder.

2. MASTER automatically queues new files.

3. WORKER transcribes audio and writes results to results folder.

4. MASTER optionally reads results from Redis or shared folder.

Example network paths:

* MASTER audio: \\192.168.18.18\audio_in\example.wav

* WORKER results: Z:\example.wav.txt

## File Structure

```
.
├── master.py          # MASTER script
├── worker.py          # WORKER script
├── redis.conf         # Redis configuration
├── requirements.txt   # Python dependencies
├── audio_in/          # MASTER local folder for .wav files
└── results/           # MASTER local folder (optional) or WORKER network folder
```

## Troubleshooting

* [WinError 2] The system cannot find the file specified

  * Whisper requires ffmpeg. Install and add to PATH:

    ```
    1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    2. Extract to C:\ffmpeg
    3. Add C:\ffmpeg\bin to System PATH
    4. Open new terminal and run: ffmpeg -version
    ```

* Redis connection issues:

  * Ensure MASTER IP is reachable and port 6379 is open.

  * Ensure firewall allows TCP connections.

* File access issues:

  * Make sure the WORKER has read access to audio_in and write access to results.

  * Test network paths in File Explorer first.

* Whisper CPU warnings:

  * Tiny model is CPU-friendly. Warnings about FP16 are normal on CPU.

## License

This project is licensed under MIT License.
