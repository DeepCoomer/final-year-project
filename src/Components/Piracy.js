import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
function Piracy(){

    const[img1Sim,setImg1Sim] = useState("")
    const[img2Sim,setImg2Sim] = useState("")
    const[img1Blur,setImg1Blur] = useState("")
    const[img2Blur,setImg2Blur] = useState("")
    const[imgDim,setImgDim] = useState("")

    const[simscore,setSimScore] = useState("")
    const[blurscore,setBlurscore] = useState({"mean1":1,"mean2":1})

    function onSubmitSim(){
        const formData = new FormData();
        formData.append(
            "img1Sim",
            img1Sim,
            img1Sim.name
        );

        formData.append(
            "img2Sim",
            img2Sim,
            img2Sim.name
        );
        axios.post(`http://127.0.0.1:5002/sift`, formData)
        .then(res => {
            //console.log(res);
            console.log(res.data);
            setSimScore(res.data.score)
        })
    }

    function onSubmitBlur(){
        const formData = new FormData();
        formData.append(
            "img1Blur",
            img1Blur,
            img1Blur.name
        );

        formData.append(
            "img2Blur",
            img2Blur,
            img2Blur.name
        );
        axios.post(`http://127.0.0.1:5002/blurdetection`, formData)
        .then(res => {
            //console.log(res);
            console.log(res.data);
            setBlurscore(res.data)
        })
    }
    

    return(
        <div>
        <div className="container mt-2">
        <div className="row d-flex justify-content-center">
          <div className="col-md-6">
            <div className="card">
              <form action="" className="box">
                <h1>Check Piracy</h1>
                <hr/>
                <h3>Image Similarity</h3>
                <input onChange={(e)=>{setImg1Sim(e.target.files[0])}} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <input onChange={(e)=>{setImg2Sim(e.target.files[0])}} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <Button onClick={()=>{onSubmitSim()}}>Submit</Button>
                <div>Similarity Score is : {simscore*100} </div>

                <hr/>
                <h3>Blur Difference</h3>
                <input onChange={(e)=>{setImg1Blur(e.target.files[0])}} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <input onChange={(e)=>{setImg2Blur(e.target.files[0])}} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <Button onClick={()=>{onSubmitBlur()}}>Submit</Button>
                <div>Blur Score of Image 1 is : {blurscore.mean1} </div>
                <div>Blur Score of Image 2 is : {blurscore.mean2} </div>
                
                <hr/>
                <h3>Dimension</h3>
                <input onChange={(e)=>{setImgDim(e.target.files[0])}} type="file" name="file" id="" style={{cursor: "pointer"}} />
                <Button onClick={()=>{}}>Submit</Button>


              </form>
              
            </div>
          </div>
        </div>
      </div>
    </div>
    
    )
}
export default Piracy