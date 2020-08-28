import cv2
import face_recognition as fr
import numpy as np
import subprocess
import pyautogui as pag
from time import sleep

locked_status_info = subprocess.run(["gsettings", "get", "org.gnome.desktop.lockdown", "disable-lock-screen"], capture_output=True)
locked = 'true' in str(locked_status_info.stdout)
if not locked:
    x_old,y_old = pag.position()

while True:
    locked_status_info = subprocess.run(["gsettings", "get", "org.gnome.desktop.lockdown", "disable-lock-screen"], capture_output=True)
    locked = 'true' in str(locked_status_info.stdout)
    if locked:
        x, y = pag.position()
        if x_old != x or y_old != y:
            video_capture = cv2.VideoCapture(0)

            alex = fr.load_image_file("IMG_3865_weniger_scharf.jpg")

            alex_face_encoding = fr.face_encodings(alex)[0]

            know_face_encodings = [alex_face_encoding]

            know_face_names = ["Alex"]

            while True:
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
                        
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom),  (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, name, (left + 6, bottom + 6), font, 1.0, (255, 255, 255), 1)


                cv2.imshow("Webcam_facereg", frame)
                if cv2.waitKey(1) and 0xFF == ord('q'): 
                    break
            video_capture.release()
            cv2.destroyAllWindows()
    sleep(1)

