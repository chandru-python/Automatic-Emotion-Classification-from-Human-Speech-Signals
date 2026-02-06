# 🎤 Real-Time Voice Emotion Detection

## 📌 Overview

This project implements a real-time voice emotion detection system using deep learning. It captures speech from a microphone, processes the audio signal, and predicts the speaker’s emotional state using a pre-trained HuBERT model. A simple Tkinter GUI displays detected emotions and confidence levels interactively.

The system works offline and demonstrates practical applications of speech emotion recognition in human–computer interaction.

---

## 🚀 Features

* Real-time microphone audio recording
* Deep learning–based emotion classification
* Offline model loading (no internet required)
* Silence detection to avoid false predictions
* Interactive graphical interface (Tkinter)
* Displays emotion label and confidence score

---

## 🧠 Technologies Used

* Python
* PyTorch
* Hugging Face Transformers
* HuBERT (Speech Representation Model)
* NumPy
* SoundDevice
* Tkinter (GUI)

---

## 📂 Project Structure

```
project-folder/
│
├── models/
│   └── hubert_emotion/       
│
├── main.py                   
├── README.md
└── requirements.txt
```
## Model link https://huggingface.co/xmj2002/hubert-base-ch-speech-emotion-recognition?utm_source
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
python main.py
```

### Controls

* **Start** → Begins listening and emotion detection
* **Stop** → Stops detection

Detected emotion and confidence will appear on the GUI.

---

## 🎯 Supported Emotions

* Neutral
* Angry
* Sad
* Confident (mapped from happy class)
* Silence detection (no output)

---

## 🔍 How It Works

1. Records 6-second audio clips at 16kHz
2. Detects silence using amplitude threshold
3. Extracts speech features using Wav2Vec2 extractor
4. HuBERT model classifies emotion
5. GUI displays prediction and confidence

---

## 📈 Applications

* Smart assistants
* Mental health monitoring
* Customer support analytics
* Human–computer interaction research
* Interview assessment tools

---

## ⚠️ Limitations

* Limited emotion classes
* Accuracy depends on audio quality
* Not optimized for noisy environments
* Uses fixed recording duration

---

## 🔮 Future Improvements

* Add more emotion categories
* Real-time streaming inference
* Noise reduction preprocessing
* Save prediction history
* Deploy as web or mobile app

---

## 👤 Author

Chandru AI/ML Developer

---

## 📜 License

This project is for academic and educational use.
