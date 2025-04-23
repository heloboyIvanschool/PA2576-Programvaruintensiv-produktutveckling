import React, { useState } from 'react';
import './Discovery.css';

// Denna sidan är under utveckling..
const Discovery = () => {
  // Låter söktermen vara tom som initialt värde
  const [searchQuery, setSearchQuery] = useState('');
// Vi skapar möjligheten att söka efter användare genom textinmatning
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    // Implement search functionality here
    console.log('Search query:', searchQuery);
  };
  // Här under ska vi ha mer funktionalitet

  // Renderar komponenten 
  return (
    <div className="discovery-container">
      <h1>Discover Users</h1>
      <form onSubmit={handleSearchSubmit} className="search-form">
        <input
          type="text"
          placeholder="Search for users..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
      </form>
    </div>
  );
};

export default Discovery;