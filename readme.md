
# AI YouTube Comment Microservice

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-framework-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-development-orange)

🚧 Project Status: Active Development

An AI-powered microservice that monitors YouTube channels, analyzes new videos, generates meaningful comments using AI, and posts them after manual approval.

The system runs locally on a **Raspberry Pi** and can later be deployed to **Google Cloud Run**.

---

# Features

- Detect new videos from a YouTube channel
- Download audio using `yt-dlp`
- Chunk long audio using `ffmpeg`
- AI transcription for long videos
- AI summarization of transcripts
- AI-generated YouTube comments
- Hindi / Devanagari comment generation
- Manual approval workflow
- Post comments via official YouTube API
- OAuth-based authentication
- Cloud-ready microservice architecture

---

# System Architecture

```mermaid
flowchart TD

A[YouTube Channel] --> B[Video Detection API]
B --> C[Download Audio yt-dlp]
C --> D[Chunk Audio ffmpeg]
D --> E[AI Transcription]
E --> F[AI Summary Generation]
F --> G[AI Comment Generation]
G --> H[Database Storage]
H --> I[Manual Approval]
I --> J[Post Comment via YouTube API]
````

---

# Tech Stack

| Component        | Technology                        |
| ---------------- | --------------------------------- |
| Backend          | FastAPI                           |
| Database         | SQLite                            |
| AI               | OpenAI API                        |
| Video Download   | yt-dlp                            |
| Audio Processing | ffmpeg                            |
| Authentication   | Google OAuth2                     |
| Deployment       | Raspberry Pi / Docker / Cloud Run |

---

# Project Structure

```
yt-comment-microservice

app/
 ├── main.py
 ├── api/
 │     ├── auth.py
 │     └── comments.py
 ├── services/
 │     ├── youtube_service.py
 │     ├── transcript_service.py
 │     ├── ai_service.py
 │     ├── oauth_service.py
 │     └── youtube_post_service.py
 └── db/
       ├── models.py
       └── database.py
```

---

# Installation

## 1 Clone Repository

```
git clone https://github.com/manish-pandey-dev/yt-comment-microservice.git
cd yt-comment-microservice
```

---

# 2 Create Python Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

# 3 Install Dependencies

```
pip install -r requirements.txt
```

---

# 4 Install System Dependencies

```
sudo apt install ffmpeg
sudo apt install yt-dlp
```

---

# Environment Configuration

Create `.env` file in the root folder.

```
OPENAI_API_KEY=

YOUTUBE_API_KEY=
YOUTUBE_CHANNEL_ID=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

---

# Run Application

```
uvicorn app.main:app --reload --port 8000
```

Open the API documentation:

```
http://localhost:8000/docs
```

---

# OAuth Setup

1. Open **Google Cloud Console**
2. Enable **YouTube Data API v3**
3. Create OAuth credentials
4. Add redirect URI:

```
http://localhost:8000/auth/callback
```

Then authenticate:

```
http://localhost:8000/auth/login
```

---

# Workflow

## Detect New Video

```
GET /check
```

---

# View Pending Comments

```
GET /comments/pending
```

---

# Approve Comment

```
POST /comments/{id}/approve
```

---

# Post Comment

```
POST /comments/{id}/post
```

---

# Example AI Comment

```
यह वीडियो एक महत्वपूर्ण बात समझाता है कि पूजा-पाठ का उद्देश्य केवल भौतिक लाभ नहीं बल्कि आत्मचिंतन होना चाहिए।
```

---

# Future Improvements

* Automatic channel monitoring
* Language detection
* Background job queue
* Web dashboard
* Multi-channel support
* Cloud deployment
* Scheduled automation

---

# Deployment Options

## Raspberry Pi

Run locally using FastAPI.

## Docker

Containerized deployment.

## Google Cloud Run

Serverless deployment for scalable workloads.

---

# Screenshots (Optional)

You can later add screenshots here showing:

* FastAPI documentation page
* Comment approval workflow
* Database tables
* Example AI-generated comment

---

# Author

Manish Pandey

GitHub
[https://github.com/manish-pandey-dev](https://github.com/manish-pandey-dev)

````

---

# After Pasting

Run:

```bash
git add README.md
git commit -m "Added professional README"
git push
````

------------------------------------



To connect from remote machine :
ssh manish651@raspberrypiMKP or
ssh manish651@192.168.1.167
---It will ask for pw give pw, pw is in onepass 



Navigate to project folder :
cd github-projects/yt-comment-microservice/



To start the server :
source venv/bin/activate
uvicorn app.main:app --reload --port 8000



To connect to DB:
navigate to same folder
sqlite3 app.db


DB Commands :
to see the list of tables - .tables
to schema structure - .schema
to table structure - .schema videos
to quite from db - .quit




------------------------------------
git status
git add .
git commit -m "Add project README and documentation"
git push origin main
git tag -a v0.1.0 -m "Initial working version with AI transcription and comment generation"
git push origin v0.1.0
git tag