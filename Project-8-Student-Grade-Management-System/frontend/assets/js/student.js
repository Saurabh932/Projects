// ===============================
// Authentication
// ===============================
const token = localStorage.getItem("access_token");
const role = localStorage.getItem("user_role");

if (!token) window.location.href = "/index.html";

if (role !== "admin") {
    alert("Unauthorized access");
    window.location.href = "/pages/student_grade.html";
}

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
        const response = await fetch(
            `/grade/student/${studentUID}`,
            { headers: { Authorization: `Bearer ${token}` } }
        );

        const data = await response.json();

        if (!response.ok) {
            return alert(data.detail || "Failed to load student details");
        }

        document.getElementById("studentName").innerText = data.name;
        document.getElementById("avg").innerText = data.average ?? "-";

        const gradeEl = document.getElementById("grade");
        gradeEl.innerText = data.grade ?? "-";
        gradeEl.className = "value grade-pill";

        if (data.grade === "A") gradeEl.classList.add("badge-A");
        else if (data.grade === "B") gradeEl.classList.add("badge-B");
        else if (data.grade === "C") gradeEl.classList.add("badge-C");
        else if (data.grade === "F") gradeEl.classList.add("badge-F");

        renderSubjects(data.subjects || []);
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
        tbody.innerHTML += `
        <tr>
            <td>${s.subject_name}</td>
            <td>${s.marks_obtain}</td>
            <td>${s.max_marks}</td>
            <td>${s.teacher_name ?? "-"}</td>
            <td class="actions">
                <button class="btn-edit" onclick="openEditModal('${s.uid}', ${s.marks_obtain}, ${s.max_marks}, '${s.teacher_name ?? ""}')">Edit</button>
                <button class="btn-del" onclick="deleteSubject('${s.uid}')">Delete</button>
            </td>
        </tr>`;
    });
}


// ===============================
// Edit Subject Modal
// ===============================
let currentSubjectUID = null;

function openEditModal(uid, marks, maxMarks, teacherName) {
    currentSubjectUID = uid;

    document.getElementById("editMarks").value = marks;
    document.getElementById("editMaxMarks").value = maxMarks;
    document.getElementById("editTeacherName").value = teacherName || "";

    document.getElementById("editSubjectModal").style.display = "flex";
}

function closeEditModal() {
    currentSubjectUID = null;
    document.getElementById("editSubjectModal").style.display = "none";
}


// ===============================
// Update Subject
// ===============================
async function updateSubject() {
    if (!currentSubjectUID) return;

    const updateData = {
        marks_obtain: Number(document.getElementById("editMarks").value),
        max_marks: Number(document.getElementById("editMaxMarks").value),
        teacher_name: document.getElementById("editTeacherName").value
    };

    const res = await fetch(
        `/grade/subject/${currentSubjectUID}`,
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
// Delete Subject
// ===============================
async function deleteSubject(uid) {
    if (!confirm("Delete subject marks?")) return;

    const res = await fetch(
        `/grade/subject/${uid}`,
        { method: "DELETE", headers: { Authorization: `Bearer ${token}` } }
    );

    if (!res.ok) return alert("Deletion failed");

    alert("Subject deleted!");
    fetchStudentDetails();
}


// ===============================
// Navigation
// ===============================
function goBack() {
    window.location.href = "/pages/dashboard.html";
}

function logout() {
    localStorage.clear();
    window.location.href = "/index.html";
}


// Load Data
fetchStudentDetails();
