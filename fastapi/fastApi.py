from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from model import predict
import urllib.request as urlb
import numpy as np


app = FastAPI()

@app.get('/')
def Home():
        html = open('index.html', 'r')
        return HTMLResponse(content=html.read(), status_code=200)

#create model object
model = predict()

@app.post('/webpred')
async def predict_web(file:UploadFile = File(...)):
     
        image = await file.read()
        #predict results
        pred = model.prediction(image)
        #format result and return it
        image_pred = pred[0].tolist()
        image_pred = {
            'Cat': image_pred[0],
                #'Cat': f"{image_pred[0]*100:.2f}%",
                #'Dog': f"{image_pred[1]*100:.2f}%"
            'Dog': image_pred[1]
            }
        # print(image_pred)
        return image_pred


@app.get('/webpred')
async def predict_web(image_url):
        print(image_url)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
        request = urlb.Request(image_url, headers = headers)
        #open url
        image = urlb.urlopen(request)
        #image to nparray
        image_arr  = np.asarray(bytearray(image.read()))
        #predict results
        pred = model.prediction(image_arr)
        #format result and return it
        image_pred = pred[0].tolist()
        image_pred = {
            'Cat': image_pred[0],
                #'Cat': f"{image_pred[0]*100:.2f}%",
                #'Dog': f"{image_pred[1]*100:.2f}%"
            'Dog': image_pred[1]
            }
        
        return image_pred


# use ngrok to test api
# from pyngrok import ngrok
# import uvicorn
# ngrok_tunnel = ngrok.connect(8000)
# print('Public URL:', ngrok_tunnel.public_url)
# # nest_asyncio.apply()
# uvicorn.run(app, port=8000)