import face_recognition
import cv2
import numpy as np
import os
import serial
import smtplib
import imghdr
from email.message import EmailMessage

s = serial.Serial('COM1',9600)

CurrentFolder = os.getcwd() 
image = CurrentFolder+'\\Deeptimaan.jpg'

video_capture = cv2.VideoCapture(0)

Rahul_image = face_recognition.load_image_file(image)
Rahul_face_encoding = face_recognition.face_encodings(Rahul_image)[0]


known_face_encodings = [
    Rahul_face_encoding
]
known_face_names = [
    "Deeptimaan"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    print("waiting for bell input")
    serial_data = s.read()
    if(serial_data == b'a'):
        while(1):
            ret, frame = video_capture.read()

    
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            
            rgb_small_frame = small_frame[:, :, ::-1]

        
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)
                    if(name == "Unknown"):
                        s.write(b'0')
                        i = 0
                        serial_data = s.read()
                        if(serial_data == b'p'):
                            print(" Memebers present inside home no need to send image")
                        elif(serial_data == b'q'):
                            while i < 10:
                                print("sending image on mail")
                                return_value, image = video_capture.read()
                                cv2.imwrite('opencv.png', image)
                                i += 1
                                Sender_Email = "deeptimaankrishnajadaun@gmail.com"
                                Reciever_Email = "developer54452@gmail.com"
                                Password = "cjbjqxhxpzqsymso" 
                                newMessage = EmailMessage()                         
                                newMessage['Subject'] = "Alert Theft inside your home" 
                                newMessage['From'] = Sender_Email                   
                                newMessage['To'] = Reciever_Email                   
                                newMessage.set_content('Let me know what you think. Image attached!') 
                                with open('opencv.png', 'rb') as f:
                                    image_data = f.read()
                                    image_type = imghdr.what(f.name)
                                    image_name = f.name
                                newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                                    smtp.login(Sender_Email, Password)              
                                    smtp.send_message(newMessage)
                    elif(name == "Deeptimaan"):
                        s.write(b'1')
                        
            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a 
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a 
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display 
            cv2.imshow('Video', frame)

            # Hit 'q' o
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
video_capture.release()
cv2.destroyAllWindows()
