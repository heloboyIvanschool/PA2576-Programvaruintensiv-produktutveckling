import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  const [profilePicture, setProfilePicture] = useState('');

  useEffect(() => {
    fetch('/get-profile-picture', { credentials: 'include' }) // Inkludera cookies för autentisering
      .then(response => response.json())
      .then(data => {
        setProfilePicture(data.profile_picture);
      })
      .catch(error => console.error('Error fetching profile picture:', error));
  }, []);

  return (
    <nav className='navbar'>
      <div className='navbar-container'>
        <Link to="/" className="navbar-logo">
          Resonate
        </Link>
        <div className='navbar-menu'>
          <Link to="/" className="navbar-item">Home</Link>
          <Link to="/discovery" className="navbar-item">Discovery</Link>
          <Link to="/profile" className="navbar-item">Profile</Link>
        </div>
        <div className='navbar-profile'>
          <span className='navbar-username'>Noclip</span>
          <img
            src={profilePicture || 'default_profile_pic.jpg'}
            alt='Profile'
            className='navbar-profile-pic'
          />
        </div>  
      </div>
    </nav>
  );
}

export default Navbar;