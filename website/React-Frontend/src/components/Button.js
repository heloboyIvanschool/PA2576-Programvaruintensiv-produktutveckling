import React from 'react';
import './Button.css'; // Assuming you have a CSS file for styling

// Knappen ska fungera on click
function Button({ label, onClick }) {
  return (
    <button className='btn' onClick={onClick}>
      {label}
    </button>
  );
}

export default Button;