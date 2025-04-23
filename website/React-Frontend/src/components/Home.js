import { useState, useEffect } from "react";
import "./Home.css";

// Detta är startsidan för Resonate

//Här hämtar vi användardatan som kommer synas på hemsidan
const Home = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // API anrop för att hämta datan
    useEffect(() => {
        fetch("/api/user", { credentials: "include" }) // Ändrat för att matcha Flask API
            .then(response => {
                if (!response.ok) throw new Error("Failed to fetch data");
                // Kollar om svaret är okej eller inte
                return response.json();
            })
            // Uppdaterar datan
            .then(data => {
                setData(data);
                setLoading(false);
            })
            // Markerar att laddningen är klar
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);
    // Renderar UI-komponenten
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