import React from 'react';
import './Profile.css';

function Profile() {
  return (
    <>
    <div className="profile-page">

      <div className="left-column">
      
        <div className="profile-group">
          <div className="profile-container">
            <div className="profile-header">
              <img src="https://i.scdn.co/image/ab67616d0000b273c447c48ddac6e8a417d0f77a" alt="Profile" className="profile-pic-large" />
              <h1 className="profile-username">Noclip</h1>
            </div>
          </div>
          
          
          <div className="favorite-songs-showcase">
            <div className="favorite-songs-container">
              <h2>Favorite Songs</h2>
              <ul className="favorite-songs">
                <li>Song 1</li>
                <li>Song 2</li>
                <li>Song 3</li>
              </ul>
            </div>
        
        
            <div className='showcase'>
              <div className='showcase-section'>
                <h2>Albums</h2>
                <div className="showcase-items">
                  <img src="https://i.scdn.co/image/ab67616d0000b2730cd942c1a864afa4e92d04f2" alt="Album 1" className="showcase-item" />
                  <img src="https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c" alt="Album 2" className="showcase-item" />
                  <img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Album 3" className="showcase-item" />
                </div> 
              </div>
        
              <div className="showcase-section">
                <h2>Artists</h2>
                <div className="showcase-items">
                  <img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Artist 1" className="showcase-item" />
                  <img src="https://i.scdn.co/image/ab67616d0000b2730cd942c1a864afa4e92d04f2" alt="Artist 2" className="showcase-item" />
                  <img src="https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c" alt="Artist 3" className="showcase-item" />
                </div>
              </div>
        
              <div className="showcase-section">
                <h2>Badges</h2>
                <div className="showcase-items">
                  <img src="https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c" alt="Badge 1" className="showcase-item" />
                  <img src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac" alt="Badge 2" className="showcase-item" />
                  <img src="https://i.scdn.co/image/ab67616d0000b2730cd942c1a864afa4e92d04f2" alt="Badge 3" className="showcase-item" />
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>
      
      
      <div className="feed">
        <h2>Posts</h2>
        <div className="post">Post 1</div>
        <div className="post">Post 2</div>
        <div className="post">Post 3</div>
      
      </div>
    </div>

      
    </>
  );
}

export default Profile;