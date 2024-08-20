from flask import Flask, render_template, request, url_for, redirect, session, flash
import re, os
from itertools import groupby
from operator import itemgetter
import calendar
from werkzeug.utils import secure_filename  # Import secure_filename
from flask_session import Session
from functions import extract_github_details, fetch_github_repo_contents, read_text_file
from functions_GPT import comprehend_data

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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

@app.before_request
def set_default_session_variable():
    # Check if the session variable 'git_details' is set, if not set it to an empty string
    if 'git_details' not in session:
        session['git_details'] = ('','')  # Setting default value to an empty string

# Context processor to inject session variables globally
@app.context_processor
def inject_session_variable():
    # Add session variables to the context, like 'username'
    return {'session_git_details': session.get('git_details', '')}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template("index.html")
    
@app.route("/git", methods=['GET', 'POST'])
def git():
    if request.method == 'POST':
        session['git_link'] = request.form.get("file")
        print(session['git_link'])
        session['git_details'] = extract_github_details(session['git_link'])

        return render_template("git.html")

    else:

        return render_template("git.html")
    
@app.route("/pitch", methods=['GET', 'POST'])
def pitch():
    if request.method == 'POST':
        session['pitch_link'] = request.form.get("file")
        print(session['pitch_link'])
        text = """Whoops - this feature isn't actually built yet! Please watch this space. Feel free to use the GitHub upload
        though which does work."""
        return render_template("pitch.html", text=text)

    else:

        return render_template("pitch.html")
    
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':

        # TODO: Abstract below into functions
        files = fetch_github_repo_contents(session['git_details'][0], session['git_details'][1])

        prompt = ''

        for file in files:
            prompt += (f"Path: {file['path']}\nContent: {file['content'][:5000]}...\n")

        mark_scheme = read_text_file("mark_scheme.txt")
        output = comprehend_data(prompt, mark_scheme)

        return render_template("results.html", text=output)

    else:

        return render_template("results.html")




"""
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
"""


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)