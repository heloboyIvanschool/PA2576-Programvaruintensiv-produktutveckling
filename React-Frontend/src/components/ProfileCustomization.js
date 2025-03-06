import React, { useState } from 'react';
import './ProfileCustomization.css'; // Assuming you have a CSS file for styling
import { Link, useNavigate } from 'react-router-dom';

function ProfileCustomization() {
  const [Album1, setAlbum1] = useState('https://open.spotify.com/album/0u7sgzvlLmPLvujXxy9EeY');
  const [Album2, setAlbum2] = useState('https://open.spotify.com/album/0NGM3Ftwjw0dLNpAowmz3x');
  const [Album3, setAlbum3] = useState('https://open.spotify.com/album/1zcm3UvHNHpseYOUfd0pna');

  const [Song1, setSong1] = useState('https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH');
  const [Song2, setSong2] = useState('https://open.spotify.com/embed/track/70LcF31zb1H0PyJoS1Sx1r');
  const [Song3, setSong3] = useState('https://open.spotify.com/embed/track/6SXy02aTZU3ysoGUixYCz0');

  const [Artist1, setArtist1] = useState('https://open.spotify.com/artist/4KXp3xtaz1wWXnu5u34eVX');
  const [Artist2, setArtist2] = useState('https://open.spotify.com/artist/4bthk9UfsYUYdcFyqxmSUU');
  const [Artist3, setArtist3] = useState('https://open.spotify.com/artist/0PFtn5NtBbbUNbU9EAmIWF');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/profile');
  };
  

  return (
    <div className="profile-customization-page">
      <h1>Profile Customization</h1>

      <div className="profile-group">
      
                <div className="profile-container">
      
                  <div className="profile-header">
                  <img src="https://i.scdn.co/image/ab6761610000e5eba7874efb5aa08fc40af59c10" alt="Profile" className="profile-pic-large" />
                    
                    <div className="profile-info">
                      <h1 className="profile-username">Sean Banan </h1>
      
                      <div className="favorite-genres">
                        <span className="genre">Rock</span>
                        <span className="genre">Progressive-Rock</span>
                        <span className="genre">House</span>
                        <span className="genre">EDM</span>
                      </div>
                    </div> 
                  </div>
                </div>
                
                
                
                <div className="favorite-songs-showcase">
                  <div className="favorite-songs-container">
                    <h2>Top Songs</h2>
                    <ul className="favorite-songs">
                    <input type="text" value={Song1} onChange={(e) => setSong1(e.target.value)} placeholder="Enter Song URL" />
                      <iframe src="https://open.spotify.com/embed/track/3rwd5wW9Ew5H6YlyZk9wtH" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                      <iframe src="https://open.spotify.com/embed/track/70LcF31zb1H0PyJoS1Sx1r" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                      <iframe src="https://open.spotify.com/embed/track/6SXy02aTZU3ysoGUixYCz0" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                      <iframe src="https://open.spotify.com/embed/track/0fMqi9V3pulDGq1S62Y0WL" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                      <iframe src="https://open.spotify.com/embed/track/5UuikgHTxSRFRnC0zXx10i" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                      <iframe src="https://open.spotify.com/embed/track/03sEzk1VyrUZSgyhoQR0LZ" width="270" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                    </ul>
                  </div>
              
              
                  <div className='showcase'>

                    <div className='showcase-section'>
                      <h2>Albums</h2>
                      <div className="showcase-items">

                        <div className="showcase-items">
                          <input type="text" value={Album1} onChange={(e) => setAlbum1(e.target.value)} placeholder="Enter Album URL"/>
                        </div>-
                         
                        <div className="showcase-items">
                          <input type="text" value={Album2} onChange={(e) => setAlbum2(e.target.value)} placeholder="Enter Album URL"/>
                        </div>
                      
                        <div className="showcase-items">
                          <input type="text" value={Album3} onChange={(e) => setAlbum3(e.target.value)} placeholder="Enter Album URL"/>
                        </div>
                      
                      </div> 
                    </div>
              

                    <div className="showcase-section">
                      <h2>Artists</h2>
                      <div className="showcase-items">

                      <input type="text" value={Artist1} onChange={(e) => setArtist1(e.target.value)} placeholder="Enter Artist URL" />

                      <input type="text" value={Artist2} onChange={(e) => setArtist2(e.target.value)} placeholder="Enter Artist URL" />

                      <input type="text" value={Artist3} onChange={(e) => setArtist3(e.target.value)} placeholder="Enter Artist URL" />

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



      <form onSubmit={handleSubmit}>
        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default ProfileCustomization;