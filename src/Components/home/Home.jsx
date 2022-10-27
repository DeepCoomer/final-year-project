import React from "react";
import "./home.css"


function Home() {
  return (
    <>
      <div className="container mt-2">
        <div className="row d-flex justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <form action="" className="box">
                <h1>Upload Your Book</h1>
                <input type="text" name="username" placeholder="Authorname" />
                <input type="password" name="password" placeholder="Username" />
                <input type="file" name="file" id="" style={{cursor: "pointer"}} />
                <input type="submit" value="SUBMIT" />
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;
