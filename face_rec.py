import cv2
import face_recognition as fr
import numpy as np
from time import sleep
import pyautogui as pag
from os import path

path = path.dirname(__file__)


while True:

    video_capture = cv2.VideoCapture(0)

    alex = fr.load_image_file(path + "/alex_klein.PNG")
    sergej = fr.load_image_file(path + "/sergej.PNG")
    face_encodings = fr.face_encodings(alex)[0]
    face_encodings += fr.face_encodings(sergej)[0]
    know_face_encodings = [fr.face_encodings(sergej)[0], fr.face_encodings(alex)[0]]

    know_face_names = ["Sergej", "Alex"]

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
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom),  (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 20, bottom), font, 1.0, (255, 255, 255), 1)


        cv2.imshow("Webcam_facereg", frame)
        if cv2.waitKey(1) and 0xFF == ord('q'): 
            break
    video_capture.release()
    cv2.destroyAllWindows()
sleep(10)

