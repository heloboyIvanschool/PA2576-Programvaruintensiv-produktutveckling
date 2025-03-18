from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import ProfileSong, ProfileAlbum, ProfileArtist, Song, Album, Artist, Profiles

profile = Blueprint('profile', __name__)

# hämtar just nu all data, måste då uppdatera resterande kod om vi ska göra såhär
@profile.route('/api/profile', methods=['GET'])
@login_required
def get_full_profile():
    """Hämtar all profilinfo i ett anrop"""
    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

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
        "username": current_user.username,
        "profile_picture": profile.profile_picture or "https://i1.sndcdn.com/avatars-000339644685-3ctegw-t500x500.jpg",
        "bio": profile.bio or "",
        "favorite_genres": profile.favorite_genres or [],
        "songs": songs,
        "albums": albums,
        "artists": artists
    }), 200

@profile.route('/api/profile-showcase', methods=['GET', 'POST'])
@login_required
def profile_content():
    """ Hanterar showcase-innehåll: Hämtar, lägger till och tar bort låtar, album och artister. """
    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
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
            "message": "Showcase retrieved successfully",
            "songs": songs or [],
            "albums": albums or [],
            "artists": artists or []
        }), 200

    elif request.method == 'POST':
        data = request.get_json()
        action = data.get("action")  # 'add' eller 'remove'
        content_type = data.get("content_type")  # 'song', 'album' eller 'artist'
        content_id = data.get("content_id")  # ID från Spotify API
        content_data = data.get("content_data")  # Metadata från frontend

        if not content_id or not content_type:
            return jsonify({"error": "Missing content ID or type"}), 400

        model_map = {
            "song": (ProfileSong, Song, "song_id"),
            "album": (ProfileAlbum, Album, "album_id"),
            "artist": (ProfileArtist, Artist, "artist_id")
        }

        if content_type not in model_map:
            return jsonify({"error": "Invalid content type"}), 400

        profile_model, main_model, column = model_map[content_type]

        if action == "add":
            existing_item = main_model.query.filter_by(**{column: content_id}).first()
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
                return jsonify({"error": f"{content_type.capitalize()} not found in showcase"}), 404

        else:
            return jsonify({"error": "Invalid action"}), 400

        db.session.commit()
        return jsonify({"message": f"{content_type.capitalize()} updated successfully"}), 200

@profile.route('/api/profile-picture', methods=['GET', 'POST'])
@login_required
def profile_picture():
    """ Hanterar profilbild: Hämtar eller uppdaterar. """
    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        return jsonify({"profile_picture": profile.profile_picture or "https://i1.sndcdn.com/avatars-000339644685-3ctegw-t500x500.jpg"}), 200

    elif request.method == 'POST':
        data = request.get_json()
        profile_picture_url = data.get("profile_picture")

        if not profile_picture_url:
            return jsonify({"error": "No profile picture URL provided"}), 400

        profile.profile_picture = profile_picture_url
        db.session.commit()

        return jsonify({
            "message": "Profile picture updated successfully",
            "profile_picture": profile.profile_picture
        }), 200

@profile.route('/api/profile-bio', methods=['GET', 'POST'])
@login_required
def profile_bio():
    """ Hanterar användarens biografi. """
    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        return jsonify({"bio": profile.bio or ""}), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_bio = data.get("bio")

        if not new_bio:
            return jsonify({"error": "Bio text is required"}), 400

        profile.bio = new_bio
        db.session.commit()

        return jsonify({
            "message": "Bio updated successfully",
            "bio": profile.bio
        }), 200

@profile.route('/api/profile-genres', methods=['GET', 'POST'])
@login_required
def profile_genres():
    """ Hanterar favoritgenrer. """
    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    if request.method == 'GET':
        return jsonify({"favorite_genres": profile.favorite_genres or []}), 200

    elif request.method == 'POST':
        data = request.get_json()
        genres = data.get("genres")

        if not genres or not isinstance(genres, list):
            return jsonify({"error": "Genres must be a list"}), 400

        if not all(isinstance(genre, str) for genre in genres):
            return jsonify({"error": "All genres must be strings"}), 400

        profile.favorite_genres = genres
        db.session.commit()

        return jsonify({
            "message": "Genres updated successfully",
            "favorite_genres": profile.favorite_genres
        }), 200
