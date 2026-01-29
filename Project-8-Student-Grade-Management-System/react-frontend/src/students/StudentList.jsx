import { useEffect, useState } from "react";
import { apiRequest } from '../api/client';

export default function StudentList() {
    const [students, setStudents] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        async function fetchStudents() {
            try {
                const data = await apiRequest("/students/");
                setStudents(data);
            }
            catch (err){
                setError(err.message);
            }
            finally {
                setLoading(false);
            }
        }

        fetchStudents();
    }, []);

    if (loading) return <p>Loading students...</p>;
    if (error) return <p style={{ color: "red"}}>{ error }</p>;

    return (
        <div>
            <h2>Students</h2>

            {students.length == 0 && <p>No students found</p>}

            <table border="1" cellPadding="8">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Average</th>
                        <th>Grade</th>
                    </tr>
                </thead>

                <tbody>
                    {students.map((s) => (
                        <tr key={s.uid}>
                            <td>{s.name}</td>
                            <td>{s.average ?? "-"}</td>
                            <td>{s.grade ?? "-"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}