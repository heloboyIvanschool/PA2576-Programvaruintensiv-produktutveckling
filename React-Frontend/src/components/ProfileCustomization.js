import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './ProfileCustomization.css'; // Assuming you have a CSS file for styling

function ProfileCustomization() {
  const [username, setUsername] = useState('Noclip');
  const [profilePic, setProfilePic] = useState('https://i.scdn.co/image/ab67616d0000b273c447c48ddac6e8a417d0f77a');
  const [favoriteAlbum, setFavoriteAlbum] = useState('https://open.spotify.com/album/0u7sgzvlLmPLvujXxy9EeY');
  const [favoriteSong, setFavoriteSong] = useState('https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH');
  const [favoriteArtist, setFavoriteArtist] = useState('https://open.spotify.com/artist/4KXp3xtaz1wWXnu5u34eVX');

  return (
    <div className="profile-customization-page">
      <h1>Profile Customization</h1>
      <form>
        <div className="form-group">
          <label>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Profile Picture URL:</label>
          <input type="text" value={profilePic} onChange={(e) => setProfilePic(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Favorite Album URL:</label>
          <input type="text" value={favoriteAlbum} onChange={(e) => setFavoriteAlbum(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Favorite Song URL:</label>
          <input type="text" value={favoriteSong} onChange={(e) => setFavoriteSong(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Favorite Artist URL:</label>
          <input type="text" value={favoriteArtist} onChange={(e) => setFavoriteArtist(e.target.value)} />
        </div>
      </form>
      <Link to="/profile">Back to Profile</Link>
    </div>
  );
}

export default ProfileCustomization;