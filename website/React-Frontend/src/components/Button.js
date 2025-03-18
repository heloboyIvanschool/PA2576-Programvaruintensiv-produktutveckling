import React from 'react';
import './Button.css'; // Assuming you have a CSS file for styling

function Button({ label, onClick }) {
  return (
    <button className='btn' onClick={onClick}>
      {label}
    </button>
  );
}

export default Button;