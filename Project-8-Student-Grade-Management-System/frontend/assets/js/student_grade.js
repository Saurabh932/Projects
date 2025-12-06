console.log("📌 Student Grade Page Loaded");

// 1) Read auth info
const token = localStorage.getItem("access_token");
const email = localStorage.getItem("user_email");

if (!token || !email) {
    console.warn("Missing token or email — redirecting to login");
    window.location.href = "/index.html";
}

// 2) Check if admin clicked "View" with ?uid=...
const params = new URLSearchParams(window.location.search);
const studentUidFromUrl = params.get("uid");

// Decide endpoint:
// - Student logged in directly => /grade/me
// - Admin viewing a particular student => /grade/{student_uid}
const apiUrl = studentUidFromUrl
    ? `http://127.0.0.1:8000/grade/student/${studentUidFromUrl}`
    : `http://127.0.0.1:8000/grade/me`;

console.log("➡ Using API URL:", apiUrl);

async function fetchMyGrades() {
    try {
        const response = await fetch(apiUrl, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        const data = await response.json();
        console.log("🎯 Grade API Response:", data);

        if (!response.ok) {
            alert(data.detail || "Failed to fetch Student Grades");
            return;
        }

        // The backend returns name, average, grade, subjects[]
        document.getElementById("studentName").innerText = data.name ?? "Student";
        document.getElementById("avg").innerText = data.average ?? "-";

        const gradeEl = document.getElementById("grade");
        gradeEl.innerText = data.grade ?? "-";

        // Optional: apply pastel grade color classes if your CSS has .badge-A / .badge-B / etc.
        gradeEl.className = "value grade-pill"; // reset base class
        if (data.grade === "A") gradeEl.classList.add("badge-A");
        else if (data.grade === "B") gradeEl.classList.add("badge-B");
        else if (data.grade === "C") gradeEl.classList.add("badge-C");
        else if (data.grade === "F") gradeEl.classList.add("badge-F");

        renderSubjects(data.subjects || []);
    } catch (error) {
        console.error("❌ Error fetching grade:", error);
    }
}

fetchMyGrades();

function renderSubjects(subjects) {
    const tbody = document.getElementById("subjectBody");
    tbody.innerHTML = "";

    subjects.forEach((s) => {
        tbody.innerHTML += `
        <tr>
            <td>${s.subject_name}</td>
            <td>${s.marks_obtain}</td>
            <td>${s.max_marks}</td>
            <td>${s.teacher_name ?? "-"}</td>
        </tr>`;
    });
}

// Logout
function logout() {
    localStorage.clear();
    window.location.href = "/index.html";
}
