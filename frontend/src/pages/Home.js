import {React,useContext }from 'react'
import { Link } from 'react-router-dom'
import EventList from '../components/HomeCard';
function Home() {

  const containerStyle = {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  };
  return (
    <div  id='home'>
      <div className="container text-center " style={containerStyle}>
        <h1 className="mb-4 display-1">Welcome to Eventy!</h1>
        <p className="lead display-4">
          Discover and join amazing events happening around you.
        </p>
        <div className="d-flex justify-content-center mt-4">
          <button className="btn btn-primary me-3 fs-4"><Link to="login" className="nav-link active text-white">Login</Link></button>
          <button className="btn btn-success fs-4"><Link to="/register" className="nav-link active text-white">Register</Link></button>
        </div>
      </div>
      <div className='mt-5 '>
        <h2 className='fs-1 text-center'>Check out Our Events!</h2>
        <EventList/>
      </div>
    </div>
  )
}

export default Home