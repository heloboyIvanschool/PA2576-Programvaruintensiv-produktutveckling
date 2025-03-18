import React from 'react';
import Navbar from './components/Navbar';
import Profile from './components/Profile'; // Import the Profile component
import Home from './components/Home'; // Import the Home component
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import ProfileCustomization from './components/ProfileCustomization';

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/profile-customization' element={<ProfileCustomization />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;