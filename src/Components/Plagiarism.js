import Button from 'react-bootstrap/Button';
import React, { useState } from "react";
import Form from 'react-bootstrap/Form';
import axios from 'axios';
import ReactTable from "react-table";  

function Plagiarism(){
    const [selectedFile,setSelectedFile] = useState("")
    const [plagData, setPlagData] = useState({data:[]})
    
    function onFileChange(e){
        setSelectedFile(e.target.files[0])
    }
    function onSubmit(){
        //console.log(selectedFile)
        const formData = new FormData();
        formData.append(
            "myFile",
            selectedFile,
            selectedFile.name
        );
        axios.post(`http://127.0.0.1:5001/plag`, formData)
        .then(res => {
            //console.log(res);
            console.log(res.data);
            setPlagData(res.data);
        })

    }
return(
    <div>
        <div className="container mt-2">
        <div className="row d-flex justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <form action="" className="box">
                <h1>Check Plagiarism</h1>

                <input onChange={(e)=>onFileChange(e)} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <Button onClick={()=>{onSubmit()}}>Submit</Button>

              </form>
              {plagData.data.map((plagD, index) => (
                    <div key={index}>
                    <h5>Search {index+1}</h5>
                    <div>Page No: {plagD[0]}</div>
                    <div>Page Data: {plagD[1]}</div>
                    <hr />
                    </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
)
}
export default Plagiarism