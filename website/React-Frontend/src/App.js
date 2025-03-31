import React from 'react';
import Navbar from './components/Navbar';
import Profile from './components/Profile';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Discovery from './components/Discovery';
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
          <Route path="/login" element={<Login />} />
          <Route path="/auth" element={<Register />} />
          <Route path="/discovery" element={<Discovery />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;