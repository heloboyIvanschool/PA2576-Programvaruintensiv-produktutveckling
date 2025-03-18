import React from 'react';
import './Profile.css';
import { Link } from 'react-router-dom';
import { fetchProfile } from "./api";

function Profile() {
  return (
    <>
      <div className="profile-page">
        <div className="left-column">
          <div className="profile-group">
            <div className="profile-container">
              <div className="profile-header">
                <img
                  src="https://i.scdn.co/image/ab6761610000e5eba7874efb5aa08fc40af59c10"
                  alt="Profile"
                  className="profile-pic-large"
                />
                <div className="profile-info">
                  <h1 className="profile-username">Sean Banan</h1>
                  <div className="favorite-genres">
                    <span className="genre">Rock</span>
                    <span className="genre">Progressive-Rock</span>
                    <span className="genre">House</span>
                    <span className="genre">EDM</span>
                  </div>
                </div>
              </div>
              <Link to="/profile-customization">Edit Profile</Link>
            </div>

            <div className="favorite-songs-showcase">
              <div className="favorite-songs-container">
                <h2>Top Songs</h2>
                <ul className="favorite-songs">
                  <iframe
                    src="https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                  <iframe
                    src="https://open.spotify.com/embed/track/70LcF31zb1H0PyJoS1Sx1r"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                  <iframe
                    src="https://open.spotify.com/embed/track/6SXy02aTZU3ysoGUixYCz0"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                  <iframe
                    src="https://open.spotify.com/embed/track/0fMqi9V3pulDGq1S62Y0WL"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                  <iframe
                    src="https://open.spotify.com/embed/track/5UuikgHTxSRFRnC0zXx10i"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                  <iframe
                    src="https://open.spotify.com/embed/track/03sEzk1VyrUZSgyhoQR0LZ"
                    width="270"
                    height="80"
                    frameBorder="0"
                    allowTransparency="true"
                    allow="encrypted-media"
                  ></iframe>
                </ul>
              </div>

              <div className="showcase">
                <div className="showcase-section">
                  <div className="showcase-section-content">
                    <h2>Albums</h2>
                    <div className="showcase-items">
                      <a href="https://open.spotify.com/album/0u7sgzvlLmPLvujXxy9EeY" target="_blank">
                        <img
                          src="https://i.scdn.co/image/ab67616d0000b273042dbf8721e37f11843bfeac"
                          alt="Album 1"
                          className="showcase-item"
                        />
                      </a>
                      <a href="https://open.spotify.com/album/0NGM3Ftwjw0dLNpAowmz3x" target="_blank">
                        <img
                          src="https://i.scdn.co/image/ab67616d0000b273be6e758fe8300a72eceddb8f"
                          alt="Album 2"
                          className="showcase-item"
                        />
                      </a>
                      <a href="https://open.spotify.com/album/1zcm3UvHNHpseYOUfd0pna" target="_blank">
                        <img
                          src="https://i.scdn.co/image/ab67616d0000b2735405ef9e393f5f1e53b4b42e"
                          alt="Album 3"
                          className="showcase-item"
                        />
                      </a>
                    </div>
                  </div>
                </div>

                <div className="showcase-section">
                  <div className="showcase-section-content">
                    <h2>Artists</h2>
                    <div className="showcase-items">
                      <a href="https://open.spotify.com/artist/4KXp3xtaz1wWXnu5u34eVX" target="_blank">
                        <img
                          src="https://i.scdn.co/image/38129832f70d5798de2618faa55182407135842c"
                          alt="Artist 1"
                          className="showcase-item"
                        />
                      </a>
                      <a href="https://open.spotify.com/artist/4bthk9UfsYUYdcFyqxmSUU" target="_blank">
                        <img
                          src="https://i.scdn.co/image/ab6761610000e5eb1e63dea1bded4ae1d53b5c9a"
                          alt="Artist 2"
                          className="showcase-item"
                        />
                      </a>
                      <a href="https://open.spotify.com/artist/0PFtn5NtBbbUNbU9EAmIWF" target="_blank">
                        <img
                          src="https://i.scdn.co/image/ab6761610000e5eba59a5bcab211f964fe9bfb06"
                          alt="Artist 3"
                          className="showcase-item"
                        />
                      </a>
                    </div>
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
