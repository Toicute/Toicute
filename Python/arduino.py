import cv2
import serial
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from model import Model
from GUI import MyVideoCapture, App
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

model = Model('model/content/vgg16_finetune.h15')


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.read().decode('utf-8').rstrip()
    return data


while True:
    a = time.time()
    ret, frame = App.update()
    try:
        result = model.predict(frame)
    except:
        print('Lỗi cam')
        result = None
    if result == 'dat':
        send = '2'
    elif result == 'meo':
        send = '3'
    elif result == 'sai_nhan':
        send = '4'
    else:
        send = 'abc'
    value = write_read(send)
    b = time.time()
    print(value)
    print(b-a)
    time.sleep(2)