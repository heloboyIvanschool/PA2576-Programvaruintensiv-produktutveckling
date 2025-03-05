import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Assuming you have a CSS file for styling

function Navbar() {
  return (
    <nav className='navbar'>
      <div className='navbar-container'>
        <Link to="/" className="navbar-logo">
          Resonate
        </Link>
        <div className='navbar-menu'>
          <Link to="/" className="navbar-item">
            Home
          </Link>
          <Link to="/discovery" className="navbar-item">
            Discovery
          </Link>
          <Link to="/profile" className="navbar-item">
            Profile
          </Link>
        </div>
        <div className='navbar-profile'>
          <span className='navbar-username'>Noclip</span>
          <img src='https://i.scdn.co/image/ab67616d0000b273c447c48ddac6e8a417d0f77a' alt='Profile' className='navbar-profile-pic' />
        </div>  
      </div>
    </nav>
  );
}

export default Navbar;