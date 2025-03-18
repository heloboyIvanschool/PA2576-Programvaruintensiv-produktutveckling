import { useState, useEffect } from "react";
import "./Home.css"; // Se till att Home.css är korrekt länkad

const Home = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("/api/user", { credentials: "include" }) // Ändrat för att matcha Flask API
            .then(response => {
                if (!response.ok) throw new Error("Failed to fetch data");
                return response.json();
            })
            .then(data => {
                setData(data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    return (
        <div className="home-container">
            <h1>Welcome to Resonate!</h1>
            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
            {data && <p>Hello, {data.user}!</p>}
            <h2>här</h2>
        </div>
    );
};

export default Home;