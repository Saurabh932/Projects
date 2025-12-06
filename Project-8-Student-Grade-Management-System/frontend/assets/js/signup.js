document.addEventListener("DOMContentLoaded", () =>{
    const form = document.getElementById("signupForm");
    const errorBox = document.getElementById("signup-error");

    if (!form) return;

    form.addEventListener("submit", async (e) =>{
        e.preventDefault();

        const first_name = document.getElementById("signupFirstName").value.trim();
        const last_name = document.getElementById("signupLastName").value.trim();
        const email = document.getElementById("signupEmail").value.trim();
        const password = document.getElementById("signupPassword").value;

        if (!first_name || !last_name || !email || !password){
            errorBox.style.display = "block";
            errorBox.innerText = "Email and Password are required!";
            return;
        }
        try{
            const response = await fetch("/auth/signup", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({first_name, last_name, email, password})
            });

            const data = await response.json();

            if (!response.ok){
                errorBox.style.display = "block";
                errorBox.innerText = data.detail || "Signup failed!";
                return;
            }

            alert("Account created successfully! You can now login.");
            window.location.href="/index.html";
        }
        catch(err){
            console.error("Signup error:", err);
            errorBox.style.display = "block";
            errorBox.innerText = "Something went wrong. Try again."
        }
    });
});