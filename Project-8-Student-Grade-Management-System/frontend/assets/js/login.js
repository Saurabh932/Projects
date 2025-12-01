const loginForm = document.getElementById("loginForm")
const errorMsg = document.getElementById("error-message")


loginForm.addEventListener("submit", async(e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const result = await apiCall("/auth/login", "POST", {email, password});

    if (result.access_token){
        localStorage.setItem("token", result.access_token);
        localStorage.setItem("user_role", result.user.role);
        localStorage.setItem("user_uid", result.user.uid);

        if (result.user.role === "admin"){
            window.location.href = "admin.html";
        }else {
            window.location.href = "dashboard.html";
        }
    }else{
        errorMsg.style.display = "block";
        errorMsg.innerText = result.detail || "Login Failed";
    }
});