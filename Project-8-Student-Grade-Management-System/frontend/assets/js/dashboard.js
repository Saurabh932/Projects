// Redirect if no login token found
const token = localStorage.getItem("access_token");
const userRole = localStorage.getItem("user_role");

if (!token) {
    window.location.href = "/index.html";
}

// Helper: Add Authorization header
function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
    };
}

// Load logged-in email in navbar
document.getElementById("user-email").innerText =
    localStorage.getItem("email") || "";



// ===============================
// Fetch All Students
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
    offset = 0; // Reset pagination for new filter
    fetchStudents();
}

async function fetchStudents() {
  try {
    const url =
      `http://127.0.0.1:8000/students/?search=${search}&sort=${sort}&order=${order}&limit=${limit}&offset=${offset}`;

    const response = await fetch(url, { headers: getAuthHeaders() });

    if (!response.ok) {
      throw new Error("Failed to fetch students");
    }

    const data = await response.json();
    renderStudents(data);

  } catch (err) {
    console.error("Error:", err);
    alert("Error fetching students!");
  }
}




// ===============================
// Pagination
// ===============================
function nextPage(){
    offset += limit;
    fetchStudents();
}

function prevPage() {
    if (offset === 0) return;
    offset -= limit;
    fetchStudents();
}


// ===============================
// Render Students Table
// ===============================
function renderStudents(students) {
    const tbody = document.getElementById("studentsTableBody");
    tbody.innerHTML = "";

    students.forEach(st => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${st.name}</td>
            <td>${st.average ?? "-"}</td>
            <td>${st.grade ?? "-"}</td>
            <td>
                <button class="btn btn-primary" onclick="openSubjectModal('${st.name}')">Add Subject</button>
                <button class="btn btn-danger" onclick="viewDetails('${st.name}')">View</button>
                ${userRole === "admin" 
                    ? `<button class="btn btn-del" onclick="deleteStudent('${st.uid}')">Delete</button>` 
                    : ""}
            </td>
        `;

        tbody.appendChild(row);
    });
}

fetchStudents();


// ===============================
// Add Student Modal
// ===============================
function openAddStudentModal() {
    document.getElementById("addStudentModal").style.display = "block";
}

function closeAddStudentModal() {
    document.getElementById("addStudentModal").style.display = "none";
}

// Add new student
async function addStudent() {
    const name = document.getElementById("studentName").value;
    const total_marks = Number(document.getElementById("totalMarks").value);
    const total_sub = Number(document.getElementById("totalSubs").value);

    if (!name || !total_marks || !total_sub) {
        alert("All fields are required!");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/students/add", {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({ name, total_marks, total_sub })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Failed to add student");
            return;
        }

        alert("Student successfully added!");
        closeAddStudentModal();
        fetchStudents();

    } catch (error) {
        console.error("Error adding student:", error);
    }
}


// ===============================
// Add Subject Modal
// ===============================
let currentStudentName = null;

function openSubjectModal(studentName) {
    currentStudentName = studentName;
    document.getElementById("subjectStudentName").innerText = studentName;
    document.getElementById("addSubjectModal").style.display = "block";
}

function closeSubjectModal() {
    currentStudentName = null;
    document.getElementById("addSubjectModal").style.display = "none";
}

async function addSubjectMarks() {
    if (!currentStudentName) {
        alert("Student missing!");
        return;
    }

    const subject_name = document.getElementById("subjectName").value;
    const marks_obtain = Number(document.getElementById("subjectMarks").value);
    const max_marks = Number(document.getElementById("subjectMaxMarks").value);
    const teacher_name = document.getElementById("teacherName").value;

    if (!subject_name || !marks_obtain || !max_marks) {
        alert("Enter all required fields");
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/grade/${currentStudentName}/subject`,
            {
                method: "POST",
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    subject_name,
                    marks_obtain,
                    max_marks,
                    teacher_name
                })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Error adding subject");
            return;
        }

        alert("Subject added successfully!");
        closeSubjectModal();
        fetchStudents();

    } catch (error) {
        console.error(error);
    }
}


// ===============================
// View Student — Navigate to next page
// ===============================
function viewDetails(name) {
    window.location.href = `/pages/student.html?name=${encodeURIComponent(name)}`;
}



// ===============================
// Delete Student — Deletes the student
// ===============================
async function deleteStudent(uid){
    if (!confirm("Are you sure to delete?"))
        return;

    try{
        const response = await fetch(`http://127.0.0.1:8000/students/delete/${uid}`, {
            method: "DELETE",
            headers: getAuthHeaders()
        });

        if(!response.ok){
            alert("Failed to deleted student.");
            return;
        }
        alert("Deleted Successfully");
        fetchStudents();
    }
    catch (error){
        console.log(error);
        alert("Error deleting student!");
    }

}


// ===============================
// Logout
// ===============================
function logout() {
    localStorage.clear();
    window.location.href = "/index.html";
}
