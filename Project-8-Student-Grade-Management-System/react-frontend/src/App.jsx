import { useState } from 'react'
import Login from './auth/Login'
import StudentList from './students/StudentList';


function App() {
  const [loggedIn, setLoggedIn] = useState(Boolean(localStorage.getItem("access_token")));

  if (!loggedIn){
    return <Login onLogin={() => setLoggedIn(true)}/>
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>
      
      <button onClick={() => {localStorage.removeItem("access_token");
                              setLoggedIn(false);}}>
        Logout
      </button>

      <hr />
      <StudentList />

    </div>
  )
}

export default App
