import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Components/home/Home";
import Login from "./Components/accounts/Login";
import Register from "./Components/accounts/Register";
import Navbar from "./Components/Navbar";
import AddBook from "./Components/AddBook";
import Plagiarism from "./Components/Plagiarism";
import Piracy from "./Components/Piracy";

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/addbook" element={<AddBook></AddBook>}></Route>
          <Route exact path="/plag" element={<Plagiarism></Plagiarism>}></Route>
          <Route exact path="/piracy" element={<Piracy></Piracy>}></Route>
          <Route exact path="/accounts/login" element={<Login />} />
          <Route exact path="/accounts/register" element={<Register />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
