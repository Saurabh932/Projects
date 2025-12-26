// ===============================
// Authentication & Role Check
// ===============================
const token = localStorage.getItem("access_token");
const userRole = (localStorage.getItem("user_role") || "student").toLowerCase();

console.log("Current User Role:", userRole);
console.log("Token Present:", !!token);

if (!token) {
    console.warn("No token found, redirecting to login.");
    window.location.href = "/index.html";
}


if (userRole !== "admin") {
    console.warn("Non-admin attempted to access dashboard");
    window.location.href = "/pages/student_grade.html";
}


function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

const emailSpan = document.getElementById("user-email");
if (emailSpan) {
    emailSpan.innerText = localStorage.getItem("user_email") || "";
}

// ===============================
// Admin UI Rule
// ===============================
function applyRoleVisibility() {
    const addBtn = document.getElementById("addStudentBtn");
    const approvalSec = document.getElementById("approvalSection");

    if (userRole !== "admin") {
        if (addBtn) addBtn.style.display = "none";
        if (approvalSec) approvalSec.style.display = "none";
    } else {
        if (approvalSec) {
            approvalSec.style.display = "block";
            fetchApprovals();
        }
    }
}

// ===============================
// Pending Approvals (Admin)
// ===============================
async function fetchApprovals() {
    try {
        const response = await fetch("/auth/pending", { headers: getAuthHeaders() });
        const users = await response.json();
        const tbody = document.getElementById("approvalBody");
        if (!tbody) return;

        tbody.innerHTML = "";
        users.forEach(u => {
            tbody.innerHTML += `
                <tr>
                    <td>${u.email}</td>
                    <td>
                        <button class="action-btn btn-approve" onclick="approveUser('${u.uid}')">Approve</button>
                        <button class="btn-reject action-btn delete-btn" onclick="rejectUser('${u.uid}')">Reject</button>
                    </td>
                </tr>`;
        });
    } catch (err) {
        console.error("Approval Fetch Error:", err);
    }
}

function toggleApprovalCard() {
    const card = document.getElementById("approvalCard");
    if (!card) return;

    // We toggle the 'active' class to trigger the CSS transition
    card.classList.toggle("active");

    // Optional: Log to verify it's working
    console.log("Card classes:", card.className);
}

async function approveUser(uid) {
    await fetch(`/auth/approve/${uid}`, { method: "POST", headers: getAuthHeaders() });
    alert("User Approved!");
    fetchApprovals();
}

async function rejectUser(uid) {
    await fetch(`/auth/reject/${uid}`, { method: "DELETE", headers: getAuthHeaders() });
    alert("User Rejected!");
    fetchApprovals();
}

// ===============================
// Student Fetch + Pagination
// ===============================
let search = "";
let sort = "name";
let order = "asc";
let limit = 10;
let offset = 0;

function applyFilters() {
    search = document.getElementById("searchBox").value.trim();
    sort = document.getElementById("sortSelect").value;
    order = document.getElementById("orderSelect").value;
    offset = 0;
    fetchStudents();
}

async function fetchStudents() {
    try {
        const url = `/students/?search=${search}&sort=${sort}&order=${order}&limit=${limit}&offset=${offset}`;
        console.log("Fetching students from:", url);
        
        const res = await fetch(url, { headers: getAuthHeaders() });
        const data = await res.json();
        
        console.log("Student Data Received:", data);
        
        // Handle case where backend might return { students: [...] } instead of [...]
        const studentsArray = Array.isArray(data) ? data : (data.students || []);
        renderStudents(studentsArray);
    } catch (err) {
        console.error("Student Fetch Error:", err);
        alert("Failed to load students! Check console for errors.");
    }
}

function nextPage() { offset += limit; fetchStudents(); }
function prevPage() { offset = Math.max(0, offset - limit); fetchStudents(); }

// ===============================
// Render Students Table
// ===============================
function renderStudents(students) {
    const tbody = document.getElementById("studentsTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    students.forEach(st => {
        const isAdmin = userRole === "admin";
        tbody.innerHTML += `
            <tr>
                <td>${st.name}</td>
                <td>${st.average ?? "-"}</td>
                <td>${st.grade ?? "-"}</td>
                <td class="actions">
                    <button class="action-btn view-btn" onclick="viewStudent('${st.uid}')">🔍 View</button>
                    ${isAdmin ? `
                        <button class="action-btn edit-btn" onclick="openSubjectModal('${st.uid}', '${st.name}')">✏ Add Subject</button>
                        <button class="action-btn delete-btn" onclick="deleteStudent('${st.uid}')">🗑 Delete</button>
                    ` : ''}
                </td>
            </tr>`;
    });
}

// ===============================
// Modals
// ===============================
function openAddStudentModal() { document.getElementById("addStudentModal").style.display = "flex"; }
function closeAddStudentModal() { document.getElementById("addStudentModal").style.display = "none"; }

async function addStudent() {
    const name = document.getElementById("studentName").value.trim();
    if (!name) return alert("Enter student name!");

    const res = await fetch("/students/add", {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ name })
    });

    if (!res.ok) {
        const err = await res.json();
        return alert(err.detail);
    }

    closeAddStudentModal();
    fetchStudents();
}

let currentStudentUID = null;
function openSubjectModal(uid, name) {
    currentStudentUID = uid;
    document.getElementById("subjectStudentName").innerText = name;
    document.getElementById("addSubjectModal").style.display = "flex";
}

function closeSubjectModal() { document.getElementById("addSubjectModal").style.display = "none"; }

async function addSubjectMarks() {
    const subject_name = document.getElementById("subjectName").value;
    const marks_obtain = Number(document.getElementById("subjectMarks").value);
    const max_marks = Number(document.getElementById("subjectMaxMarks").value);
    const teacher_name = document.getElementById("teacherName").value;

    await fetch(`/grade/${currentStudentUID}/subject`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ subject_name, marks_obtain, max_marks, teacher_name })
    });

    closeSubjectModal();
    fetchStudents();
}

async function deleteStudent(uid) {
    if (!confirm("Delete student?")) return;
    await fetch(`/students/delete/${uid}`, { method: "DELETE", headers: getAuthHeaders() });
    fetchStudents();
}

function viewStudent(uid) {
    if (userRole !== "admin") {
        alert("Unauthorized");
        return;
    }
    window.location.href = `/pages/student.html?uid=${uid}`;
}

function logout() { localStorage.clear(); window.location.href = "/index.html"; }

// ===============================
// INITIALIZE
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    applyRoleVisibility();
    fetchStudents();
});