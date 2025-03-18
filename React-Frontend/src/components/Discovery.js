import React, { useState } from 'react';
import './Discovery.css'; // Importera en CSS-fil för styling

const Discovery = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    // Implement search functionality here
    console.log('Search query:', searchQuery);
  };

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