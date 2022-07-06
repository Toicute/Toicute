import tkinter
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, BOTTOM, Y, StringVar
from tkinter.ttk import Frame, Button, Entry, Style, Label
import PIL.ImageTk, PIL.Image
from tkinter import Frame
import cv2
import serial
import time
import numpy as np
import tensorflow as tf
# from tensorflow.keras import models
from model import Model
from threading import Thread
x = 0
class App:
    def __init__(self, window, window_title, path, video_source=0):
        super().__init__()
        # Gọi model và khởi tạo arduino
        self.model = Model(path)
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
        self.sovat = 0

        # Tạo cửa sổ GUI
        self.window = window
        self.window.title = window_title
        self.video_source = video_source
        self.vid = MyVideoCapture(video_source)


        self.frame1 = Frame()
        self.frame1.pack(fill=X)
        self.canvas = tkinter.Canvas(self.frame1, width=self.vid.width, height=self.vid.height)
        self.canvas.pack(side=LEFT)

        self.canvas_2 = tkinter.Canvas(self.frame1,  width=300, height=self.vid.height)
        self.canvas_2.pack(side=RIGHT)
        self.frame2 = Frame()
        self.frame2.pack(fill=BOTH)
        self.label = Label(self.frame2, text=f"Đây là số vật {self.sovat}", font=("Arial Bold", 50))
        self.label.pack(side=LEFT)
        self.delay = 15

        self.update()
        self.window.mainloop()

    def write(self, x):
        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)

    def read(self):
        data = self.arduino.read().decode('utf-8').rstrip()
        return data

    def predict(self, frame):
        if self.read() == '9':
            self.crop = frame[:,  130:420]
            pred = self.model.predict(frame)
            if pred == 'meo':
                send = '3'
            elif pred == 'sai_nhan':
                send = '4'
            else:
                send = 'abc'
            print(pred)
            self.write(send)
            self.sovat += 1
            print(f'Phát hiện vật, số vật là {self.sovat}')
            self.label.configure(text=f"Đây là số vật {self.sovat}")
            self.crop = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.crop))
            self.canvas_2.create_image(1, 0, image=self.crop, anchor=tkinter.NW)

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        thread = Thread(target=self.predict(frame))
        thread.start()
        self.window.after(self.delay, self.update)

        # if i>50:
        #     self.crop = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(crop))
        #     self.canvas2.create_image(1, 0, image=self.crop, anchor=tkinter.NW)
        #     pred = self.model.predict(frame)
        #     if pred == 'meo':
        #         send = '3'
        #     elif pred == 'sai_nhan':
        #         send = '4'
        #     else:
        #         send = 'abc'
        #     print(pred)
        #     self.write(send)
        #     self.sovat += 1
        #     print(f'Phát hiện vật, số vật là {self.sovat}')
        #     self.label.configure(text=f"Đây là số vật {self.sovat}")
        #     i = 0
        # i += 1

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise Exception

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

i = 0
ret, frame = App(tkinter.Tk(), "Tkinter and OpenCV", path='model/content/vgg16_finetune.h15')


# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.read().decode('utf-8').rstrip()
#     return data
#
# a = time.time()
# try:
#     result = model.predict(frame)
# except:
#     print('Lỗi cam')
#     result = None

# value = write_read(send)
# b = time.time()
# print(value)
# print(b-a)
# time.sleep(2)