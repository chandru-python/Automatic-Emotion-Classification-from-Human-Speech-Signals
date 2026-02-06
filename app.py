from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import torch
import soundfile as sf
from transformers import Wav2Vec2FeatureExtractor, HubertForSequenceClassification
from pydub import AudioSegment


# =====================================
# FLASK CONFIG
# =====================================
app = Flask(__name__, static_folder="static")
app.secret_key = "dyuiknbvcxswe678ijc6i"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

# =====================================
# DATABASE
# =====================================
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =====================================
# LOAD HUBERT EMOTION MODEL (OFFLINE)
# =====================================
MODEL_PATH = os.path.join(BASE_DIR, "models", "hubert_emotion")

if not os.path.isdir(MODEL_PATH):
    raise FileNotFoundError("HuBERT emotion model folder not found")

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    MODEL_PATH, local_files_only=True
)

emotion_model = HubertForSequenceClassification.from_pretrained(
    MODEL_PATH, local_files_only=True
)
emotion_model.eval()

id2label = emotion_model.config.id2label

# =====================================
# EMOTION PREDICTION FUNCTION
# =====================================
def predict_emotion_from_audio(wav_path):
    audio, sr = sf.read(wav_path)

    inputs = feature_extractor(
        audio,
        sampling_rate=sr,
        return_tensors="pt"
    )

    with torch.no_grad():
        logits = emotion_model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]

    idx = torch.argmax(probs).item()
    emotion = id2label[idx]
    confidence = probs[idx].item()

    friendly_map = {
        "hap": "confident",
        "neu": "neutral",
        "ang": "angry",
        "sad": "sad",
        "fea": "fear",
        "dis": "disgust",
        "sur": "surprise"
    }

    return friendly_map.get(emotion, emotion), round(confidence * 100, 2)

# =====================================
# ROUTES
# =====================================

@app.route("/")
def index():
    return render_template("index.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?", (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Login successful", "success")
            return redirect(url_for("voice_emotion"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = generate_password_hash(request.form["password"])

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (name,email,phone,password) VALUES (?,?,?,?)",
                (name, email, phone, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists", "danger")

    return render_template("register.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return render_template("about.html")


# =====================================
# 🎤 VOICE EMOTION ROUTE
# =====================================
@app.route("/voice-emotion", methods=["GET", "POST"])
def voice_emotion():

    if "user_id" not in session:
        flash("Please login to access Voice Emotion Detection", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        if "audio" not in request.files:
            return jsonify({"error": "No audio received"}), 400

        audio_file = request.files["audio"]

        raw_path = os.path.join(BASE_DIR, "temp.webm")
        wav_path = os.path.join(BASE_DIR, "temp.wav")

        # 1️⃣ Save raw browser audio
        audio_file.save(raw_path)

        # 2️⃣ Convert WebM → WAV (16kHz mono)
        sound = AudioSegment.from_file(raw_path)
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(wav_path, format="wav")

        # 3️⃣ Predict emotion
        emotion, confidence = predict_emotion_from_audio(wav_path)

        # 4️⃣ Cleanup
        os.remove(raw_path)
        os.remove(wav_path)

        return jsonify({
            "emotion": emotion,
            "confidence": confidence
        })

    return render_template("voice_emotion.html")



# =====================================
# RUN SERVER
# =====================================
if __name__ == "__main__":
    app.run(debug=True)
