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


// ========================================================================================

/*  
    Updating to call /auth/login

    JWT in localStorage keeps the flow simple and clean for our learning 
    Now we’ll connect your Login UI → FastAPI Auth API.
*/


// If already logged in -> go to dashboard
const existingToken = localStorage.getItem("access_token");
if (existingToken && window.location.pathname.endsWith("index.html")) {
    window.location.href = "/pages/dashboard.html";
}

// If new user
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    if (form){
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (!response.ok) {
                    const errEl = document.getElementById("error-message");
                    if(errEl){
                        errEl.style.display = "block";
                        errEl.innerText = data.detail || "Login Failed!"; 
                    }
                    else{
                        alert(data.detail || "Login failed!");
                    }
                    return;
                }

                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("user_role", data.user.role);
                localStorage.setItem("user_email", data.user.email);
                localStorage.setItem("user_id", data.user.uid);


                if (data.user.role === "admin"){
                    window.location.href = "/pages/dashboard.html";
                }
                else{
                    window.location.href = "/pages/student_grade.html";
                }

            } catch (error) {
                console.error("Login error:", error);
                alert("Something went wrong! Try again.");
            }
        });
    }
});


function logout(){
    localStorage.clear();
    window.location.href="/index.html";
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