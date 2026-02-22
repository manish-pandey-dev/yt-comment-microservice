import subprocess
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHUNK_DURATION = 300  # 5 minutes


def fetch_transcript(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"

    output_dir = Path("./tmp")
    output_dir.mkdir(exist_ok=True)

    audio_path = output_dir / f"{video_id}.mp3"

    # Download full audio
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
        print("yt-dlp error:", result.stderr)
        return None

    if not audio_path.exists():
        return None

    # Split audio into chunks
    chunk_pattern = output_dir / f"{video_id}_chunk_%03d.mp3"

    split_command = [
        "ffmpeg",
        "-i", str(audio_path),
        "-f", "segment",
        "-segment_time", str(CHUNK_DURATION),
        "-c", "copy",
        str(chunk_pattern)
    ]

    subprocess.run(split_command, capture_output=True)

    full_transcript = ""

    chunk_files = sorted(output_dir.glob(f"{video_id}_chunk_*.mp3"))

    for chunk in chunk_files:
        print(f"Transcribing {chunk.name}")

        with open(chunk, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        full_transcript += transcript.text + " "

        chunk.unlink(missing_ok=True)

    audio_path.unlink(missing_ok=True)

    return full_transcript.strip()
