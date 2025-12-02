function logout(){
    localStorage.clear();
    window.location.href="/";
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