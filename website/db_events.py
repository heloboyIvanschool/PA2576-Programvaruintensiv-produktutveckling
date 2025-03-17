from sqlalchemy import event
from .models import ProfileSong, Song, ProfileAlbum, Album, ProfileArtist, Artist
from .__init__ import db

def remove_unused_entries(mapper, connection, target, content_type):
    """ Tar bort låtar, album eller artister från databasen om ingen längre refererar till dem. """
    model_map = {
        "song": (ProfileSong, Song, "song_id"),
        "album": (ProfileAlbum, Album, "album_id"),
        "artist": (ProfileArtist, Artist, "artist_id")
    }

    profile_model, main_model, column = model_map[content_type]

    entry_in_use = profile_model.query.filter_by(**{column: getattr(target, column)}).first()
    if not entry_in_use:
        db.session.delete(main_model.query.get(getattr(target, column)))
        db.session.commit()

# Lyssna på radering av låtar, album och artister
@event.listens_for(ProfileSong, 'after_delete')
def remove_unused_songs(mapper, connection, target):
    remove_unused_entries(mapper, connection, target, "song")

@event.listens_for(ProfileAlbum, 'after_delete')
def remove_unused_albums(mapper, connection, target):
    remove_unused_entries(mapper, connection, target, "album")

@event.listens_for(ProfileArtist, 'after_delete')
def remove_unused_artists(mapper, connection, target):
    remove_unused_entries(mapper, connection, target, "artist")
