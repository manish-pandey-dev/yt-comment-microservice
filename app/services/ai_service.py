import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_transcript(transcript: str) -> str:
    if not transcript:
        return None

    prompt = f"""
You are analyzing a YouTube video transcript.

Create a structured summary with:

1. 8-12 key bullet points
2. Main argument of the speaker
3. One surprising or strong insight

Keep it concise but information-rich.

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def generate_comment(summary: str) -> str:
    if not summary:
        return None

    prompt = f"""
You are a thoughtful YouTube viewer.

Write ONE meaningful YouTube comment based on this summary.

IMPORTANT:
- Write in the same language as the original video.
- If the video is Hindi, write in proper Devanagari script.
- Max 250 characters.
- Mention one specific idea.
- No emojis.
- No generic praise.
- No promotion.
- Sound natural and human.

Summary:
{summary}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
