// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';
// import './Navbar.css';

// function Navbar() {
//   const [profilePicture, setProfilePicture] = useState('');

//   useEffect(() => {
//     fetch('/api/profile-picture', { credentials: 'include' })  // funkar inte just nu (/profile-picture)
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.profile_picture) {
//           setProfilePicture(data.profile_picture);
//         } else {
//           setProfilePicture('https://i1.sndcdn.com/avatars-000339644685-3ctegw-t500x500.jpg'); // Standardbild om ingen finns
//         }
//       })
//       .catch((error) => console.error('Error fetching profile picture:', error));
//   }, []);

//   return (
//     <nav className='navbar'>
//       <div className='navbar-container'>
//         <Link to="/" className="navbar-logo">Resonate</Link>
//         <div className='navbar-menu'>
//           <Link to="/" className="navbar-item">Home</Link>
//           <Link to="/discovery" className="navbar-item">Discovery</Link>
//           <Link to="/profile" className="navbar-item">Profile</Link>
//         </div>
//         <div className='navbar-profile'>
//           <span className='navbar-username'>Noclip</span>
//           <img
//             src={profilePicture || 'https://i1.sndcdn.com/avatars-000339644685-3ctegw-t500x500.jpg'}
//             alt='Profile'
//             className='navbar-profile-pic'
//           />
//         </div>
//       </div>
//     </nav>
//   );
// }

// export default Navbar;



import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const [profilePicture, setProfilePicture] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    fetch('/profile-picture', { credentials: 'include' })
      .then((res) => res.json())
      .then((data) => {
        if (data.logged_in) {
          setProfilePicture(data.profile_picture || "default_profile_pic.jpg");
          setIsLoggedIn(true);
        } else {
          setIsLoggedIn(false);
        }
      })
      .catch((error) => {
        console.error('Error fetching profile picture:', error);
        setIsLoggedIn(false);
      });
  }, []);

  return (
    <nav className='navbar'>
      <div className='navbar-container'>
        <Link to="/" className="navbar-logo">Resonate</Link>
        <div className='navbar-menu'>
          <Link to="/" className="navbar-item">Home</Link>
          <Link to="/discovery" className="navbar-item">Discovery</Link>
          {isLoggedIn ? (
            <Link to="/profile" className="navbar-item">Profile</Link>
          ) : (
            <Link to="/login" className="navbar-item">Log in</Link>
          )}
        </div>
        {isLoggedIn && (
          <Link to="/profile" className="navbar-profile">
            <img
              src={profilePicture}
              alt='Profile'
              className='navbar-profile-pic'
            />
          </Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

