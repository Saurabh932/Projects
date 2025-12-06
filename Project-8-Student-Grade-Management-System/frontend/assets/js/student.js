// C:\Saurabh\Dev\Projects\Project-8-Student-Grade-Management-System\frontend\assets\js\student.js
// ===============================
// Authentication
// ===============================
const token = localStorage.getItem("access_token");
const role = localStorage.getItem("user_role");

if (!token) window.location.href = "/index.html";

const params = new URLSearchParams(window.location.search);
const studentUID = params.get("uid");

if (!studentUID) {
    alert("Invalid student reference!");
    window.location.href = "/pages/dashboard.html";
}


// ===============================
// Fetch Student Grades
// ===============================
async function fetchStudentDetails() {
    try {
        // This endpoint is correct for fetching full details for one student
        const response = await fetch(
            `http://127.0.0.1:8000/grade/student/${studentUID}`,
            { headers: { Authorization: `Bearer ${token}` } }
        );

        const data = await response.json();

        if (!response.ok) {
            return alert(data.detail || "Failed to load student details");
        }

        document.getElementById("studentName").innerText = data.name;
        document.getElementById("avg").innerText = data.average ?? "-";
        document.getElementById("grade").innerText = data.grade ?? "-";

        renderSubjects(data.subjects);
    } catch (err) {
        console.error("Error:", err);
    }
}


// ===============================
// Render Subject List
// ===============================
function renderSubjects(subjects) {
    const tbody = document.getElementById("subjectBody");
    tbody.innerHTML = "";

    subjects.forEach(s => {
        // 👑 CRITICAL: Action buttons only render if the user is an admin
        const adminActions = role === "admin"
            ? `
                <button class="btn-edit" onclick="openEditModal('${s.uid}', ${s.marks_obtain}, ${s.max_marks}, '${s.teacher_name ?? ""}')">Edit</button>
                <button class="btn-del" onclick="deleteSubject('${s.uid}')">Delete</button>
              `
            : `<span class="badge">View Only</span>`;

        tbody.innerHTML += `
        <tr>
            <td>${s.subject_name}</td>
            <td>${s.marks_obtain}</td>
            <td>${s.max_marks}</td>
            <td>${s.teacher_name ?? "-"}</td>
            <td>${adminActions}</td>
        </tr>`;
    });
}


// ===============================
// Edit Subject Modal (Unchanged)
// ===============================
let currentSubjectUID = null;

function openEditModal(uid, marks, maxMarks, teacherName) {
    if (role !== "admin") return alert("Only admin can edit!");

    currentSubjectUID = uid;

    document.getElementById("editMarks").value = marks;
    document.getElementById("editMaxMarks").value = maxMarks;
    document.getElementById("editTeacherName").value = teacherName || "";

    document.getElementById("editSubjectModal").style.display = "block";
}

function closeEditModal() {
    currentSubjectUID = null;
    document.getElementById("editSubjectModal").style.display = "none";
}


// ===============================
// Update Subject (Unchanged)
// ===============================
async function updateSubject() {
    if (!currentSubjectUID) return;

    const updateData = {
        marks_obtain: Number(document.getElementById("editMarks").value),
        max_marks: Number(document.getElementById("editMaxMarks").value),
        teacher_name: document.getElementById("editTeacherName").value
    };

    const res = await fetch(
        `http://127.0.0.1:8000/grade/subject/${currentSubjectUID}`,
        {
            method: "PATCH",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(updateData)
        }
    );

    if (!res.ok) return alert("Failed updating subject!");

    alert("Updated successfully!");
    closeEditModal();
    fetchStudentDetails();
}


// ===============================
// Delete Subject (Unchanged)
// ===============================
async function deleteSubject(uid) {
    if (role !== "admin") return alert("Not allowed");
    if (!confirm("Delete subject marks?")) return;

    const res = await fetch(
        `http://127.0.0.1:8000/grade/subject/${uid}`,
        { method: "DELETE", headers: { Authorization: `Bearer ${token}` } }
    );

    if (!res.ok) return alert("Deletion failed");

    alert("Subject deleted!");
    fetchStudentDetails();
}


// ===============================
// Back Button
// ===============================
function goBack() {
    window.location.href = "/pages/dashboard.html";
}


// Load Data
fetchStudentDetails();