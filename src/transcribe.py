import whisper
from src.app_config import WHISPER_MODEL_SIZE


def transcribe_video(video_path: str) -> str:
    """
    Extracts audio from a video file and transcribes it using OpenAI Whisper.

    Args:
        video_path (str): Path to the local MP4 file.

    Returns:
        str: The transcribed text.
    """
    print(f"Loading Whisper model: {WHISPER_MODEL_SIZE}...")
    model = whisper.load_model(WHISPER_MODEL_SIZE)

    print(f"Transcribing {video_path}...")
    # Whisper handles audio extraction from video files internally via ffmpeg
    result = model.transcribe(video_path)

    return result["text"]


if __name__ == "__main__":
    # Test stub
    pass
