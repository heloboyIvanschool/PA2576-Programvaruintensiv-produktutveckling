import os
import json
import base64
import requests
from flask import Flask, request, jsonify, Blueprint
from dotenv import load_dotenv

# Skapar en Blueprint för Spotify-hantering
SpotifyHandler = Blueprint('SpotifyHandler', __name__)

# Laddar miljövariabler från .env-filen
load_dotenv()

class SpotifyAPI:
    """
    Hanterar autentisering och anrop till Spotifys API.
    """
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.token = self.get_token()

    def get_token(self):
        """
        Hämtar en åtkomsttoken från Spotify via client credentials-flödet.
        """
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            print("Error fetching Spotify token:", response.json())
            return None

        return response.json().get("access_token")

    def search(self, query, search_type):
        """
        Utför en sökning på Spotify för angiven typ (track, album, artist).

        Args:
            query (str): Sökterm.
            search_type (str): Typ av sökning – 'track', 'album' eller 'artist'.

        Returns:
            dict | None: Första sökresultatet eller None.
        """
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": query, "type": search_type, "limit": 1}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching {search_type}: ", response.json())
            return None

        return response.json().get(search_type + "s", {}).get("items", [None])[0]


class SpotifySearch:
    """
    Wrapper-klass som förenklar hämtning av olika typer av Spotify-data.
    """
    def __init__(self, query):
        self.spotify = SpotifyAPI()
        self.query = query

    def get_track(self):
        """
        Hämtar låtinformation från Spotify.
        """
        track_data = self.spotify.search(self.query, "track")
        if not track_data:
            return None

        return {
            "name": track_data["name"],
            "artist": ", ".join(artist["name"] for artist in track_data["artists"]),
            "album": track_data["album"]["name"],
            "cover_url": track_data["album"]["images"][0]["url"] if track_data["album"]["images"] else None,
            "embed_link": f"https://open.spotify.com/embed/track/{track_data['id']}"
        }

    def get_album(self):
        """
        Hämtar albuminformation från Spotify.
        """
        album_data = self.spotify.search(self.query, "album")
        if not album_data:
            return None

        return {
            "name": album_data["name"],
            "artist": ", ".join(artist["name"] for artist in album_data["artists"]),
            "release_date": album_data["release_date"],
            "cover_url": album_data["images"][0]["url"] if album_data["images"] else None,
            "spotify_link": album_data["external_urls"]["spotify"]
        }

    def get_artist(self):
        """
        Hämtar artistinformation från Spotify.
        """
        artist_data = self.spotify.search(self.query, "artist")
        if not artist_data:
            return None

        return {
            "name": artist_data["name"],
            "genres": artist_data["genres"],
            "popularity": artist_data["popularity"],
            "followers": artist_data["followers"]["total"],
            "image_url": artist_data["images"][0]["url"] if artist_data["images"] else None,
            "spotify_link": artist_data["external_urls"]["spotify"]
        }


# Route för att söka efter låtar, album eller artister via API:et
@SpotifyHandler.route('/search', methods=['GET'])
def search():
    """
    API-endpoint för att söka efter en låt, ett album eller en artist.

    Förväntar sig query-parametrar:
    - query: söksträngen
    - type: 'track', 'album' eller 'artist'

    Returns:
        JSON-resultat med relevant data eller felmeddelande.
    """
    query = request.args.get('query')
    search_type = request.args.get('type')

    if not query or search_type not in ["track", "album", "artist"]:
        return jsonify({"error": "Ange en giltig query och typ (track, album, artist)"}), 400

    search_instance = SpotifySearch(query)
    result = None

    if search_type == "track":
        result = search_instance.get_track()
    elif search_type == "album":
        result = search_instance.get_album()
    elif search_type == "artist":
        result = search_instance.get_artist()

    if not result:
        return jsonify({"error": f"Inga resultat hittades för {query}"}), 404

    return jsonify(result)