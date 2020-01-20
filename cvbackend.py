import cv2
from mtcnn.mtcnn import MTCNN

class ProcessedIMG:
    def __init__(self, data):
        img = cv2.imread(data, cv2.COLOR_BGR2RGB)
video = cv2.VideoCapture(0)
d = MTCNN()

while True:
    r, f = video.read()
    g = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
    faces = d.detect_faces(g)
    for face in faces:
        x = face.get('box')[0]
        y = face.get('box')[1]
        w = face.get('box')[2]
        h = face.get('box')[3]
        cv2.rectangle(f,(x,y), (x+w,y+h), (0,255,0), 2)
    cv2.imshow('Video',f)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break;
        
video.release()
cv2.destroyAllWindows()