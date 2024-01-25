import { useState } from 'react'
import './App.css'

function App() {
  const [identity, setIdentity] = useState("world!!");

  const handleIdentityChange = (e) => {
    setIdentity(e.target.value);
  }

  return (
    <>
      <header>
        <h1>hello {identity}</h1>
      </header>
      <input type="text" onChange={handleIdentityChange} />
    </>
  )
}

export default App
