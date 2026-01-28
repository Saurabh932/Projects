import { useState } from 'react'
import Login from './auth/Login'

function App() {
  const [loggedIn, setLoggedIn] = useState(Boolean(localStorage.getItem("access_token")));

  if (!loggedIn){
    return <Login onLogin={() => setLoggedIn(true)}/>
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>
      <p>Logged in</p>
    </div>
  )
}

export default App
