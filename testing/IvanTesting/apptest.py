'''STFU'''

from flask import Flask
from modelstest import db, User, Follower, Post, Like, Comment, Song

app = Flask(__name__)

# Konfigurera SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resonate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  #Initiera db med appen

# Skapa databasen om den inte finns
with app.app_context():
    db.create_all()

with app.app_context():  # Skapa en application context
    # Skapa en användare
    new_user = User(
        userId="user123",
        username="TestUser",
        email="testuser@email.com",
        profilePicture="https://example.com/profile.jpg",
        favoriteGenres=["Rock", "Indie"]
    )

    db.session.add(new_user)  # Lägg till användaren i databasen
    db.session.commit()  # Spara ändringen

    print("✅ User added successfully!")

    # Skapa ett inlägg kopplat till användaren
    new_post = Post(
        postId="post456",
        userId="user123",
        songId="spotify_song_789",
        caption="Detta är min favoritlåt!",
        likes=0
    )

    db.session.add(new_post)
    db.session.commit()

    print("✅ Post added successfully!")

if __name__ == '__main__':
    app.run(debug=True)
