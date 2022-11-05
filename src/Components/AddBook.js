import Button from 'react-bootstrap/Button';
import React, { useState } from "react";
import Form from 'react-bootstrap/Form';
import axios from 'axios';


function AddBook() {
  const [bname,setBname] = useState("")
  const [authname,setAuthname] = useState("")

  const [selectedFile,setSelectedFile] = useState("")
  function onFileChange(e){
    setSelectedFile(e.target.files[0])
    console.log(selectedFile)
  }

  function onFileUpload(){

    const json = JSON.stringify({bname,authname});
    const blob = new Blob([json], {
      type: 'application/json'
    });

    const formData = new FormData();
    formData.append(
        "myFile",
        selectedFile,
        selectedFile.name
      );
    formData.append("document", blob);
    console.log(formData)
    //axios({method:'post', url:"http://127.0.0.1:5000/addbook", data:formData});

    axios.post(`http://127.0.0.1:5001/addbook`, formData)
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
  }

  return (
    <>
      <div className="container mt-2">
        <div className="row d-flex justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <form action="" className="box">
                <h1>Upload Your Book</h1>
                <Form.Control onChange={(e)=>{setBname(e.target.value)}} placeholder="Book Name"></Form.Control>
                <Form.Control onChange={(e)=>{setAuthname(e.target.value)}} placeholder="Author Name"></Form.Control>

                <input onChange={(e)=>onFileChange(e)} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <Button onClick={onFileUpload}>Submit</Button>

              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default AddBook;

