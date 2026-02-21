import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_comment(transcript: str) -> str:
    if not transcript:
        return None

    transcript_snippet = transcript[:3000]  # prevent huge payload

    prompt = f"""
You are a thoughtful YouTube viewer.

Create one meaningful comment based on this transcript.

Rules:
- Maximum 250 characters
- Mention one specific idea from the video
- No emojis
- No generic praise like "great video"
- Sound human, not AI
- No promotion

Transcript:
{transcript_snippet}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()