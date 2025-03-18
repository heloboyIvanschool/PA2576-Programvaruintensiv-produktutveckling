import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // useEffect för att kontrollera om användaren redan är inloggad
  useEffect(() => {
    const checkLoginStatus = async () => {
      const response = await fetch('http://127.0.0.1:5000/auth-status', {
        method: 'GET',
        credentials: 'include', // Skicka sessionen/cookies med
      });

      const data = await response.json();

      if (data.logged_in) {
        navigate('/profile');  // Om användaren är inloggad, navigera till profile
      }
    };

    checkLoginStatus(); // Kör funktionen vid sidladdning
  }, [navigate]); // Dependency array, kör bara när navigate förändras (vid inladdning)

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Invalid credentials');
      }

      navigate('/profile');
    } catch (error) {
      console.error("Error in fetching:", error);  // Loggar mer detaljer om felet
      setError(error.message || 'An error occurred');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Log in</h2>
        {error && <p className="login-error">{error}</p>} {/* Visa felmeddelande om det finns */}
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Log in</button>
        </form>

        <div className="google-login">
          <p>Or log in with Google:</p>
          <a href="#">Login with Google (Coming Soon)</a>
        </div>
        <Link to="/signup" className="login-footer">Sign up</Link>
      </div>
    </div>
  );
}

export default Login;
