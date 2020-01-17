from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/go',methods=['POST'])
def go():
   return redirect('/',302)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=False)