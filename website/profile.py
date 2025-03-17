from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import ProfileSong, ProfileAlbum, ProfileArtist, Song, Album, Artist, Profiles

profile = Blueprint('profile', __name__)

@profile.route('/profile-content', methods=['GET', 'POST'])
@login_required
def profile_content():
    """
    Hanterar showcase-innehåll:
    - GET: Hämtar användarens låtar, album och artister i showcase.
    - POST: Lägger till eller tar bort låtar, album eller artister från showcase.
    """

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        # Hämta användarens showcase-innehåll
        songs = [
            {"song_id": entry.song_id, "title": entry.song.title, "artist": entry.song.artist, "cover_url": entry.song.cover_url, "spotify_url": entry.song.spotify_url}
            for entry in ProfileSong.query.filter_by(profile_id=profile.profile_id).join(Song).all()
        ]
        albums = [
            {"album_id": entry.album_id, "title": entry.album.title, "artist": entry.album.artist, "cover_url": entry.album.cover_url, "spotify_url": entry.album.spotify_url}
            for entry in ProfileAlbum.query.filter_by(profile_id=profile.profile_id).join(Album).all()
        ]
        artists = [
            {"artist_id": entry.artist_id, "name": entry.artist.name, "cover_url": entry.artist.cover_url, "spotify_url": entry.artist.spotify_url}
            for entry in ProfileArtist.query.filter_by(profile_id=profile.profile_id).join(Artist).all()
        ]

        return jsonify({
            "songs": songs,
            "albums": albums,
            "artists": artists
        }), 200

    elif request.method == 'POST':
        data = request.json
        action = data.get("action")  # 'add' eller 'remove'
        content_type = data.get("content_type")  # 'song', 'album' eller 'artist'
        content_id = data.get("content_id")  # ID från Spotify API
        content_data = data.get("content_data")  # Metadata från frontend (titel, artist, album, etc)

        if not content_id or not content_type:
            return jsonify({"error": "Missing content ID or type"}), 400

        # Välj rätt tabell och kolumn baserat på content_type
        model_map = {
            "song": (ProfileSong, Song, "song_id"),
            "album": (ProfileAlbum, Album, "album_id"),
            "artist": (ProfileArtist, Artist, "artist_id")
        }

        if content_type not in model_map:
            return jsonify({"error": "Invalid content type"}), 400

        profile_model, main_model, column = model_map[content_type]

        if action == "add":
            # Kolla om objektet redan finns i databasen
            existing_item = main_model.query.filter_by(**{column: content_id}).first()

            # Om objektet inte finns, lägg till det
            if not existing_item:
                if not content_data:
                    return jsonify({"error": f"Missing {content_type} data"}), 400

                new_item = main_model(**{
                    column: content_id,
                    "title" if content_type != "artist" else "name": content_data.get("title") or content_data.get("name"),
                    "artist": content_data.get("artist") if content_type != "artist" else None,
                    "cover_url": content_data.get("cover_url"),
                    "spotify_url": content_data.get("spotify_url")
                })
                db.session.add(new_item)

            # Lägg till referens i användarens profil
            existing_entry = profile_model.query.filter_by(profile_id=profile.profile_id, **{column: content_id}).first()
            if existing_entry:
                return jsonify({"message": f"{content_type.capitalize()} already in showcase"}), 200

            new_entry = profile_model(profile_id=profile.profile_id, **{column: content_id})
            db.session.add(new_entry)

        elif action == "remove":
            existing_entry = profile_model.query.filter_by(profile_id=profile.profile_id, **{column: content_id}).first()
            if existing_entry:
                db.session.delete(existing_entry)

        else:
            return jsonify({"error": "Invalid action"}), 400

        db.session.commit()
        return jsonify({"message": f"{content_type.capitalize()} updated successfully"}), 200

@profile.route('/profile-picture', methods=['GET', 'POST'])
@login_required
def profile_picture():

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        # Returnerar nuvarande profilbild
        return jsonify({"profile_picture": profile.profile_picture}), 200

    elif request.method == 'POST':
        data = request.json
        profile_picture_url = data.get("profile_picture")

        if not profile_picture_url:
            return jsonify({"error": "No profile picture URL provided"}), 400

        # Uppdaterar profilbilden i databasen
        profile.profile_picture = profile_picture_url
        db.session.commit()

        return jsonify({
            "message": "Profile picture updated successfully",
            "profile_picture": profile.profile_picture
        }), 200

@profile.route('/profile-bio', methods=['GET', 'POST'])
@login_required
def profile_bio():
    """
    Hanterar biografi:
    - GET: Hämtar användarens bio.
    - POST: Uppdaterar användarens bio.
    """

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        return jsonify({"bio": profile.bio}), 200

    elif request.method == 'POST':
        data = request.json
        new_bio = data.get("bio")

        if not new_bio:
            return jsonify({"error": "Bio text is required"}), 400

        profile.bio = new_bio
        db.session.commit()

        return jsonify({
            "message": "Bio updated successfully",
            "bio": profile.bio
        }), 200

@profile.route('/profile-genres', methods=['GET', 'POST'])
@login_required
def profile_genres():
    """
    Hanterar favoritgenrer:
    - GET: Hämtar användarens favoritgenrer.
    - POST: Uppdaterar eller lägger till nya favoritgenrer.
    """

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        return jsonify({"favorite_genres": profile.favorite_genres or []}), 200

    elif request.method == 'POST':
        data = request.json
        genres = data.get("genres")

        if not genres or not isinstance(genres, list):
            return jsonify({"error": "Genres must be a list"}), 400

        profile.favorite_genres = genres
        db.session.commit()

        return jsonify({
            "message": "Genres updated successfully",
            "favorite_genres": profile.favorite_genres
        }), 200
