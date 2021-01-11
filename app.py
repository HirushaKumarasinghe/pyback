# import wordworks
# import trained_data_extractor
import os      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from docx2pdf import convert



app = Flask(__name__)

app.secret_key = "secret key" # for encrypting the session

#It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
IMG_UPLOAD_FOLDER = os.path.join(path, 'imguploads')


# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('/upload.html')

@app.route('/doc', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            print()
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/')

@app.route('/img', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            print()
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['IMG_UPLOAD_FOLDER'], filename))
        flash('File(s) successfully uploaded')
        return redirect('/')

# @app.route('/anlyse')
# def resume_analyser():
#     return trained_data_extractor.gather_data('pdf','')

if __name__ == '__main__':
    app.run()
