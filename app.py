from flask import Flask, render_template, request, url_for, redirect, session, flash
import re, os
from functions import search_director, get_director_details, get_company_details
from itertools import groupby
from operator import itemgetter
import calendar
from werkzeug.utils import secure_filename  # Import secure_filename
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# For uploading
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Define where to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit the maximum file size to 16MB
app.secret_key = 'your_secret_key'  # Required for flash messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


'''
1. Need an index main page with links
- Search for a GitHub repo
- Search for a YouTube vid
- Check results
2. Search for a GitHub repo page
- Enter a GitHub link
- 'Upload'
    - Need to read the link (reject if not a GitHub repo)
    - Go to the GitHub repo with API
    - Write all the files to a message
    - Store the message / give straight to ChatGPT
    - Write ChatGPT response to a variable
3. Search for a YouTube vid
- Enter a YouTube link
- 'Upload'
    - Need to read the link (reject if not a YouTube link)
    - Convert video to file format and pass to ChatGPT (not sure if possible)
    - Store the conversion / give straight to ChatGPT
    - Write ChatGPT response to a variable
4. Check results
- Display combined ChatGPT response so far
'''



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template("index.html")
    
@app.route("/git", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template("git.html")
    
@app.route("/pitch", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template("pitch.html")
    
@app.route("/results", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template("results.html")





@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        # Secure the filename
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        return redirect(url_for('index'))

@app.route('/upload-false', methods=['POST'])
def upload_file_false():
    flash('This function is not built yet')
    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)