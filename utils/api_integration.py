import requests
import os

 
API_KEY = os.getenv("CRICBUZZ_API_KEY", "d796d360e4msh8060d58be8bed38p172e52jsn679a3df8b9d4")

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": 'd796d360e4msh8060d58be8bed38p172e52jsn679a3df8b9d4'
}

def fetch_live_matches():
    """Fetch ongoing live matches"""
    url = f"{BASE_URL}/matches/v1/live"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def fetch_series():
    """Fetch ongoing/upcoming cricket series"""
    url = f"{BASE_URL}/series/v1/international"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def fetch_player_stats(player_id: int):
    """Fetch individual player stats by ID"""
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
