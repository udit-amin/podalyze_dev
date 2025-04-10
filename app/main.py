from fastapi import FastAPI
from app.auth import SpotifyUserAuth, start_local_server
from app.podcast import get_saved_shows, get_episodes_for_show
from app.transcriber import transcribe_and_store_segments
from app.vectorstore import ask_about_episode, summarize_episode_transcript
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

@app.get("/")
def index():
    return {"message": "Welcome to Podalyze"}

@app.get("/auth-url")
def auth_url():
    auth = SpotifyUserAuth(CLIENT_ID, CLIENT_SECRET)
    return {"url": auth.get_auth_url()}

@app.get("/callback")
def callback(code: str):
    auth = SpotifyUserAuth(CLIENT_ID, CLIENT_SECRET)
    tokens = auth.exchange_code_for_token(code)
    shows = get_saved_shows(tokens["access_token"])
    return {"shows": [s["show"]["name"] for s in shows]}

@app.get("/show/{show_id}/episodes")
def episodes(show_id: str, token: str):
    return get_episodes_for_show(token, show_id)

@app.post("/episode/{episode_id}/transcribe")
def transcribe_episode(episode_id: str, audio_url: str):
    segments = transcribe_and_store_segments(audio_url, episode_id)
    return {"segments": segments}

@app.post("/episode/{episode_id}/ask")
def ask(episode_id: str, question: str):
    if "summarize" in question.lower():
        return {"summary": summarize_episode_transcript(episode_id)}
    answer = ask_about_episode(episode_id, question)
    return {"answer": answer}