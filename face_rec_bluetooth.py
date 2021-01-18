#!/usr/bin/python3
import cv2
import face_recognition as fr
import numpy as np
from time import sleep
import pyautogui as pag
import subprocess
from verbose import checkIfVerbose
from os import path

path = path.dirname(__file__) + '/'
    
video_capture = cv2.VideoCapture(0)

alex = fr.load_image_file(path + "C:/Users/Alex/Desktop/IMG_3792.jpg")

alex_face_encoding = fr.face_encodings(alex)[0]

know_face_encodings = [alex_face_encoding]

know_face_names = ["Alex"]
x_old = 0
y_old = 0
x = 0
y = 0

bt_status_connected = False
x_old,y_old = pag.position()
wasDisconnected = False
pag.FAILSAFE = False  # disable aborting for mouse moving to a corner of the screen

bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
if "Connected: 1" in str(bt_status_info.stdout):
    bt_status_connected = True

while True:
    if bt_status_connected:
        bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
        # button7location = pag.locateOnScreen('IMG_3934-min.png')
        # while button7location == None:
        #     button7location = pag.locateOnScreen('IMG_3934-min.png', confidence=0.5)
        if wasDisconnected:
            x, y = pag.position()
            if checkIfVerbose():
                print("Get mouse position:" + str(x) + ":" + str(y))
        else:
            x = x_old
            y = y_old
        if "Connected: 1" in str(bt_status_info.stdout):
            if (x_old != x or y_old != y):
                ret, frame = video_capture.read()
                rgb_frame = frame[:, :, ::-1]
                face_locations = fr.face_locations(rgb_frame)
                face_encodings = fr.face_encodings(rgb_frame, face_locations)
                
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = fr.compare_faces(know_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distance = fr.face_distance(know_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distance)
                    if matches[best_match_index]:
                        name = know_face_names[best_match_index]
                        #pag.press('enter')
                        bt_status_info = subprocess.run(["xset", "-q"], capture_output=True)
                        if "Group 2:     on" in str(bt_status_info.stdout):
                            pag.hotkey('shift', 'alt')
                            sleep(0.1)
                        with open(path + "bla.txt", "r") as f:
                            pag.write(f.read())
                        pag.press('enter')   
                        wasDisconnected = False
                        video_capture.release()
                        cv2.destroyAllWindows()
                        video_capture = cv2.VideoCapture(0)
                        break
        else:
            bt_status_connected = False
            wasDisconnected = True 
    else:
        wasDisconnected = True
        bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
        if "Trusted: 0" in str(bt_status_info.stdout):
            subprocess.run(["bluetoothctl", "trust", "3C:2E:FF:7A:58:03"])
        #subprocess.run(["Kristina120804/
        # ", "disconnect", "3C:2E:FF:7A:58:03"])
        connection_status_info = subprocess.run(["bluetoothctl", "connect", "3C:2E:FF:7A:58:03"], capture_output=True)
        connection_status = "Connection successful" in str(connection_status_info.stdout)
        if checkIfVerbose():
            print(str(connection_status_info.stdout))
        if connection_status:
            while not bt_status_connected:
                bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
                if "Connected: 1" in str(bt_status_info.stdout):
                    bt_status_connected = True
                    if checkIfVerbose():
                        print("bluetooth connected")
                    x_old,y_old = pag.position()
                else:
                    sleep(2)
    sleep(1)
video_capture.release()
cv2.destroyAllWindows()

