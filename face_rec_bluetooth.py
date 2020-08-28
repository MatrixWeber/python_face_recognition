import cv2
import face_recognition as fr
import numpy as np
from time import sleep
import pyautogui as pag
import subprocess

while True:
    
    video_capture = cv2.VideoCapture(0)

    alex = fr.load_image_file("IMG_3865_weniger_scharf.jpg")

    alex_face_encoding = fr.face_encodings(alex)[0]

    know_face_encodings = [alex_face_encoding]

    know_face_names = ["Alex"]
    x_old = 0
    y_old = 0

    bt_status_connected = False
    connection_status = False
    x_old,y_old = pag.position()


    while True:
        x, y = pag.position()
        print("Get mouse position:" + str(x) + ":" + str(y))
        if (x_old != x or y_old != y) and connection_status and bt_status_connected:
            bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
            print('Mouse was moved')
            if "Connected: 1" in str(bt_status_info.stdout):
                print("bluetooth connected")
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
                        pag.press('enter')
                        f = open("bla.txt", "r")
                        pag.write(f.read())
                        pag.press('enter')   
                        exit()
        elif not connection_status:
                subprocess.run(["bluetoothctl", "trust", "3C:2E:FF:7A:58:03"])
                subprocess.run(["bluetoothctl", "disconnect", "3C:2E:FF:7A:58:03"])
                connection_status_info = subprocess.run(["bluetoothctl", "connect", "3C:2E:FF:7A:58:03"], capture_output=True)
                connection_status = "Connection successful" in str(connection_status_info.stdout)
                print(str(connection_status_info.stdout))
        bt_status_info = subprocess.run(["bt-device", "-i", "Matrix"], capture_output=True)
        if "Connected: 0" in str(bt_status_info.stdout):
            bt_status_connected = False
            x_old,y_old = pag.position()
            print("bluetooth disconnected")
        else:
            bt_status_connected = True
            print("bluetooth connected")
        sleep(1)
    video_capture.release()
    cv2.destroyAllWindows()

