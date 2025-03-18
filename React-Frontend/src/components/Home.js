import { useState, useEffect } from "react";

const Home = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/", { credentials: "include" })
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    return (
        <div>
            <h1>Welcome to Resonate!</h1>
            {data && <p>Hello, {data.user}!</p>}
        </div>
    );
};

export default Home;