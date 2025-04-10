# Podalyze

🎙️ Podalyze is a full-stack podcast summarizer and episode Q&A engine powered by OpenAI and Spotify.

## Features
- Spotify OAuth login
- Fetch saved shows and episodes
- Transcribe episodes using Whisper
- Speaker diarization (mock or WhisperX/pyannote support ready)
- Store transcripts as vector embeddings
- RAG-based Q&A from raw transcript
- Optional summarization on demand

## Deployment
Podalyze is deployable via Docker on AWS EC2, ECS, or any container environment.

### Local Setup
```bash
git clone https://github.com/udit-amin/podalyze_dev.git
cd podalyze_dev
touch .env.local  # Add your secrets here
docker build -t podalyze .
docker run -p 8000:8000 --env-file .env.local podalyze
```

## Environment Variables
Add these to `.env.local`:
```
CLIENT_ID=
CLIENT_SECRET=
OPENAI_API_KEY=
```

## API Routes
- `GET /auth-url` – Get Spotify login URL
- `GET /callback?code=...` – Spotify redirect
- `GET /show/{show_id}/episodes` – Episode list
- `POST /episode/{episode_id}/transcribe` – Transcribe and index
- `POST /episode/{episode_id}/ask` – Ask questions or request summary

---

### LICENSE
MIT License. See `LICENSE` file for details.
