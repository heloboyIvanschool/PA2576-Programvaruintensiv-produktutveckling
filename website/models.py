from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

followers = db.Table(
    'followers',
    db.Column('followerId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
    db.Column('followingId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True)
)

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

    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.followerId == userId),
        secondaryjoin=(followers.c.followingId == userId),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(followers.c.followingId == user.userId).count() > 0

    favorite_songs = db.relationship('Song', secondary=user_songs, back_populates='liked_by_users', cascade="all, delete")
    favorite_albums = db.relationship('Album', secondary=user_albums, back_populates='liked_by_users', cascade="all, delete")

    def __repr__(self):
        return f'<User {self.username}>'

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

    #relations
    posts = db.relationship('Post', back_populates='song', cascade="all, delete-orphan")

user_songs = db.Table(
    'user_songs',
    db.Column('userId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
    db.Column('songId', db.String, db.ForeignKey('songs.songId', ondelete="CASCADE"), primary_key=True)
)

user_albums = db.Table(
    'user_albums',
    db.Column('userId', db.Integer, db.ForeignKey('users.userId', ondelete="CASCADE"), primary_key=True),
    db.Column('albumId', db.String, db.ForeignKey('albums.albumId', ondelete="CASCADE"), primary_key=True)
)