import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // useEffect for checking if user is already logged in
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://127.0.0.1:5000/auth-status', {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Failed to fetch login status');
        }

        const data = await response.json();

        if (data.logged_in) {
          navigate('/profile');
        } else {
          setLoading(false);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
        setError('Could not check login status. Please try again later.');
        setLoading(false);
      }
    };

    checkLoginStatus();
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    console.log("Attempting login with:", { email, password });

    try {
      console.log("Sending login request to server...");
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include',
      });
      
      console.log("Login response status:", response.status);
      
      const data = await response.json();
      console.log("Login response data:", data);

      if (!response.ok) {
        throw new Error(data.error || 'Invalid credentials');
      }

      console.log("Login successful, redirecting to:", data.next || '/profile');
      navigate(data.next || '/profile');
    } catch (error) {
      console.error("Error in login process:", error);
      setError(error.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Log in</h2>
        {error && <p className="login-error">{error}</p>}

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

          <button type="submit" disabled={loading}>Log in</button>
        </form>

        {loading && <p>Loading...</p>}

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