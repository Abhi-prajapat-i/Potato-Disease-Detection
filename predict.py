

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf



IMAGE_SIZE =(256,256)
MODEL = tf.keras.models.load_model("model/3")
CLASS_NAME = ["Early Blight", "Late Blight", "Healthy"]



def read_file_as_image(data) -> np.ndarray:
    img = np.array(Image.open(BytesIO(data)))
    return img



def predict_image(
    file: UploadFile = File(...)
):
    img_array = read_file_as_image(file.read())

    img_array = tf.image.resize(img_array,IMAGE_SIZE)

    # img_array = img_array/255.0

    img_batch = np.expand_dims(img_array, 0)
    predicted = MODEL.predict(img_batch, verbose=0)

    predicted_class = CLASS_NAME[np.argmax(predicted[0])]

    confidence = (np.max(predicted[0]))*100

    return predicted_class, confidence