const API_URL = "http://127.0.0.1:5000/api"; // Flask backend

export const fetchProfile = async () => {
    try {
        const response = await fetch(`${API_URL}/profile-content`, {
            credentials: "include", // Behövs om du använder Flask-Login
        });
        if (!response.ok) throw new Error("Något gick fel");
        return await response.json();
    } catch (error) {
        console.error("Error fetching profile:", error);
        return null;
    }
};