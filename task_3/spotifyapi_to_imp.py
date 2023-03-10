""" lab 2 task 2 """
import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    """ this func gets token from spotify api request
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    res = requests.post(url, headers = headers, data = data)

    json_result = json.loads(res.content)

    return json_result["access_token"]


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


def search_track(token, track_name):
    """ """
    url = url = "https://api.spotify.com/v1/search"

    header = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    query_url = url + query

    result = requests.get(query_url, headers = header)

    json_result = json.loads(result.content)['tracks']['items']
    if len(json_result) == 0:
        print("sorry... that's too underground for spotify")
        return None
    return json_result[0]

def get_top_songs(token, artist_id):
    """ """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=UA"
    header = get_auth_header(token)
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def available_markets(track):
    """ """
    markets = track['album']['available_markets']
    object_is_list(markets)
    return None


def artist_albums(token, artist_id):
    """ """
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    header = get_auth_header(token)
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)['items']
    return json_result

def track_info(token, track_id):
    """ """
    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    header = get_auth_header(token)
    result = requests.get(url, headers = header)
    json_result = json.loads(result.content)
    print(json_result)
    return json_result


def object_is_list(obj):
    """ """
    print("requested object is a list. enter an index of press -1 to see all values")
    while True:
        try:
            indx = int(input())
            if indx != -1:
                print(f"requested value: {obj[idx]}")
                return None
            for indx, value in enumerate(obj):
                print(f"{indx + 1}. {value}")
            return None
        except ValueError:
            break
    return None


def object_is_object(obj):
    """ """
    print("the requested object is a object")
    print("available options:")
    ignore = ['disc_number', 'uri', 'type', 'is_local',\
 'href', 'external_urls', 'external_ids', 'preview_url']
    keyys = [item for item in list(obj.keys()) if item not in ignore]
    for indx, keyy in enumerate(keyys):
        print(f"{indx + 1}. {keyy}")
    try:
        indx = int(input())
        rec = obj[keyys[indx - 1]]
        if isinstance(rec, list):
            object_is_list(rec)
        elif isinstance(rec, dict):
            object_is_object(rec)
        else:
            print(rec)
    except ValueError:
        return None

if __name__ == "__main__":

    print("hi! get to know your favorite artist! what's their name?")
    token = get_token()
    while True:
        try:
            artist_name = input()
            result = search_for_artist(token, artist_name)
            artist_id = result["id"]
            songs = get_top_songs(token, artist_id)
            print("choose what you want you know about them:")
            keys = list(result.keys())
            keys = [keys[i] for i in [1, 2, 4, 8]]
            keys += [
                "most popular song", "top ten tracks",
                "available markets(the most popular song)",
                "albums",
                "info about most popular song"
            ]
            for idx, key in enumerate(keys):
                print(f"{idx + 1}. {key}")
            print("enter the index")
            try:
                index = int(input())
            except ValueError:
                break
            if index < 5:
                request = result[keys[index - 1]]
                if isinstance(request, list):
                    object_is_list(request)
                elif isinstance(request, dict):
                    object_is_object(request)
                else:
                    print(request)
            elif index == 5:
                name = result['name']
                print(f"the most popular song by {name} is \"{songs[0]['name']}\"")
            elif index == 6:
                for idx, song in enumerate(songs):
                    print(f"{idx + 1}. {song['name']}")
            elif index == 7:
                track = search_track(token, songs[0]["name"])
                available_markets(track)
            elif index == 8:
                albums = artist_albums(token, artist_id)
                for idx, album in enumerate(albums[::-1]):
                    print(f"{idx + 1}. {album['name']}")
            elif index == 9:
                track = search_track(token, songs[0]["name"])
                object_is_object(track)
            print("press Enter to end or input the next artist")
        except KeyError:
            break
        except AttributeError:
            break
        except TypeError:
            break
