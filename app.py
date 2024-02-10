# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['RESULTS_FOLDER'] = 'results/'
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part'

    name = request.form.get('name', '').lower()
    cnic = request.form.get('cnic', '').lower()
    passport_number = request.form.get('passport_number', '').lower()

    files = request.files.getlist('files')
    results = []

    for file in files:
        if file.filename == '':
            continue

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        model = ocr_predictor(pretrained=True)
        img = DocumentFile.from_images(file_path)
        result = model(img)
        output = result.export()

        full_text = " ".join([obj3["value"] for obj1 in output['pages'][0]["blocks"] for obj2 in obj1["lines"] for obj3 in obj2["words"]])

        name_found = name in full_text.lower() if name else False
        cnic_found = cnic in full_text.lower() if cnic else False
        passport_number_found = passport_number in full_text.lower() if passport_number else False

        found = name_found or cnic_found or passport_number_found
        result_info = []

        if name_found:
            result_info.append(f"Name found in:\n- {filename}")
        if cnic_found:
            result_info.append(f"CNIC found in:\n- {filename}")
        if passport_number_found:
            result_info.append(f"Passport number found in:\n- {filename}")

        status = 'found' if found else 'not found'
        results.append((filename, status, result_info))

    response = "<br>".join([f"{filename}: {status}<br>{', <br>'.join(result_info)}\n" for filename, status, result_info in results])
    # return response if results else 'No files processed'
    return render_template('results_page.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
