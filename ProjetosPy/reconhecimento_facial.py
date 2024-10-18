import cv2
import time
import os
import face_recognition

folder_name = "fotosreco"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)

photo_count = 0
photo_limit = 10  

while photo_count < photo_limit:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and photo_count < photo_limit:  
        photo_name = os.path.join(folder_name, f'foto_{photo_count + 1}.png')
        cv2.imwrite(photo_name, frame)  
        print(f'Foto tirada: {photo_name}')
        photo_count += 1
        time.sleep(1)  

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


base_image_path = os.path.join(folder_name, 'foto_1.png')
base_image = face_recognition.load_image_file(base_image_path)
base_encoding = face_recognition.face_encodings(base_image)[0]

for i in range(2, photo_limit + 1):
    compare_image_path = os.path.join(folder_name, f'foto_{i}.png')
    compare_image = face_recognition.load_image_file(compare_image_path)
    compare_encoding = face_recognition.face_encodings(compare_image)

    if compare_encoding:  
        results = face_recognition.compare_faces([base_encoding], compare_encoding[0])
        face_distance = face_recognition.face_distance([base_encoding], compare_encoding[0])
        similarity_percentage = (1 - face_distance[0]) * 100  
        if results[0]:
            print(f'Foto {i} é semelhante à Foto 1: {similarity_percentage:.2f}%')
        else:
            print(f'Foto {i} NÃO é semelhante à Foto 1: {similarity_percentage:.2f}%')
    else:
        print(f'Nenhuma face encontrada na Foto {i}.')
