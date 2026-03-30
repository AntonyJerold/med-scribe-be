# Med-Scribe Backend

A FastAPI-based medical transcription service that converts MP3 audio files to text using Whisper, then processes them into SOAP format using Ollama.

## Features

- **Audio Transcription**: Converts MP3 audio to text using faster-whisper (medium model)
- **SOAP Processing**: Converts transcribed text to clinical SOAP format using Ollama (Model: Mistral)
- **Full Async Support**: Properly implemented async/await patterns throughout
- **Comprehensive Error Handling**: Robust error handling with detailed error messages at every step
- **Clinical Assistant Ready**: Configured to process medical dictations

## Prerequisites

### 1. Python
- Python 3.8+ required
- [Download Python](https://www.python.org/downloads/)

### 2. Dependencies

Install Python packages:
```bash
pip install fastapi uvicorn faster-whisper httpx
```

### 3. Ollama (Running Locally on Network)

**Download and Install:**
- [Download Ollama](https://ollama.ai)
- Extract and run the installer
- Download/Setup 'Mistral' Model on ollama

**Pull the Mistral Model:**
```bash
ollama pull mistral
```

**Run Ollama on Network:**
```bash
ollama serve --host localhost:11434
```
This makes Ollama accessible on your local network at `http://localhost:11434`

## Installation & Setup

1. **Clone/navigate to project:**
```bash
cd med-scribe-be
```

2. **Create virtual environment (recommended):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install fastapi uvicorn faster-whisper httpx
```

4. **Ensure sample audio file:**
- Place your MP3 file in `resources/sample_dictation.mp3`

## Running the Server

```bash
python server.py
```

Server will start on `http://localhost:3010`

## API Endpoints

### GET /soap-transcribe

Transcribes audio file and processes into SOAP format.

**Query Parameters:**
- `filename` (optional): Name of the file to transcribe (defaults to `sample_dictation.mp3`)

**Example Requests:**

# Testing on Browser/Postman

# 1. Using default file
url- http://localhost:3010/soap-transcribe

# 2. With specific filename query parameter
url- http://localhost:3010/soap-transcribe?filename=sample_dictation.mp3


## ⚙️ How It Works
1. Upload or provide an audio file  
2. API transcribes the audio (audio-to-text) 
3. Extracts SOAP notes using Ollama Mistral model (text-to-soap)  
4. Saves the result in `results/` folder  
5. Returns response in structured JSON 
---

## 📥 API Response

**Response Success (200):**
```json
{
  transcript: "Transcribed text of the given Audio...",
  SOAP:{
    "Subjective": "Patient reports...",
    "Objective": "Vital signs...",
    "Assessment": "Clinical impression...",
    "Plan": "Treatment plan..."
  }
}
```


### Prerequisites for Testing
1. **Ollama running:** `ollama serve --host localhost:11434`
2. **Server running:** `python server.py`
3. **Sample file present:** `resources/sample_dictation.mp3`


## Architecture

```
med-scribe-be/
├── main.py           # FastAPI app and main endpoint
├── server.py         # Uvicorn server entry point
├── configs/
│   └── constants.py  # Configuration (model, URLs, prompts)
├── utils/
│   ├── transcriber.py      # Whisper transcription logic
│   └── ollama_soap_client.py # Ollama SOAP formatting
└── resources/
    └── sample_dictation.mp3  # Sample audio file
```