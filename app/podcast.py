import requests

def get_saved_shows(access_token, limit=20):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.spotify.com/v1/me/shows"
    
    saved_shows = []
    offset = 0

    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        saved_shows.extend(data["items"])
        if data["next"] is None:
            break
        offset += limit

    return saved_shows

def get_episodes_for_show(access_token, show_id, limit=20):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/shows/{show_id}/episodes"
    
    episodes = []
    offset = 0

    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        episodes.extend(data["items"])
        if data["next"] is None:
            break
        offset += limit

    return episodes
