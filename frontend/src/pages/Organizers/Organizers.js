import React from 'react'
import { Link } from 'react-router-dom'

function Organizers() {
  const backgroundImageUrl = 'url("https://images.unsplash.com/photo-1502899135311-704d7e22d0fa?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")';

  const containerStyle = {
    backgroundImage: backgroundImageUrl,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    color: 'white',
  };
  return (
    <div style={containerStyle}>
      <div className="container text-center">
        <h2 className="mb-4 display-1">Are you an organizer?</h2>
        <p className="lead display-4">
          Join us today and use the Eventy platform to manage your events.
        </p>
        <div className="d-flex justify-content-center mt-4">
          <button className="btn btn-primary me-3 fs-4"><Link to="/organizers/login" className="nav-link active text-white">Login</Link></button>
          <button className="btn btn-success fs-4"><Link to="/organizers/register" className="nav-link active text-white">Register</Link></button>
        </div>
      </div>
    </div>
  )
}

export default Organizers