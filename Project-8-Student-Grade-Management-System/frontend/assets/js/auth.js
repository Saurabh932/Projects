function logout(){
    localStorage.clear();
    window.location.herf="/";
}

function getToken(){
    return localStorage.getItem("access_token");
}

function getAuthHeaders(){
    return {
        "Authorization":`Bearer ${getToken()}`,
        "Content-Type":"application/json"
    };
}