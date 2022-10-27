import React from "react";
import { Link } from "react-router-dom";
import "./register.css";

function Register() {
  return (
    <>
      <div className="container mt-2">
        <div className="row d-flex justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <form action="" className="box">
                <h1>Register</h1>
                <p className="text-mutted">
                  Please enter your username and password!
                </p>
                <input type="text" name="username" placeholder="Username" />
                <div class="form-floating">
                  <select
                    className="form-select"
                    id="floatingSelect"
                    aria-label="Floating label select example"
                  >
                    <option selected>None</option>
                    <option value="1">User</option>
                    <option value="2">Publisher</option>
                  </select>
                  <label for="floatingSelect">Select Your Role</label>
                </div>
                <input type="password" name="password" placeholder="Password" />
                <input type="submit" value="REGISTER" />
                <Link className="forgot text-muted" to={"/accounts/login"}>
                  Back to Login Page
                </Link>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Register;
