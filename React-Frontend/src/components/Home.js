import { useState, useEffect } from "react";
import './Home.css'; // Importera en CSS-fil för styling

const Home = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/", { credentials: "include" })
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div className="home-container">
      <h1>Welcome to Resonate!</h1>
      {data ? (
        <p>Hello, {data.user}!</p>
      ) : (
        <p>Loading user data...</p>
      )}
      <p>Explore the features and enjoy your stay!</p>
    </div>
  );
};

export default Home;