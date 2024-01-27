import React, {useState} from 'react'
import Swal from "sweetalert2"
import {useNavigate} from "react-router-dom"

export default function OrganizerLogin() 
{

  const [username, setUsername] = useState();
  const [password, setPassword] = useState();

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const url = "https://eventy-project.onrender.com";
    fetch(`${url}/organizers/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username,  password }),
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.success) {
          navigate("/organizers/home");

          Swal.fire({
            position: "center",
            icon: "success",
            title: response.success,
            showConfirmButton: false,
            timer: 1500,
          });
        } else {
          Swal.fire({
            position: "center",
            icon: "error",
            title: response.error,
            showConfirmButton: false,
            timer: 1500,
          });
        }
      });

    console.log(username,  password);
    // Clear your form
    setUsername("");
    setPassword("");
  };
  
  const containerStyle = {
    minheight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  }
  return (
    <div  style={containerStyle}>
      <div className='col-md-6 mt-5 card pt-3 pb-4 px-3 '>
        <h3 className='text-center mt-4'>Organizer Login</h3>
        <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input value={username} onChange={ e => setUsername(e.target.value)} type="text" className="form-control" />
        </div>
       
        <div className="mb-3">
          <label className="form-label">Password</label>
          <input type="password"  value={password} onChange={ e => setPassword(e.target.value)} className="form-control"/>
        </div>
          <button type="submit" className="btn btn-success w-100">Login</button>
        </form>
      </div>

     
    </div>
  )
}
