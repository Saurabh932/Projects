import { useState } from "react";
import { apiRequest } from "../api/client";

export default function Login({ onLogin }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");

        try {
            const data = await apiRequest("/auth/login", { method: "POST", 
                                                          body: JSON.stringify({ email, password })
                                                        })

        localStorage.setItem("access_token", data.access_token);
        onLogin();
        }
        catch (err) {
            setError(err.message);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h2>Admin Login</h2>

            { error && <p style={{ color: "red" }}>{error}</p> }

            <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />

            <br />

            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />

            <br />

            <button type="submit">Login</button>
        </form>
    )
}