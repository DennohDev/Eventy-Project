import React, { useState } from "react";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";

export default function OrganizerRegister() {
  const [username, setUsername] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [phone, setPhone] = useState();

  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const url = "http://localhost:5000";
    fetch(`${url}/organizers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, phone, password }),
    })
      .then((res) => res.json())
      .then((response) => {
        if (response.success) {
          navigate("/");

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

    console.log(username, email, phone, password);
    // Clear your form
    setUsername("");
    setEmail("");
    setPassword("");
    setPhone("");
  };

  return (
    <div className="container d-flex align-items-center justify-content-center vh-100, ">
      <div className="col-md-8 mt-5 card pt-3 pb-4 px-3">
        <h3 className="text-center mt-4">Register as an Organizer</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              type="text"
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Email address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Phone</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-control"
            />
          </div>
          <button type="submit" className="btn btn-success w-100">
            Register
          </button>
        </form>
      </div>
    </div>
  );
}
