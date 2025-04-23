import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Register.css";

// En komponent för att registrera nya användare

function Register() {
  // Detta är saker som användaren ska lägga in 
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  

  //Hanterar processen efter inmatning
  const handleRegister = async (e) => {
    e.preventDefault();
    //Återställer gamla felmeddelanden
    setError("");

    //Skickar inmatningsdatan via API till servern
    const response = await fetch("http://127.0.0.1:5000/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, password_confirm: passwordConfirm }),
      credentials: "include",
    });

    // Tolkar API-svaret som en json fil
    const data = await response.json();

    // Om inloggningen lyckas så skickas den till profilsidan
    if (response.ok) {
      navigate("/profile"); // Skicka användaren till profil-sidan efter lyckad registrering
    } else {
      setError(data.error || "Registration failed");
    }
  };

  // Renderar registreringsformuläret
  return (
    // Alla inputs som behövs, vad som är placeholder namn osv..
    <div className="register-container">
      <div className="register-box">
        <h2>Sign Up</h2>
        {error && <p className="register-error">{error}</p>}
        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
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
          <input
            type="password"
            placeholder="Confirm Password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            required
          />
          <button type="submit">Sign Up</button>
        </form>
        <p className="register-footer">
          Already have an account? <a href="/login">Log in</a>
        </p>
      </div>
    </div>
  );
}

export default Register;
