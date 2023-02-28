import folium
import json
import pycountry
import pandas as pd
from geopy.geocoders import Nominatim
from spotifyapi_to_imp import get_token, search_for_artist, get_top_songs, search_track


def av_marks(artist_name: str) -> list:
    """ """
    token = get_token()
    artist_id = search_for_artist(token, artist_name)["id"]
    top_song = get_top_songs(token, artist_id)[0]["name"]
    return list(search_track(token, top_song)['album']['available_markets'])


def format_country(countries: list):
    """ """
    pass


def find_coords(path: str) -> None:
    """ """
    locations = []
    with open(path, "r", encoding = "utf-8") as countries:
        countries_list = countries.readlines()
    geolocator = Nominatim(user_agent="map")
    for line in countries_list:
        location = geolocator.geocode(line)
        locations+= [[line.replace("\n", ""), location.latitude, location.longitude]]
    df = pd.DataFrame(locations, columns=["Name", "Lat", "Lon"])
    df.to_csv("task_3/coords.csv", sep=',', encoding='utf-8')


def coords_from_csv(path: str, names: str): 
    """ """
    locs = []
    df = pd.read_csv(path)

    for name in names:
        locs += ((df.loc[df['Name'] == name]).values).tolist()
    return locs


def create_map(locs):
    """ """
    music_map = folium.Map(zoom_start=5)
    for loc in locs:
        music_map.add_child(folium.Marker(location=[loc[-2], loc[-1]]))
        music_map.save("Map_Marker_irynka2.html")

names = ["Ukraine", "Poland"]

create_map(coords_from_csv("task_3/coords.csv", names))

# print(av_marks("Taylor Swift"))
