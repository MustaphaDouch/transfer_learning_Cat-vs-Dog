import streamlit as st
import numpy as np
import os
import validators
import requests
import cv2
import urllib.request as urlb
import math


st.set_option('deprecation.showfileUploaderEncoding', False)
# Hearders :
os.system('mkdir -p .cache/assets/')
st.title("CATs VS DOGs Classification \n  Model Based on Transfer Learning From MobileNet V2")
st.caption('MobileNet v2 : https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4')
st.caption('Data source : https://www.kaggle.com/competitions/dogs-vs-cats/overview')

st.header("Data Input")

# Input Data :
input_option = st.selectbox('Select your image input type : ',
                            ('Locale (URI)','Web (URL)'))

uploaded_image = None

# setup api request
api_url = f"http://{os.getenv('API_IP', '127.0.0.1')}:{os.getenv('API_PORT', '8000')}/webpred"
# api_url = 'http://127.0.0.1:8000/webpred' 
# api_url = 'http://9797-105-189-18-124.ngrok.io/'

def show_results(resp):
    cat = resp['Cat']*100
    dog = resp['Dog']*100
    color_cat = 'green' if cat >= dog else 'red'
    color_dog = 'green' if dog > cat else 'red'
    col1, col2 = st.columns([1.5 if cat<11.11 else math.floor(cat/10),1.5 if dog<11 else math.floor(dog/10)])

    col1.markdown(f'<h1 style="background-color:{color_cat}; padding:15px ">🐈</h1>', unsafe_allow_html=True)
    col2.markdown(f'<h1 style="background-color:{color_dog};padding:15px;">🐕</h1>', unsafe_allow_html=True)
    col1.metric('CAT', f'{cat:.2f}%')
    col2.metric('DOG', f'{dog:.2f}%')


if input_option == 'Web (URL)':
    uploaded_image = st.text_input('Enter image URL : ')
    while uploaded_image != None:

        if validators.url(uploaded_image) :
            try:                
                response_code = requests.head(uploaded_image)
                
                if response_code.status_code == 200:
                    #set request with header    
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                    request = urlb.Request(uploaded_image, headers = headers)
                    
                    #open url
                    image = urlb.urlopen(request)
                    
                    #image to nparray
                    image_arr  = np.asarray(bytearray(image.read()))
                    
                    #open image with cv2 
                    imgBGR = cv2.imdecode(image_arr, -1)
                    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
                    st.image(imgRGB)  
                    try:
                        resp = requests.get(api_url, params = {'image_url': uploaded_image}).json()

                        show_results(resp)
                    except:
                        st.error('ERROR : API not working', icon="🚨")
                else:   
                    st.error(f'ERROR STATUT CODE {response_code.status_code} : Please Enter a Valid URL', icon="🚨")
            
            except Exception as e :
                st.error(f'ERROR : Please Enter a Valid URL', icon="🚨")

        elif uploaded_image == '':
            pass
        else:
            st.error('ERROR : Please Enter a Valid URL', icon="🚨")
        
        break
    
elif input_option == 'Locale (URI)':
    uploaded_image = st.file_uploader("Choose an Image File")
    while uploaded_image != None:
        #read image from input 
        imgBGR = cv2.imdecode(np.asarray(uploaded_image.getbuffer()), cv2.IMREAD_COLOR)
        imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
        st.image(imgRGB)
        try:
            resp = requests.post(api_url, files={'file':uploaded_image.getbuffer().tobytes()}).json()
            show_results(resp)
        except:
            st.error('ERROR : API not working', icon="🚨")
        break


