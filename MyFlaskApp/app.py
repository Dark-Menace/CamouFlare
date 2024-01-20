from flask import Flask, render_template, request, jsonify, send_file
import steganography
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'upload'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png'}
# Ensure the "upload" folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    # Check if the file extension is in the set of allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode', methods=['POST'])

def encode():
    if 'file' not in request.files or 'textData' not in request.form:
        return jsonify({"result":'Invalid request!'}), 400

    image_file = request.files['file']
    
    encoded_message = request.form['textData']
    if encoded_message=='':
        return jsonify({"result":"No data is passed!"}),400
    
    if image_file.filename == '' or  not allowed_file(image_file.filename):
        return jsonify({"result":'Invalid file request!'}), 400
    
    uploaded_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(f"{uploaded_filename}")

    obj=steganography.Steganography(1,uploaded_filename,encoded_message)
    
    Output_filename = os.path.join(app.config['UPLOAD_FOLDER'], "Output.png")

    return send_file(Output_filename, mimetype='image/png', as_attachment=True, download_name='processed_image.png')

    


@app.route('/decode', methods=['POST'])
def decode():
    
    if 'file' not in request.files:
        return jsonify({"result":'Invalid request!'}), 400

    image_file = request.files['file']
    if image_file.filename == '' or  not allowed_file(image_file.filename):
        return jsonify({"result":"Invalid file request!"}), 400

    uploaded_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(f"{uploaded_filename}")
    
    obj=steganography.Steganography(0,uploaded_filename)
    # Return the result to the AngularJS front-end
    return jsonify({"result":"Decoding Successful", "dataFound":obj.decoded_message})

if __name__ == '__main__':
    app.run(debug=True)
