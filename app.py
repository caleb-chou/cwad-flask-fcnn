from flask import Flask, render_template, redirect, request, flash
import cv2
from mtcnn.mtcnn import MTCNN
from werkzeug.utils import secure_filename

app = Flask(__name__,static_folder='./static')
d = MTCNN()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go',methods=['GET','POST'])
def go():
    if(request.method == 'POST'):
        print(request.files.get('image-file',''))
        if 'image-file' not in request.files:
            return redirect('/')
        image_to_process = request.files['image-file']
        fn = image_to_process.filename
        fn = secure_filename(fn)
        image_to_process.save('./static/images/test.png')
        f = cv2.imread('./static/images/test.png')
        g = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
        faces = d.detect_faces(g)
        for face in faces:
            x = face.get('box')[0]
            y = face.get('box')[1]
            w = face.get('box')[2]
            h = face.get('box')[3]
            cv2.rectangle(f,(x,y), (x+w,y+h), (0,255,0), 2)
        cv2.imwrite('./static/images/test.png',f)
        return render_template('image.html')
    return redirect('/',code=302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=False)