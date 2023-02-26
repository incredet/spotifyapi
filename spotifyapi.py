from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = requests.post(url, headers = headers, data = data)

    json_result = json.loads(result.content)
  
    token = json_result["access_token"]

    return token


def get_auth_header(token):
    """ """
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    """ """
    url = "https://api.spotify.com/v1/search"

    header = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = requests.get(query_url, headers = header)

    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
        print("sorry... that's too underground for spotify")
        return None
    return json_result[0]


def get_songs(token, artist_id):
    """ """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA"

    header = get_auth_header(token)

    result = requests.get(url, headers = header)

    json_result = json.loads(result.content)['tracks']

    return json_result




token = get_token()

result = search_for_artist(token, 'руся')

artist_id = result["id"]


songs = get_songs(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")