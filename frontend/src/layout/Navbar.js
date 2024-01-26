import React from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import { useContext } from "react";

function NavBar() {
  const { currentUser, logout } = useContext(UserContext);
  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark bg-danger">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            {/* <img src="" alt="Marvel Logo"
                            width="80" height="40" /> */}
            Eventy!
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              {currentUser && currentUser.username ? (
                <>
                  <li className="nav-item">
                    <Link to="/Events" className="nav-link">
                      Events
                    </Link>
                  </li>
                  <li className="nav-item">
                    <Link to="/Profile" className="nav-link">
                      Profile
                    </Link>
                  </li>
                </>
              ) : (
                null
              )}
            </ul>
            {currentUser && currentUser.username && (
              <button
                className="btn btn-outline-warning"
                onClick={() => logout()}
              >
                Logout
              </button>
            )}
            {!currentUser &&  (
              <Link to= "/Organizers"><button
              className="btn btn-success"
            >
              For Organizers
            </button></Link>
            )}
          </div>
        </div>
      </nav>
    </div>
  );
}

export default NavBar;
