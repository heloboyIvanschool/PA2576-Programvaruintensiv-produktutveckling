from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True) # ifall man ändrar typen av nyckeln så msåte detta även ske i alla andra tabeller där nycklen används
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String, nullable=True)
    favorite_genres = db.Column(db.PickleType, nullable=True)
    createdAt = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.String(50), default='user')

    #realations
    posts = db.relationship('Post', back_populates='user')
    likes = db.relationship('Like', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

class Profiles(db.Model):
    __tablename__ = 'profiles'
    profileId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), nullable=False)
    bio = db.Column(db.String(500), nullable=True)


class Post(db.Model):
    __tablename__ = 'posts'
    postId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    songId = db.Column(db.String, db.ForeignKey('songs.songId'), nullable=True)
    caption = db.Column(db.Text, nullable=True)
    likes = db.Column(db.Integer, default=0)
    createdAt = db.Column(db.DateTime(timezone=True), default=func.now())

    #realations
    user = db.relationship('User', back_populates='posts')
    likes = db.relationship('Like', back_populates='post', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")
    song = db.relationship('Song', back_populates='posts')

class Like(db.Model):
    __tablename__ = 'likes'
    likeId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)

    #relations
    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

class Comment(db.Model):
    __tablename__ = 'comments'
    commentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('posts.postId'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), default=func.now())

    #realtions
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

class Song(db.Model):
    __tablename__ = 'songs'
    songId = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=True)
    coverUrl = db.Column(db.String, nullable=True)
    spotifyUrl = db.Column(db.String, nullable=False)

    #relations
    posts = db.relationship('Post', back_populates='song', cascade="all, delete-orphan")

class ProfileSong(db.Model):
    __tablename__ = 'profile_songs'
    id = db.Column(db.Integer, primary_key=True)  # Unikt ID
    profileId = db.Column(db.Integer, db.ForeignKey('profiles.profileId', ondelete="CASCADE"), nullable=False)  # Användarens profil
    songId = db.Column(db.String, db.ForeignKey('songs.songId', ondelete="CASCADE"), nullable=False)  # Länk till låten i `songs`

user_songs = db.Table(
    'user_songs',
    db.Column('userId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
    db.Column('songId', db.String, db.ForeignKey('songs.songId', ondelete="CASCADE"), primary_key=True)
)

class Album(db.Model):
    __tablename__ = 'albums'
    albumId = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    coverUrl = db.Column(db.String, nullable=True)
    spotifyUrl = db.Column(db.String, nullable=False)

class ProfileAlbum(db.Model):
    __tablename__ = 'profile_albums'
    id = db.Column(db.Integer, primary_key=True)  # Unikt ID
    profileId = db.Column(db.Integer, db.ForeignKey('profiles.profileId', ondelete="CASCADE"), nullable=False)  # Användarens profil
    profileId = db.Column(db.String, db.ForeignKey('songs.songId', ondelete="CASCADE"), nullable=False)

user_albums = db.Table(
    'profile_albums',
    db.Column('userId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
    db.Column('albumId', db.String, db.ForeignKey('albums.albumId', ondelete="CASCADE"), primary_key=True)
)

class Artist(db.Model):
    __tablename__ = 'artists'
    name = db.Column(db.String, nullable=False)
    coverUrl = db.Column(db.String, nullable=True)
    spotifyUrl = db.Column(db.String, nullable=False)

class ProfileArtist(db.Model):
    __tablename__ = 'profile_artists'
    id = db.Column(db.Integer, primary_key=True)  # Unikt ID
    profileId = db.Column(db.Integer, db.ForeignKey('profiles.profileId', ondelete="CASCADE"), nullable=False)  # Användarens profil
    artistId = db.Column(db.String, db.ForeignKey('songs.songId', ondelete="CASCADE"), nullable=False)






#framtida implementationer
def remove_favorite_song(user_id, song_id):
    # Ta bort låten från profile_songs-tabellen
    db.session.query(ProfileSong).filter_by(profileId=user_id, songId=song_id).delete()
    db.session.commit()

    # Kontrollera om låten fortfarande finns i profile_songs
    song_still_used = db.session.query(ProfileSong).filter_by(songId=song_id).first()

    if not song_still_used:
        # Om ingen längre har låten som favorit, ta bort den från songs-tabellen
        db.session.query(Song).filter_by(songId=song_id).delete()
        db.session.commit()


    # following = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.followerId == userId),
    #     secondaryjoin=(followers.c.followingId == userId),
    #     backref=db.backref('followers', lazy='dynamic'),
    #     lazy='dynamic'
    # )

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.following.append(user)

    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.following.remove(user)

    # def is_following(self, user):
    #     return self.following.filter(followers.c.followingId == user.userId).count() > 0

# followers = db.Table(
#     'followers',
#     db.Column('followerId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
#     db.Column('followingId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True)
# )