# Local Video Summarizer & Transcriber 📝

This project is an AI-driven tool designed to process local MP4 video files. It extracts the audio stream, transcribes it using OpenAI's Whisper model, and uses a Large Language Model (LLM) to generate a concise summary and extract key points.

## Features 🚀

- **Local File Support**: Upload MP4 files directly from your computer.
- **Audio Extraction & Transcription**: Uses `openai-whisper` to convert speech to text.
- **AI Summarization**: Generates summaries and bullet points using Gemini or GPT models.
- **Privacy**: Process your own files without relying on YouTube links.
- **Streamlit Interface**: Simple and easy-to-use web UI.

## Requirements

- **OS**: Linux, Windows, or macOS
- **Python**: 3.10+
- **FFmpeg**: Required for audio processing by Whisper.

## Installation

### 1. Install System Dependencies (FFmpeg)

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**MacOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your System PATH environment variables.

### 2. Install Python Environment

**Activate the virtual environment**

```bash
python -m venv virtual
source virtual/bin/activate  # On Windows: .\virtual\Scripts\activate
```

**Install Python packages:**

```bash
pip install -r requirements.txt
```

### 3. Set API Key

1. Go to [Google AI Studio](https://aistudio.google.com) (or OpenAI) to get your API Key.
2. Create a `.env` file in the project directory:

```bash
touch .env
```

3. Add your key:
```
LLM_API_KEY="YOUR_API_KEY_HERE"
```

### 4. Configuration (Optional)

You can change the LLM model or Whisper model size in `src/app_config.py`. 
*Note: Larger Whisper models (small, medium, large) require more RAM and CPU/GPU power.*

```python
WHISPER_MODEL_SIZE = "base" # Options: tiny, base, small, medium, large
MODEL_NAME = "gpt-5-mini"
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. The browser will open.
3. Drag and drop an **MP4** file into the uploader.
4. Click **Transcribe & Summarize**.
5. Wait for the transcription (Whisper) and analysis (LLM) to finish.
6. Read your summary!

## FAQ

**Q: Is it free?**
A: The code uses your own API key. Google Gemini currently offers a free tier. Whisper runs locally on your machine, so it costs nothing but electricity.

**Q: It's slow?**
A: Transcription speed depends on your hardware (CPU vs GPU) and the `WHISPER_MODEL_SIZE` selected in config. `tiny` or `base` are fast; `large` is accurate but slow.