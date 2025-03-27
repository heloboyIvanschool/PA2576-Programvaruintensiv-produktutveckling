import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // Lägger till loading state
  const navigate = useNavigate();
  const location = useLocation();  // To handle the 'next' URL in the query params

  // useEffect för att kontrollera om användaren redan är inloggad
  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        setLoading(true); // Börja ladda när vi gör förfrågan
        const response = await fetch('http://127.0.0.1:5000/auth-status', {
          method: 'GET',
          credentials: 'include', // Skicka sessionen/cookies med
        });

        // Kontrollera om servern svarar korrekt
        if (!response.ok) {
          throw new Error('Failed to fetch login status');
        }

        const data = await response.json();

        if (data.logged_in) {
          navigate('/profile');  // Om användaren är inloggad, navigera till profile
        } else {
          setLoading(false); // Sluta ladda om användaren inte är inloggad
        }
      } catch (error) {
        console.error('Error checking login status:', error);
        setError('Could not check login status. Please try again later.');
        setLoading(false); // Sluta ladda om det sker ett fel
      }
    };

    checkLoginStatus(); // Kör funktionen vid sidladdning
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true); // Börja ladda när användaren försöker logga in

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
        credentials: 'include', // Include credentials (cookies)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Invalid credentials');
      }

      // After successful login, check if there's a 'next' URL to redirect to
      const nextUrl = data.next || '/profile'; // Default to '/profile' if no 'next' is provided
      navigate(nextUrl);  // Navigate to the 'next' URL or the default profile page
    } catch (error) {
      console.error("Error in fetching:", error);  // Loggar mer detaljer om felet
      setError(error.message || 'An error occurred');
    } finally {
      setLoading(false); // Sluta ladda när förfrågan är klar
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

          <button type="submit" disabled={loading}>Log in</button> {/* Disablerar knappen om vi laddar */}

        </form>

        {loading && <p>Loading...</p>} {/* Laddningsindikator när vi väntar på svar */}

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
