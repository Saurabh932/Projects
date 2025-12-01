/* 
    Checking if the login form working

*/

// const loginForm = document.getElementById("loginForm")
// const errorMsg = document.getElementById("error-message")


// loginForm.addEventListener("submit", async(e) => {
//     e.preventDefault();

//     const email = document.getElementById("email").value;
//     const password = document.getElementById("password").value;

//     const result = await apiCall("/auth/login", "POST", {email, password});

//     if (result.access_token){
//         localStorage.setItem("token", result.access_token);
//         localStorage.setItem("user_role", result.user.role);
//         localStorage.setItem("user_uid", result.user.uid);

//         if (result.user.role === "admin"){
//             window.location.href = "admin.html";
//         }else {
//             window.location.href = "dashboard.html";
//         }
//     }else{
//         errorMsg.style.display = "block";
//         errorMsg.innerText = result.detail || "Login Failed";
//     }
// });




/*  
    Updating to call /auth/login

    JWT in localStorage keeps the flow simple and clean for our learning 
    Now we’ll connect your Login UI → FastAPI Auth API.
*/


// If already logged in -> go to dashboard
const existingToken = localStorage.getItem("access_token");
if (existingToken) {
    window.location.href = "/dashboard.html";
}

// If new user
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, password: password })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail || "Login Failed!");
                return;
            }

            // Storing JWT + user data in localStorage
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("user_role", data.user.role);
            localStorage.setItem("user_email", data.user.email);

            // Navigate to dashboard after successful login
            window.location.href = "/dashboard.html";

        } catch (error) {
            console.error("Login error:", error);
            alert("Something went wrong! Try again.");
        }
    });
});
