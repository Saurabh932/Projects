// Centralized API client for the frontend
// All HTTP calls MUST go through this file


const BASE_URL = "http://localhost:8000";

export async function apiRequest(path, options = {}) {
    const token = localStorage.getItem("access_token");

    const headers = { "Content-Type": "application/json",
                    ...(token ? { Authorization: `Bearer ${token}` } : {}),
                    ...options.headers };

    const response = await fetch( `${BASE_URL}${path}`, { ...options, headers } );

    const data = await response.json();

    if (!response.ok){
        throw new Error(data.detail || "API Error");
    }

    return data;
}