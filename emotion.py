import os
import threading
import torch
import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
from transformers import Wav2Vec2FeatureExtractor, HubertForSequenceClassification

# ===============================
# MODEL PATH (WINDOWS SAFE)
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "hubert_emotion")

if not os.path.isdir(MODEL_PATH):
    raise FileNotFoundError(f"Model folder not found: {MODEL_PATH}")

# ===============================
# LOAD MODEL (OFFLINE)
# ===============================
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    MODEL_PATH, local_files_only=True
)

model = HubertForSequenceClassification.from_pretrained(
    MODEL_PATH, local_files_only=True
)
model.eval()

id2label = model.config.id2label

# ===============================
# AUDIO SETTINGS
# ===============================
SAMPLE_RATE = 16000
DURATION = 6
SILENCE_THRESHOLD = 0.01

running = False   

# ===============================
# AUDIO FUNCTIONS
# ===============================
def record_audio():
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()

def is_silence(audio):
    return np.mean(np.abs(audio)) < SILENCE_THRESHOLD

def predict_emotion(audio):
    if is_silence(audio):
        return "silence", 0.0

    inputs = feature_extractor(
        audio,
        sampling_rate=SAMPLE_RATE,
        return_tensors="pt"
    )

    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]

    idx = torch.argmax(probs).item()
    emotion = id2label[idx]
    confidence = probs[idx].item()

    friendly_map = {
        "hap": "confident",
        "neu": "neutral",
        "ang": "angry",
        "sad": "sad"
    }

    emotion = friendly_map.get(emotion, emotion)
    return emotion, confidence


# ===============================
# BACKGROUND THREAD
# ===============================
def emotion_loop():
    global running
    while running:
        status_label.config(text="🎧 Listening...")
        audio = record_audio()

        if not running:
            break

        emotion, conf = predict_emotion(audio)

        if emotion == "silence":
            emotion_label.config(text="Emotion: ---")
            confidence_label.config(text="Confidence: ---")
        else:
            emotion_label.config(
                text=f"Emotion: {emotion.upper()}"
            )
            confidence_label.config(
                text=f"Confidence: {conf*100:.2f}%"
            )

        status_label.config(text="🟢 Ready")


# ===============================
# GUI CONTROL FUNCTIONS
# ===============================
def start_detection():
    global running
    if not running:
        running = True
        threading.Thread(target=emotion_loop, daemon=True).start()
        status_label.config(text="🟢 Started")

def stop_detection():
    global running
    running = False
    status_label.config(text="🛑 Stopped")


# ===============================
# TKINTER GUI
# ===============================
root = tk.Tk()
root.title("Real-Time Voice Emotion Detection")
root.geometry("420x320")
root.resizable(False, False)

title = ttk.Label(
    root,
    text="🎤 Voice Emotion Detection",
    font=("Segoe UI", 16, "bold")
)
title.pack(pady=15)

emotion_label = ttk.Label(
    root,
    text="Emotion: ---",
    font=("Segoe UI", 14)
)
emotion_label.pack(pady=10)

confidence_label = ttk.Label(
    root,
    text="Confidence: ---",
    font=("Segoe UI", 12)
)
confidence_label.pack(pady=5)

status_label = ttk.Label(
    root,
    text="🟡 Idle",
    font=("Segoe UI", 10)
)
status_label.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

start_btn = ttk.Button(
    button_frame,
    text="▶ Start",
    command=start_detection,
    width=12
)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ttk.Button(
    button_frame,
    text="■ Stop",
    command=stop_detection,
    width=12
)
stop_btn.grid(row=0, column=1, padx=10)

root.mainloop()
