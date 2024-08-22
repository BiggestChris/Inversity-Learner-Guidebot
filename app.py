from flask import Flask, render_template, request, url_for, redirect, session, flash
import re, os
from itertools import groupby
from operator import itemgetter
import calendar
from werkzeug.utils import secure_filename  # Import secure_filename
from flask_session import Session
from functions import extract_github_details, fetch_github_repo_contents, read_text_file
from functions_GPT import comprehend_data
from requests.exceptions import RequestException

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
    return render_template("index.html")
    
@app.route("/git", methods=['GET', 'POST'])
def git():
    if request.method == 'POST':
        session['git_link'] = request.form.get("file")
        try:
            session['git_details'] = extract_github_details(session['git_link'])
            return render_template("git.html", text="GitHub read successfully")
        except ValueError:
            return render_template("git.html", text="Invalid GitHub link")

    else:

        return render_template("git.html")
    
@app.route("/pitch", methods=['GET', 'POST'])
def pitch():
    if request.method == 'POST':
        session['pitch_link'] = request.form.get("file")
        session['text'] = """Whoops - this feature isn't actually built yet! Please watch this space. Feel free to use the GitHub upload
        though which does work."""
        return render_template("pitch.html", text=session['text'])

    else:

        return render_template("pitch.html")
    
@app.route("/results", methods=['GET', 'POST'])
def results():
    if request.method == 'POST':

        # TODO: Abstract below into a new function
        # Troubleshooting on Render
        print('Owner: ', session['git_details'][0])
        print('Repo: ', session['git_details'][1])
        try:
            session['files'] = fetch_github_repo_contents(session['git_details'][0], session['git_details'][1])

            session['prompt'] = ''

            for file in session['files']:
                session['prompt'] += (f"Path: {file['path']}\nContent: {file['content'][:5000]}...\n")

            try:
                session['mark_scheme'] = read_text_file("mark_scheme.txt")
            except ValueError:
                print("Text file not found")
                session['mark_scheme'] = 'Mark scheme failed to load, so use your best judgement to determine if this is a working MVP.'

            try:
                session['output'] = comprehend_data(session['prompt'], session['mark_scheme'])
            except RequestException:
                session['output'] = 'Whoops! Something went wrong when feeding into ChatGPT, please try again later.'

            return render_template("results.html", text=session['output'])
            
        except Exception:
            return render_template("results.html", text='Whoops! Something went wrong when trying to read your repo.')


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