from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Path to Tesseract executable (Change this to your own path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


@app.route('/')
def index():
    return render_template('new.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            extracted_text = extract_text_from_image(file_path)
            return render_template('new.html', text=extracted_text, filename=filename, uploaded=True)


        return render_template('new.html', filename=filename, uploaded=True)

    else:
        return 'File type not allowed'


if __name__ == '__main__':
    app.run(debug=True)
