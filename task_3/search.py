""" search.py
"""
import folium
import pycountry
import pandas as pd
from geopy.geocoders import Nominatim
from spotifyapi_to_imp import get_token, search_for_artist, get_top_songs, search_track


def av_marks(artist_name: str) -> list:
    """ available markets
    """
    token = get_token()
    artist_id = search_for_artist(token, artist_name)["id"]
    top_song = get_top_songs(token, artist_id)[0]["name"]
    return [list(search_track(token, top_song)['album']['available_markets'])] + [[top_song]]


def format_country(counts: list):
    """ formats name of country
    """
    names = []
    for count in counts:
        country = pycountry.countries.get(alpha_2 = count)
        if country:
            names += [country.name]
    return names


def find_coords(path: str) -> None:
    """ finds coords
    """
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
    """ searches for coords in csv file
    """
    locs = []
    df = pd.read_csv(path)

    for name in names:
        locs += ((df.loc[df['Name'] == name]).values).tolist()
    return locs


def create_map(artist_name):
    """ main func (creates the map)
    """
    countries, track_name = av_marks(artist_name)
    names = format_country(countries)
    locs = coords_from_csv("task_3/coords.csv", names)
    music_map = folium.Map(zoom_start=10)
    html = """<h4>Track name: {}</h4>
    <h4>Country name: {}</h4>
    """
    for loc in locs:
        iframe = folium.IFrame(html=html.format(track_name[0],\
             loc[1].strip()), width=200, height=50)
        music_map.add_child(folium.Marker(location=[loc[-2], loc[-1]],\
            icon=folium.Icon(icon='star', color = 'lightgreen'), popup = folium.Popup(iframe)))
        music_map.save("task_3/templates/available_markets.html")
