// ===============================
// Authentication & Role Check
// ===============================
const token = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_role") || "student";

if (!token) {
    window.location.href = "/index.html";
}

function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
    };
}

// Load Navbar Email
const emailSpan = document.getElementById("user-email");
if (emailSpan) {
    emailSpan.innerText = localStorage.getItem("user_email") || "";
}


// ===============================
// Admin UI Rule
// ===============================
if (userRole !== "admin") {
    document.getElementById("addStudentBtn").style.display = "none";
    document.getElementById("approvalSection").style.display = "none";
} else {
    document.getElementById("approvalSection").style.display = "block";
    fetchApprovals();
}


// ===============================
// Pending Approvals (Admin)
// ===============================
async function fetchApprovals() {
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/pending", {
            headers: getAuthHeaders(),
        });
        const users = await response.json();

        const tbody = document.getElementById("approvalBody");
        tbody.innerHTML = "";

        users.forEach(u => {
            tbody.innerHTML += `
                <tr>
                    <td>${u.email}</td>
                    <td>
                        <button class="btn-approve" onclick="approveUser('${u.uid}')">Approve</button>
                        <button class="btn-reject" onclick="rejectUser('${u.uid}')">Reject</button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error(err);
    }
}

function toggleApprovalCard() {
    const card = document.getElementById("approvalCard");
    card.style.display = card.style.display === "none" ? "block" : "none";
}

async function approveUser(uid) {
    await fetch(`http://127.0.0.1:8000/auth/approve/${uid}`, {
        method: "POST",
        headers: getAuthHeaders(),
    });
    alert("User Approved!");
    fetchApprovals();
}

async function rejectUser(uid) {
    await fetch(`http://127.0.0.1:8000/auth/reject/${uid}`, {
        method: "DELETE",
        headers: getAuthHeaders(),
    });
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
        const url = `http://127.0.0.1:8000/students/?search=${search}&sort=${sort}&order=${order}&limit=${limit}&offset=${offset}`;
        const res = await fetch(url, { headers: getAuthHeaders() });
        const students = await res.json();
        renderStudents(students);
    } catch {
        alert("Failed to load students!");
    }
}

function nextPage() {
    offset += limit;
    fetchStudents();
}

function prevPage() {
    offset = Math.max(0, offset - limit);
    fetchStudents();
}


// ===============================
// Render Students Table
// ===============================
function renderStudents(students) {
    const tbody = document.getElementById("studentsTableBody");
    tbody.innerHTML = "";

    students.forEach(st => {
        const isAdmin = userRole === "admin"; // If needed later
        tbody.innerHTML += `
            <tr>
                <td>${st.name}</td>
                <td>${st.average ?? "-"}</td>
                <td>${st.grade ?? "-"}</td>
                <td class="actions">
                    <button class="action-btn view-btn" onclick="viewStudent('${st.uid}')">
                        🔍 View
                    </button>
                    <button class="action-btn edit-btn" onclick="openSubjectModal('${st.uid}', '${st.name}')">
                    ✏ Add Subject
                    </button>
                    </button>
                    <button class="action-btn delete-btn" onclick="deleteStudent('${st.uid}')">
                        🗑 Delete
                    </button>
                </td>
            </tr>`;
    });

}

fetchStudents();



// ===============================
// Add Student
// ===============================
function openAddStudentModal() {
    document.getElementById("addStudentModal").style.display = "flex";
}

function closeAddStudentModal() {
    document.getElementById("addStudentModal").style.display = "none";
}

async function addStudent() {
    const name = document.getElementById("studentName").value.trim();
    if (!name) return alert("Enter student name!");

    const res = await fetch("http://127.0.0.1:8000/students/add", {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ name })
    });

    if (!res.ok) {
        const err = await res.json();
        return alert(err.detail);
    }

    closeAddStudentModal();
    alert("Student Added!");
    fetchStudents();
}



// ===============================
// Add Subject (Marks)
// ===============================
let currentStudentUID = null;
let currentStudentName = null;

function openSubjectModal(uid, name) {
    if (userRole !== "admin") {
        alert("Only admin can add subjects!");
        return;
    }

    currentStudentUID = uid;
    currentStudentName = name;

    document.getElementById("subjectStudentName").innerText = currentStudentName;
    document.getElementById("addSubjectModal").style.display = "flex"; // CENTER FIX
}




function closeSubjectModal() {
    currentStudentUID = null;
    currentStudentName = null;
    document.getElementById("addSubjectModal").style.display = "none";
}

async function addSubjectMarks() {
    if (!currentStudentUID) return alert("No student selected!");

    const subject_name = document.getElementById("subjectName").value;
    const marks_obtain = Number(document.getElementById("subjectMarks").value);
    const max_marks = Number(document.getElementById("subjectMaxMarks").value);
    const teacher_name = document.getElementById("teacherName").value;

    const res = await fetch(`http://127.0.0.1:8000/grade/${currentStudentUID}/subject`, {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify({ subject_name, marks_obtain, max_marks, teacher_name })
    });

    if (!res.ok) return alert("Error adding marks!");

    closeSubjectModal();
    alert("Marks Added!");
    fetchStudents();
}



// ===============================
// Delete Student
// ===============================
async function deleteStudent(uid) {
    if (!confirm("Delete student?")) return;

    await fetch(`http://127.0.0.1:8000/students/delete/${uid}`, {
        method: "DELETE",
        headers: getAuthHeaders()
    });

    fetchStudents();
}



// ===============================
// View Student Profile Page
// ===============================
function viewStudent(uid) {
    window.location.href = `/pages/student_grade.html?uid=${uid}`;
}



// ===============================
// Logout
// ===============================
function logout() {
    localStorage.clear();
    window.location.href = "/index.html";
}
