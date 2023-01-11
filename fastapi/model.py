# import pickle
from PIL import Image
import numpy as np
from io import BytesIO
from tensorflow.keras.models import load_model
import tensorflow_hub as hub

class predict():
    def __init__(self):
        # self.model = pickle.load(open('transfer_learning_dog_vs_cat.pkl', 'rb'))
        self.model = load_model('transfer_learning_dog_vs_cat.h5', custom_objects= {'KerasLayer': hub.KerasLayer})
        pass
   


    def read_image(self, uploaded_image):
        image = Image.open(BytesIO(uploaded_image))
        return image


    def img_preprocess(self, image):
        input_shape = (224,224)
        resized_image = image.resize(input_shape)
        rescaled_image = np.asarray(resized_image) /255
        image = np.reshape(rescaled_image, [1, 224, 224, 3])
        return image

    def prediction(self, image):
        image = self.read_image(image)
        image = self.img_preprocess(image)
        #load model and predict result
        prediction = self.model.predict(image)
        return prediction
    
    def webpred(self, image):
        image = self.img_preprocess(image)
        #load model and predict result
        prediction = self.model.predict(image)
        image_pred = prediction[0].tolist()
        image_pred = {
            'Cat': f"{image_pred[0]*100:.2f}%",
            'Dog': f"{image_pred[1]*100:.2f}%"
            }
        return image_pred