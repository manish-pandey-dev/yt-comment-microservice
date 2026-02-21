import subprocess
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_transcript(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"

    output_dir = Path("./tmp")
    output_dir.mkdir(exist_ok=True)

    audio_path = output_dir / f"{video_id}.mp3"

    # Download audio only
    command = [
        "yt-dlp",
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--no-playlist",
        "--no-part",
        "-o", str(output_dir / "%(id)s.%(ext)s"),
        url
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("yt-dlp audio error:", result.stderr)
        return None

    if not audio_path.exists():
        return None

    # Transcribe using OpenAI Whisper
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    # Cleanup
    # audio_path.unlink(missing_ok=True)

    return transcript.text
