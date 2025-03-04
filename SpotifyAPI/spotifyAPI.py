from dotenv import load_dotenv
import os
import base64
from requests import post, get
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
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"       #value av det jag söker (song_name, album_name) kan ha flera types (artist, track)

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_top_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result

def search_for_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={track_name}&type=track&limit=1"       #value av det jag söker (track_name, album_name) kan ha flera types (artist, track)

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]

    if len(json_result) == 0:
        print("No tracks with this name exists...")
        return None
    
    return json_result[0]

def search_for_album(token, album_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={album_name}&type=album&limit=1"       #value av det jag söker (track_name, album_name) kan ha flera types (artist, track)

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]

    if len(json_result) == 0:
        print("No albums with this name exists...")
        return None
    
    return json_result[0]

def print_track_info(token, track_name):
    result = search_for_track(token, track_name)
    print(result["name"])   #låtnamn
    print(result["album"]["images"][0]["url"])  #albumets bild
    print(result["artists"][0]["name"])    #artistnamn

def print_artist_info(token, artist_name):
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]
    top_songs = get_top_songs_by_artist(token, artist_id)
    for idx, song in enumerate(top_songs):      
        print(f"{idx + 1}. {song['name']}")
    print(result["images"][0]["url"])  #artistens profilbild

def print_album_info(token, album_name):
    result = search_for_album(token, album_name)
    print(result["name"])   #namn på album
    print(result["images"][0]["url"])   #bild på album
    print(result["artists"][0]["name"])    #artistnamn


token = get_token()

track_name = input("Name of the track?")
print_track_info(token, track_name)

artist_name = input("Name of the artist?")
print_artist_info(token, artist_name)

album_name = input("Name of the album?")
print_album_info(token, album_name)


'''
result = search_for_artist(token, "kent")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")'''