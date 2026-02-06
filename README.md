# 🎤 Real-Time Voice Emotion Detection

## 📌 Overview

This project implements a real-time voice emotion detection system using deep learning. It captures speech from a microphone, processes audio signals, and predicts the speaker’s emotional state using a pre-trained HuBERT model. The system runs offline and provides interactive results through a graphical interface.

It demonstrates the practical use of speech emotion recognition in human–computer interaction and intelligent user analysis.

---

## 🚀 Features

* Real-time microphone audio recording
* Deep learning–based emotion classification
* Offline model loading (no internet required)
* Silence detection to avoid false predictions
* GUI-based interaction
* Displays emotion label and confidence score

---

## 🧠 Technologies Used

* Python
* PyTorch
* Hugging Face Transformers
* HuBERT Speech Model
* NumPy
* SoundDevice
* Tkinter / Flask (UI integration)

---

## 📂 Project Structure

```
project-folder/
│
├── static/                    # Frontend assets
├── templates/                 # HTML templates
│
├── app.py                     # Flask application
├── database.db                # SQLite database
├── emotion.py                 # Voice emotion detection module
│
├── models/
│   └── hubert_emotion/        # Pretrained HuBERT model files
│
├── README.md
└── requirements.txt
```

---

## 🤖 Model

HuBERT Speech Emotion Recognition Model:
[https://huggingface.co/xmj2002/hubert-base-ch-speech-emotion-recognition](https://huggingface.co/xmj2002/hubert-base-ch-speech-emotion-recognition)

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```
git clone <repository-url>
cd <project-folder>
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

Or manually:

```
pip install torch transformers sounddevice numpy
```

---

## ▶️ Usage

Run the application:

```
python app.py
```

### Controls

* **Start** → Begins listening and emotion detection
* **Stop** → Stops detection

Detected emotion and confidence will appear on the interface.

---

## 🎯 Supported Emotions

* Neutral
* Angry
* Sad
* Confident (mapped from happy class)
* Silence detection

---

## 🔍 How It Works

1. Records 6-second audio clips at 16kHz
2. Checks for silence using amplitude threshold
3. Extracts features using Wav2Vec2 extractor
4. HuBERT model predicts emotion class
5. Displays result with confidence score

---

## 📈 Applications

* Smart assistants
* Mental health monitoring
* Customer sentiment analysis
* Human–computer interaction research
* Interview assessment tools

---

## ⚠️ Limitations

* Limited emotion categories
* Performance depends on audio quality
* Sensitive to noisy environments
* Uses fixed recording duration

---

## 🔮 Future Improvements

* Expand emotion classes
* Real-time streaming inference
* Noise filtering & preprocessing
* Prediction history storage
* Web/mobile deployment

---

## 👤 Author

**Chandru — AI/ML Developer**

---

## 📜 License

This project is intended for academic and educational purposes.
