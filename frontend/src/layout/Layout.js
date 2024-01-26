import React from 'react'
import NavBar from './Navbar'
import Footer from './Footer'
import { Outlet } from 'react-router-dom'

const containerStyle ={
  height: '100vh',
}
function Layout() {
  return (
    <div>
        <NavBar/>
        <div >
            <Outlet/>
        </div>
        <Footer/>
    </div>
  )
}

export default Layout