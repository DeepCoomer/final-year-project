from flask import Flask,request
from flask_cors import CORS, cross_origin
import urllib
import cv2
import numpy as np
import math
from keras.models import load_model
import PIL
import PyPDF2 
import os
import json
import pymongo
from PIL import Image
import easyocr
import pytesseract
from difflib import SequenceMatcher 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

app = Flask(__name__)
cors = CORS(app)

    

@app.route("/addbook",methods=["POST","GET"])
@cross_origin()
def addbook():
    
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/?retryWrites=true&w=majority")
    db = client.majorproject
    coll = db.addbook

    if request.method=="POST":
        req = request.files
        print(req)
        
        print(req['myFile'])
        jsonData = json.load(req['document'])
        try:
            os.remove("tempfile.pdf")
        except:
            pass
        req['myFile'].save("tempfile.pdf")
        
        ### PDF File Extraction ###
        pdfFileObj = open('tempfile.pdf', 'rb') 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        bookText = {}
        for i in range(0,pdfReader.numPages):
            pageObj = pdfReader.getPage(i) 
            extractedText = pageObj.extractText()
            bookText[f"page {i+1}"] = extractedText

        
        #retdata = {"bname": json.load(req['document'])["bname"]}
        jsonData["bookdata"] = bookText
        print(jsonData)
        coll.insert_one(jsonData)
        pdfFileObj.close()
    return {}

@app.route("/plag",methods=["POST","GET"])
@cross_origin()
def plag():
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.wonbr.mongodb.net/?retryWrites=true&w=majority")
    db = client.majorproject
    coll = db.addbook

    reader = easyocr.Reader(['en'])
    if request.method=="POST":
        req = request.files
        #print(req['myFile'])
        req['myFile'].save("tempImg.png")
        result = reader.readtext('tempImg.png',paragraph="False")
        #print(result)
        
        detectedText = ""
        for ele in result:
            print(ele[-1])
            detectedText = detectedText +" "+ ele[-1]
        #print(detectedText)
        plagScore = []
        for x in coll.find():
            temp = x["bookdata"]
            for k,v in temp.items():
                #print(type(detectedText),type(v))
                #print(SequenceMatcher(None,detectedText,v).ratio()*100)
                plgscore = SequenceMatcher(None,detectedText,v).ratio()*100
                
                if plgscore>10:
                    plagScore.append((k,v))
    print(plagScore)
    return {"data":plagScore}


if __name__=="__main__":
    app.run(debug=True,port=5001)