from .models import db, User, Profiles, ProfileSong, ProfileAlbum, ProfileArtist, Song, Album, Artist

def add_mock_data():
    """Lägger in mock-data i databasen om den saknas"""

    # Skapa en användare om den inte finns
    user = User.query.filter_by(user_id=1).first()
    if not user:
        user = User(username="q", email="q@q", password="q")
        db.session.add(user)
        db.session.commit()

    # Skapa en profil om den inte finns
    profile = Profiles.query.filter_by(user_id=user.user_id).first()
    if not profile:
        profile = Profiles(
            user_id=user.user_id,
            bio="This is a test bio",
            favorite_genres=["Rock", "Hip-Hop", "Electronic"],
            profile_picture="https://i1.sndcdn.com/avatars-000339644685-3ctegw-t500x500.jpg"
        )
        db.session.add(profile)
        db.session.commit()

    # Mock-sånger
    mock_songs = [
        {
            "song_id": "1",
            "title": "Test Song 1",
            "artist": "Test Artist",
            "cover_url": "https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac",
            "spotify_url": "https://open.spotify.com/track/1",
            "embed_url": "https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH"
        },
        {
            "song_id": "2",
            "title": "Test Song 2",
            "artist": "Another Artist",
            "cover_url": "https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac",
            "spotify_url": "https://open.spotify.com/track/2",
            "embed_url": "https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH"
        }
    ]

    # Lägg till låtar
    for song_data in mock_songs:
        song = Song.query.get(song_data["song_id"])
        if not song:
            song = Song(**song_data)
            db.session.add(song)
            db.session.commit()

        # Koppla låt till profilen om den inte redan finns
        if not ProfileSong.query.filter_by(profile_id=profile.profile_id, song_id=song.song_id).first():
            profile_song = ProfileSong(profile_id=profile.profile_id, song_id=song.song_id)
            db.session.add(profile_song)

    # Mock-album
    mock_albums = [
        {
            "album_id": "1",
            "title": "Test Album",
            "artist": "Test Artist",
            "cover_url": "https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac",
            "spotify_url": "https://open.spotify.com/album/0u7sgzvlLmPLvujXxy9EeY"
        }
    ]

    # Lägg till album
    for album_data in mock_albums:
        album = Album.query.get(album_data["album_id"])
        if not album:
            album = Album(**album_data)
            db.session.add(album)
            db.session.commit()

        # Koppla album till profilen om den inte redan finns
        if not ProfileAlbum.query.filter_by(profile_id=profile.profile_id, album_id=album.album_id).first():
            profile_album = ProfileAlbum(profile_id=profile.profile_id, album_id=album.album_id)
            db.session.add(profile_album)

    # Mock-artister
    mock_artists = [
        {
            "artist_id": "1",
            "name": "Test Artist",
            "cover_url": "https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c",
            "spotify_url": "https://open.spotify.com/artist/4KXp3xtaz1wWXnu5u34eVX"
        }
    ]

    # Lägg till artister
    for artist_data in mock_artists:
        artist = Artist.query.get(artist_data["artist_id"])
        if not artist:
            artist = Artist(**artist_data)
            db.session.add(artist)
            db.session.commit()

        # Koppla artist till profilen om den inte redan finns
        if not ProfileArtist.query.filter_by(profile_id=profile.profile_id, artist_id=artist.artist_id).first():
            profile_artist = ProfileArtist(profile_id=profile.profile_id, artist_id=artist.artist_id)
            db.session.add(profile_artist)

    # db.session.commit()
    print("Mock-data inlagd i databasen!")