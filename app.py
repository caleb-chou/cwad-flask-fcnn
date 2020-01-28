# Imports
from flask import Flask, render_template, redirect, request
from mtcnn.mtcnn import MTCNN
import cv2, base64
import numpy as np
import math

# Constructors
app = Flask(__name__,static_folder='./static') # Webserver
d = MTCNN() # Computer vision

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Processing
@app.route('/go',methods=['GET','POST'])
def go():
    if(request.method == 'POST'):
        print(request.files.get('image-file',''))
        draw = request.form.get('features')

        if 'image-file' not in request.files: # Handle empty/bad post
            return redirect('/')
        image_to_process = request.files['image-file'] # Get data

        # Image Processing
        image_to_process = image_to_process.read()
        image_to_process = np.fromstring(image_to_process, np.uint8)
        f = cv2.imdecode(image_to_process,cv2.IMREAD_COLOR)
        g = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)

        # Find Faces
        faces = d.detect_faces(g)
        for face in faces:
            # print(face)

            x = face.get('box')[0]
            y = face.get('box')[1]
            w = face.get('box')[2]
            h = face.get('box')[3]
            cv2.rectangle(f,(x,y), (x+w,y+h),(0,255,0), 2)

            # Show facial features
            if(not draw == None):
                circle_rad = int(math.ceil(h/25))
                face_feature_color = (0,0,255)

                kp = face.get('keypoints')
                left_eye = kp.get('left_eye')
                cv2.circle(f,left_eye,circle_rad,face_feature_color,2)
                right_eye = kp.get('right_eye')
                cv2.circle(f,right_eye,circle_rad,face_feature_color,2)
                
                nose = kp.get('nose')
                cv2.circle(f, nose, circle_rad, face_feature_color,2)

                mouth_left = kp.get('mouth_left')
                cv2.circle(f,mouth_left,circle_rad,face_feature_color,2)
                mouth_right = kp.get('mouth_right')
                cv2.circle(f,mouth_right,circle_rad,face_feature_color,2)

            retval, buffer = cv2.imencode('.png', f)
        data_uri = base64.b64encode(buffer).decode('ascii')
        return render_template('image.html', image=data_uri)
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=False)