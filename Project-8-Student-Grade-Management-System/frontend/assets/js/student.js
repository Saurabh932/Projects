const tokenStd = localStorage.getItem("access_token");
const role = localStorage.getItem("user_role"); 

if (!tokenStd) window.location.href = "../index.html";

const urlParams = new URLSearchParams(window.location.search);
const studentName = urlParams.get("name");

document.getElementById("studentName").innerText = studentName;

// Renamed for clarity: this should hold the Subject UID for editing
let currentSubjectUID = null; 

//===========================================
// Fetch Details
//===========================================
async function fetchStudentDetails(){
    try{
        const response = await fetch(`http://127.0.0.1:8000/grade/${studentName}`,{
            headers: {'Authorization':`Bearer ${tokenStd}`}
        });

        const data = await response.json();
        console.log(data);

        document.getElementById("avg").innerText = data.average ?? "-";
        document.getElementById("grade").innerText = data.grade ?? "-";

        renderSubjects(data.subjects);
    }
    catch(error){
        console.log(error);
        alert("Failed to load students details.");
    }
}


//===========================================
// Rendering Student Tables
//===========================================
function renderSubjects(subjects){
    const tbody = document.getElementById("subjectBody");
    tbody.innerHTML = "";

    subjects.forEach(s => {
        const actions = role === "admin"
            ? `
                <button onclick="openEditModal('${s.uid}', ${s.marks_obtain}, ${s.max_marks}, '${s.teacher_name ?? ""}')">Edit</button>
                <button onclick="deleteSubject('${s.uid}')">Delete</button>
                ` 
            : 'No action';

        const row = `
        <tr>
            <td>${s.subject_name}</td>
            <td>${s.marks_obtain}</td>
            <td>${s.max_marks}</td>
            <td>${s.teacher_name ?? "-"}</td>
            
            <td>${actions}</td>
        </tr>`;

        tbody.innerHTML += row;
    });
}


//===========================================
// Opening Edit Modal
//===========================================
function openEditModal(uid, marks, maxMarks, teacherName){
    // Assign the uid of the subject being edited
    currentSubjectUID = uid;
    document.getElementById("editMarks").value = marks;
    document.getElementById("editMaxMarks").value = maxMarks;
    document.getElementById("editTeacherName").value = teacherName || "";

    document.getElementById("editSubjectModal").style.display = "block";
}


function closeEditModal(){
    // Ensure the correct variable is cleared
    currentSubjectUID = null; 
    document.getElementById("editSubjectModal").style.display="none";
}


//===========================================
// Updating Subject
//===========================================
async function updateSubject(){
    // Use the correct variable name
    if (!currentSubjectUID) return; 

    const marks_obtain = Number(document.getElementById("editMarks").value);
    const max_marks = Number(document.getElementById("editMaxMarks").value); 
    const teacher_name = document.getElementById("editTeacherName").value;

    try{
        // Use the correct variable for UID in the URL
        const response = await fetch(`http://127.0.0.1:8000/grade/subject/${currentSubjectUID}`, {
            method:"PATCH",
            headers:{"Authorization":`Bearer ${tokenStd}`,
                     "Content-Type":"application/json"},
            body: JSON.stringify({marks_obtain, max_marks, teacher_name})
        });

        if (!response.ok) return alert("update failed");

        alert("Subject Updated Successfully!");
        closeEditModal();
        fetchStudentDetails();
        }
    catch(err){
        console.error(err);
    }
}


//===========================================
// Deleting Subject
//===========================================
async function deleteSubject(uid){
    if (!confirm("Delete this subject?")) return;

    try{
        const response = await fetch(`http://127.0.0.1:8000/grade/subject/${uid}`,{
            method:"DELETE",
            headers: {"Authorization":`Bearer ${tokenStd}`}
        });

        if (!response.ok) return alert("Failed to delete!");
        alert("Subject deleted!"); // Changed alert to 'Subject deleted!'
        fetchStudentDetails();
    }
    catch(err){
        console.error(err);
    }
}


function goBack(){
    window.location.href = "/pages/dashboard.html"
}


fetchStudentDetails();