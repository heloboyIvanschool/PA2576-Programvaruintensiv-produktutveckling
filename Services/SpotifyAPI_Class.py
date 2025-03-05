#pip install requests
#pip install python-dotenv

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


class spotifyAPI:
    def __init__(self):
        load_dotenv()
        self.__client_id = os.getenv("CLIENT_ID")
        self.__client_secret = os.getenv("CLIENT_SECRET")

    def get_token(self):
        auth_string = self.__client_id + ":" + self.__client_secret
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

class search():
    def __init__(self):
        self.__token = spotifyAPI().get_token()
        self.__url = "https://api.spotify.com/v1/search"

    def get_auth_header(self):
        return {"Authorization": "Bearer " + self.__token}

    def get_query_url(self, query):
        query_url = self.__url + "?" + query
        result = get(query_url, headers=self.get_auth_header())
        return result


#Search for track


class search_for_track():
    def __init__(self):
        self.__search_instance = search()

    def get_query(self, track_name):
        query = f"q={track_name}&type=track&limit=1"
        return query

    def get_json(self, track_name):
        json_result = json.loads((self.__search_instance.get_query_url(self.get_query(track_name))).content)["tracks"]["items"]

        if len(json_result) == 0:
            print("No tracks with this name exists...")
            return None

        return json_result[0]

    def get_track_name(self, track_name):
        track_data = self.get_json(track_name)
        return track_data["name"] if track_data else None

    def get_track_artist(self, track_name):
        track_data = self.get_json(track_name)
        return track_data["artists"][0]["name"] if track_data else None

    def get_track_album(self, track_name):
        track_data = self.get_json(track_name)
        return track_data["album"]["name"] if track_data else None

    def get_track_cover(self, track_name):
        track_data = self.get_json(track_name)
        return track_data["album"]["images"][0]["url"] if track_data else None


#Search for Album


class search_for_album():
    def __init__(self):
        self.__search_instance = search()

    def get_query(self, album_name):
        query = f"q={album_name}&type=album&limit=1"
        return query

    def get_json(self, album_name):
        json_result = json.loads((self.__search_instance.get_query_url(self.get_query(album_name))).content)["albums"]["items"]

        if len(json_result) == 0:
            print("No albums with this name exists...")
            return None

        return json_result[0]

    def get_album_name(self, album_name):
        album_data = self.get_json(album_name)
        return album_data["name"] if album_data else None

    def get_album_artist(self, album_name):
        album_data = self.get_json(album_name)
        return album_data["artists"][0]["name"] if album_data else None

    def get_album_cover(self, album_name):
        album_data = self.get_json(album_name)
        return album_data["images"][0]["url"] if album_data else None


#Search for artist


class search_for_artist():
    def __init__(self):
        self.__search_instance = search()

    def get_query(self, artist_name):
        query = f"q={artist_name}&type=artist&limit=1"
        return query

    def get_json(self, artist_name):
        json_result = json.loads((self.__search_instance.get_query_url(self.get_query(artist_name))).content)["artists"]["items"]

        if len(json_result) == 0:
            print("No artists with this name exists...")
            return None

        return json_result[0]

    def get_artist_name(self, artist_name):
        artist_data = self.get_json(artist_name)
        return artist_data["name"] if artist_data else None

    def get_artist_cover(self, artist_name):
        artist_data = self.get_json(artist_name)
        return artist_data["images"][0]["url"] if artist_data else None




spotify_search_for_track = search_for_track()

track_name = "Om du var här"

print("\n---------------Låtinfo---------------")

print("Låtnamn:", spotify_search_for_track.get_track_name(track_name))
print("Artist:", spotify_search_for_track.get_track_artist(track_name))
print("Album:", spotify_search_for_track.get_track_album(track_name))
print("Coverbild:", spotify_search_for_track.get_track_cover(track_name))



spotify_search_for_album = search_for_album()

album_name = "Brothers in arms"

print("\n---------------Albuminfo---------------")

print("Albumnamn:", spotify_search_for_album.get_album_name(album_name))
print("Artist:", spotify_search_for_album.get_album_artist(album_name))
print("Coverbild:", spotify_search_for_album.get_album_cover(album_name))



spotify_search_for_artist = search_for_artist()

artist_name = "kent"

print("\n---------------Artistinfo---------------")

print("Artistnamn:", spotify_search_for_artist.get_artist_name(artist_name))
print("Coverbild:", spotify_search_for_artist.get_artist_cover(artist_name))

