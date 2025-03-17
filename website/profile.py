from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import ProfileSong, ProfileAlbum, ProfileArtist, Song, Album, Artist, Profiles

profile = Blueprint('profile', __name__)

@profile.route('/update-profile-content', methods=['POST'])
@login_required
def update_profile_content():
    """ Hanterar lägga till/ta bort låtar, album och artister i showcase """

    data = request.json
    action = data.get("action")  # 'add' eller 'remove'
    content_type = data.get("content_type")  # 'song', 'album' eller 'artist'
    content_id = data.get("content_id")  # ID från Spotify API, måste fixas!!!!!!!!!!!!!!!!
    content_data = data.get("content_data")  # Metadata från frontend (titel, artist, album, etc)

    if not content_id or not content_type:
        return jsonify({"error": "Missing content ID or type"}), 400

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

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
    """
    Hanterar profilbilden:
    - GET: Hämtar användarens aktuella profilbild.
    - POST: Uppdaterar användarens profilbild.
    """

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


@profile.route('/update-profile-bio', methods=['POST'])
@login_required
def update_profile_bio():
    """ Hanterar uppdatering eller tilläg av användarens bio. """

    data = request.json  # Tar emot JSON-data från frontend
    new_bio = data.get("bio")  # Hämtar den nya biotexten

    if not new_bio:
        return jsonify({"error": "Bio text is required"}), 400

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Uppdatera biotexten i databasen
    profile.bio = new_bio
    db.session.commit()

    return jsonify({"message": "Bio updated successfully"}), 200

@profile.route('/update-profile-genres', methods=['POST'])
@login_required
def update_profile_genres():
    """ Hanterar uppdatering eller tillägg av favoritgenrer i profilen. """

    data = request.json  # Tar emot JSON-data från frontend
    genres = data.get("genres")  # Lista med genrer

    if not genres or not isinstance(genres, list):
        return jsonify({"error": "Genres must be a list"}), 400

    profile = Profiles.query.filter_by(user_id=current_user.user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Uppdatera genrer i databasen
    profile.favorite_genres = genres
    db.session.commit()

    return jsonify({"message": "Genres updated successfully"}), 200
