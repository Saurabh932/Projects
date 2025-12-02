const API_BASE_URL = 'http://127.0.0.1:8000';

async function apiCall(url, method, data, token = null){
    const headers = {"Content-Type":"application/json"};

    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${API_BASE_URL}${url}`, {method, headers, body: data ? JSON.stringify(data):null});
    
    return response.json()
}; 