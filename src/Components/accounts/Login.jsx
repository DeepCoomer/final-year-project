import React from 'react';
import { Link } from 'react-router-dom';
import "./login.css";

const Login = () => {
  return (
    <>
    <div className="container mt-2">
      <div className="row d-flex justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <form action="" className="box">
              <h1>Login</h1>
              <p className="text-mutted">Please enter your username and password!</p>
              <input type="text" name="username" placeholder="Username" />
              <input type="password" name="password" placeholder="Password" />
              <Link className="forgot text-muted" to={"#"}>Forgot password?</Link>
              <input type="submit" value="LOGIN" />
              <Link className="forgot text-muted" to={"/accounts/register"}>Don't have an account? Register</Link>
            </form>
          </div>
        </div>
      </div>
    </div>
    </>
  )
}

export default Login