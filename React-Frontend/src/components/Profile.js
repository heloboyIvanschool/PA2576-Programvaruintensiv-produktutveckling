import React from 'react';
import './Profile.css';

function Profile() {
  return (
    <>
      <div className="profile-container">
        <div className="profile-header">
          <img src="https://i.scdn.co/image/ab67616d0000b273c447c48ddac6e8a417d0f77a" alt="Profile" className="profile-pic-large" />
          <h1 className="profile-username">Username</h1>
        </div>
      </div>

      <div className="favorite-songs-container">
        <h2>Favorite Songs</h2>
        <ul className="favorite-songs">
          <li>Song 1</li>
          <li>Song 2</li>
          <li>Song 3</li>
          {/* Add more songs here */}
        </ul>
      </div>

      <div className='showcase'>
        
        <div className='showcase-section'>
          <h2>Albums</h2>
          <div className="showcase-items">
            <img src="https://i.scdn.co/image/ab67616d0000b2730cd942c1a864afa4e92d04f2" alt="Album 1" className="showcase-item" />
            <img src="https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c" alt="Album 2" className="showcase-item" />
            <img src="https://via.placeholder.com/100" alt="Album 3" className="showcase-item" />
          </div>  
        </div>


        <div className="showcase-section">
          <h2>Artists</h2>
          <div className="showcase-items">
            <img src="https://via.placeholder.com/100" alt="Artist 1" className="showcase-item" />
            <img src="https://via.placeholder.com/100" alt="Artist 2" className="showcase-item" />
            <img src="https://via.placeholder.com/100" alt="Artist 3" className="showcase-item" />
          </div>
        </div>

        <div className="showcase-section">
          <h2>Badges</h2>
          <div className="showcase-items">
            <img src="https://via.placeholder.com/100" alt="Badge 1" className="showcase-item" />
            <img src="https://via.placeholder.com/100" alt="Badge 2" className="showcase-item" />
            <img src="https://via.placeholder.com/100" alt="Badge 3" className="showcase-item" />
          </div>
        </div>

      </div>
    </>
  );
}

export default Profile;