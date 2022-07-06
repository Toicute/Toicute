import cv2
from tensorflow.keras import models
import numpy as np

# Khởi tạo model, cần truyền vào đường dẫn đến model
class Model():
    def __init__(self, path):
        self.path = path
        self.model = models.load_model(path)
        self.class_name = ['dat', 'meo', 'sai_nhan']

    # Gọi predict, truyền vào khung hình cần dự đoán
    def predict(self, frame):
        frame = cv2.resize(frame, (224, 224))
        frame = np.expand_dims(frame, axis=0)
        pred = self.model.predict(frame)
        pred = np.argmax(pred, axis=1)
        result = self.class_name[pred[0]]

        return result

