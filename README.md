# Distributed-Audio-Transcription-System
This repository implements a distributed audio transcription system using Redis as a job queue and Whisper (Tiny model) for automatic speech recognition (ASR). The system supports a MASTER-WORKER architecture, where the MASTER queues audio files and WORKERS process them to produce text transcriptions.
