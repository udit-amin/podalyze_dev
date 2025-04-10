import requests
import os

def download_audio(url, episode_id):
    response = requests.get(url)
    path = f"/tmp/{episode_id}.mp3"
    with open(path, "wb") as f:
        f.write(response.content)
    return path
