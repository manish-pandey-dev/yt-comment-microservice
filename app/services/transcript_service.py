import subprocess
import os
import re
from pathlib import Path

def fetch_transcript(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    output_dir = Path("./tmp")
    output_dir.mkdir(exist_ok=True)

    command = [
        "yt-dlp",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--skip-download",
        "--output", str(output_dir / "%(id)s"),
        url
    ]

    subprocess.run(command, check=True)

    vtt_file = output_dir / f"{video_id}.en.vtt"

    if not vtt_file.exists():
        return None

    with open(vtt_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean VTT format
    text = clean_vtt(content)

    # Remove temp file
    vtt_file.unlink(missing_ok=True)

    return text


def clean_vtt(vtt_content: str) -> str:
    lines = vtt_content.splitlines()
    cleaned = []

    for line in lines:
        if "-->" in line:
            continue
        if line.strip().isdigit():
            continue
        if line.startswith("WEBVTT"):
            continue
        cleaned.append(line.strip())

    text = " ".join(cleaned)

    # Remove duplicate spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()