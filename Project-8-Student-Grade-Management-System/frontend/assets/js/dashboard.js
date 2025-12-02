const token = localStorage.getItem("access_token");
if (!token) {
  window.location.href = "/index.html";
}


async function fetchStudents() {
  try {
    const response = await fetch("http://127.0.0.1:8000/students/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

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
        <button class="btn btn-danger" onclick="deleteStudent('${st.uid}')">Delete</button>
      </td>
    `;

    tbody.appendChild(row);
  });
}

fetchStudents();


async function loadStudents(role) {
    try {
        const response = await fetch("/students", {
            method: "GET",
            headers: getAuthHeaders()
        });

        const students = await response.json();
        const table = document.getElementById("students-body");
        table.innerHTML = "";

        students.forEach(s => {
            const row = `
                <tr>
                    <td>${s.name}</td>
                    <td>${s.average ?? "-"}</td>
                    <td>${s.grade ?? "-"}</td>
                    <td>${role === "admin"
                        ? `<button onclick="deleteStudent('${s.uid}')">Delete</button>`
                        : 'View'}
                    </td>
                </tr>`;

            table.innerHTML += row;
        });
    }
    catch (err) {
        console.error("Error loading students:", err);
        alert("Failed loading student data.");
    }
}



function openAddStudentForm(){
    document.getElementById("addStudentModal").style.display = "block";
}

function closeAddStudentForm(){
    document.getElementById("addStudentModal").style.display = "none";
}

async function addStudent(){
    const name = document.getElementById("studentName").value;
    const total_marks = Number(document.getElementById("totalMarks").value);
    const total_sub = Number(document.getElementById("totalSubs").value);

    if (!name || !total_marks || !total_sub){
        alert("All fields are required!");
    }

    try{
        const response = await fetch("/students/add", {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({name, total_marks, total_sub})
        });

        if (!response.ok){
            const data = await response.json();
            alert(data.detail || "Failed to add student.")
            return;
        }
        else {
            alert("Student Added!");
            closeAddStudentForm();
            loadStudents(localStorage.getItem("user_role"))
        }
    }
    catch (error){
        console.error("Error adding student", error);
    }

}