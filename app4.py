from flask import Flask,request
from flask_cors import CORS, cross_origin
import urllib
import cv2
import numpy as np
import math
from keras.models import load_model
import PIL

app = Flask(__name__)
cors = CORS(app)


def wrapPrespective(red_point,green_point,black_point,blue_point,givenimg):
    point_matrix = np.float32([red_point,green_point,black_point, blue_point])
    height,width,_ = givenimg.shape
    point_matrix = np.float32([red_point,green_point,black_point, blue_point])
    converted_red_pixel_value = [0,0]
    converted_green_pixel_value = [width,0]
    converted_black_pixel_value = [0,height]
    converted_blue_pixel_value = [width,height]
    converted_points = np.float32([converted_red_pixel_value,converted_green_pixel_value,converted_black_pixel_value,converted_blue_pixel_value])
    perspective_transform = cv2.getPerspectiveTransform(point_matrix,converted_points)
    givenimg = cv2.warpPerspective(givenimg,perspective_transform,(width,height))
    return givenimg
    

@app.route("/sift",methods=["POST","GET"])
@cross_origin()
def sift():
    if request.method=="POST":
        req = request.files
        req["img1Sim"].save("img1Sim.jpg")
        req["img2Sim"].save("img2Sim.jpg")

        img1 = cv2.imread("img1Sim.jpg")
        img2 = cv2.imread("img2Sim.jpg")

        
        #SIFT
        sift = cv2.SIFT_create()
        keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
        
        ##Flann
        index_parms = dict(algorithm=0,tree=5)
        search_parms = dict()
        flann = cv2.FlannBasedMatcher(index_parms,search_parms)
        matches = flann.knnMatch(descriptors_1,descriptors_2,k=2)
        good_points = []
        for m,n in matches:
            if m.distance<0.6*n.distance:
                good_points.append(m)
        key_points_considered = min(len(keypoints_1),len(keypoints_2))
        flann_score = len(good_points)/key_points_considered

        ##Brute
        matches = cv2.BFMatcher().knnMatch(descriptors_1, descriptors_2, k=2)
        good = [[m] for m, n in matches if m.distance < 0.7*n.distance]
        brute_score = len(good)/key_points_considered
        #img3 = cv2.drawMatchesKnn(img_OutputOne, keypoints_1, img_OutputTwo, keypoints_2, good, None, matchColor=(0, 255, 0), matchesMask=None, singlePointColor=(255, 0, 0), flags=0)
        #print(brute_score)
        #cv2.imshow("frame",img3)
        #cv2.waitKey(0)
        
        #print(img1Url,img2Url,img1Coord,img2Coord)
        return {"score":(flann_score+brute_score)/2}
        

    return {}

@app.route("/dimension",methods=["POST","GET"])
@cross_origin()
def dimension():
    def euclidienDistance(y1,y2,x1,x2):
        temp1 = abs(y2-y1)*abs(y2-y1)
        temp2 = abs(x2-x1)*abs(x2-x1)
        return math.sqrt(temp1+temp2)
    
    if request.method=="POST":
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        req = request.json
        #print(req['imgURL'],req['coOrds'])
    
        img2 = urllib.request.urlopen(req['imgURL'])
        temparr = np.asarray(bytearray(img2.read()), dtype=np.uint8)
        img2 = cv2.imdecode(temparr, -1)
        
        ### Wrap ###
        red_point = req['coOrds'][0]
        green_point = req['coOrds'][1]
        black_point = req['coOrds'][2]
        blue_point = req['coOrds'][3]
        #print(red_point,green_point,black_point,blue_point)
        #img2 = wrapPrespective(red_point,green_point,black_point,blue_point,img2)
        #cv2.imshow("frame1",img2)
        #cv2.waitKey(5000)
        #cv2.imwrite("filename.jpg", img2)
        
        corners, ids, rejected= cv2.aruco.detectMarkers(img2, aruco_dict, parameters=parameters)
        int_corners = np.int0(corners)
        cv2.polylines(img2, int_corners, True, (0, 255, 0), 5)
        #print(corners)
        #cv2.imshow("frame",img2)
        #cv2.waitKey(0)
        for i in range(len(ids)):
            if ids[i]==10:
                temp = corners[i]
                break
        temp = temp.tolist()[0]
        #print(temp,"<<<<<<<<<")
        #print(temp[2][1])
        x = euclidienDistance(temp[0][0],temp[1][0],temp[0][1],temp[1][1])
        y = euclidienDistance(temp[1][0],temp[2][0],temp[1][1],temp[2][1])
        #print(x,y)
        
        temp3 = req['coOrds']
        #temp3 = [[0,0],[1,0],[0,1],[1,1]]
        #lengthCord = euclidienDistance(temp3[0][0],temp3[1][0],temp3[0][1],temp3[1][1])
        #widthCord = euclidienDistance(temp3[2][0],temp3[3][0],temp3[2][1],temp3[3][1])
        lengthCord = img2.shape[1]
        widthCord = img2.shape[0]
        #print(lengthCord,widthCord)
        length = (lengthCord*3)/x
        
        width = (widthCord*3)/y
        print(length,width)
        return {"length":length,"width":width}
    return {}
        
@app.route("/fontdetection",methods=["POST","GET"])
@cross_origin()
def fontdetection():
    model = load_model('top_model.h5')
    score = model.evaluate(testX, testY, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    
    img2 = urllib.request.urlopen(req['imgURL'])
    temparr = np.asarray(bytearray(img2.read()), dtype=np.uint8)
    img2 = cv2.imdecode(temparr, -1)
    
    img_path="sample.jpg"
    pil_im =PIL.Image.open(img_path).convert('L')
    pil_im=blur_image(pil_im)
    org_img = img_to_array(pil_im)
    def rev_conv_label(label):
        if label == 0 :
            return 'Lato'
        elif label == 1:
            return 'Raleway'
        elif label == 2 :
            return 'Roboto'
        elif label == 3 :
            return 'Sansation'
        elif label == 4:
            return 'Walkway'
    data=[]
    data.append(org_img)
    data = np.asarray(data, dtype="float") / 255.0
    y = np.argmax(model.predict(data),axis=1)
    label = rev_conv_label(int(y[0]))

    print(label)

@app.route("/blurdetection",methods=["POST","GET"])
@cross_origin()
def blurDetection():
    if request.method == "POST":
        def detect_blur_fft(image, size=60, thresh=10, vis=False):
            (h, w, _) = image.shape
            (cX, cY) = (int(w / 2.0), int(h / 2.0))
            fft = np.fft.fft2(image)
            fftShift = np.fft.fftshift(fft)
            
            fftShift[cY - size:cY + size, cX - size:cX + size] = 0
            fftShift = np.fft.ifftshift(fftShift)
            recon = np.fft.ifft2(fftShift)
            magnitude = 20 * np.log(np.abs(recon))
            mean = np.mean(magnitude)
            return mean
        def blurChecker(img):
            mean = detect_blur_fft(img)
            #print(mean)
            cummulativeMean = 0
            i = 1
            for radius in range(1, 30, 2):
                image = img.copy()
                if radius > 0:
                    i+=1
                    image = cv2.GaussianBlur(image, (radius, radius), 0)
                    mean = detect_blur_fft(image)
                    cummulativeMean+=mean
            return abs((cummulativeMean/i)-mean)

        
        req = request.files
        req["img1Blur"].save("img1Blur.jpg")
        req["img2Blur"].save("img2Blur.jpg")

        img1 = cv2.imread("img1Blur.jpg")
        img2 = cv2.imread("img2Blur.jpg")
        
        
        mean1 = cv2.Laplacian(img1, cv2.CV_64F).var()
        mean2 = cv2.Laplacian(img2, cv2.CV_64F).var()

        print(mean1,mean2,mean1,mean2)


        return ({"mean1":mean1,"mean2":mean2})
    return {}

if __name__=="__main__":
    app.run(debug=True,port=5002)