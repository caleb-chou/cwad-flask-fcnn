from flask import Flask, render_template, redirect, request, flash
import cv2, base64
import numpy as np
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle

app = Flask(__name__,static_folder='./static')
d = MTCNN()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go',methods=['GET','POST'])
def go():
    if(request.method == 'POST'):
        print(request.files.get('image-file',''))
        if 'image-file' not in request.files: # Handle empty/bad post
            return redirect('/')
        image_to_process = request.files['image-file'] # Get data
        image_to_process = image_to_process.read()
        image_to_process = np.fromstring(image_to_process, np.uint8)
        f = cv2.imdecode(image_to_process,cv2.IMREAD_COLOR)
        g = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        faces = d.detect_faces(g)
        for face in faces:
            x = face.get('box')[0]
            y = face.get('box')[1]
            w = face.get('box')[2]
            h = face.get('box')[3]
            cv2.rectangle(f,(x,y), (x+w,y+h), (0,255,0), 2)
            retval, buffer = cv2.imencode('.png', f)
        data_uri = base64.b64encode(buffer).decode('ascii')
        return render_template('image.html', image=data_uri)
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=False)