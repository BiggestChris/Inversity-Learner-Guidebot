# Inversity Learner Guidebot
 Repo for submission to Inversity Learner 1.0

# Flask framework built off of existing projects, Bellingcat Challenge submission was used as a start template

Summary: This project is the technical side of the submission for the Inversity Learner 1.0 challenge. It functions as a web app built using Flask, where users can input the submission so far, and using AI there is a quick check to help the user determine if it as at a respectable standard for submission. Currently ChatGPT API can't read video files, so it is just the GitHub repo that is used to form a judgement.

app.py - this is the main file used for the application, it contains all of the flask routes - important ones are /git which is where GitHub repo is to be uploaded and /results which is where ChatGPT results are run

functions.py - this is where all functions have been abstracted to (except ChatGPT API function)

functions_GPT.py - this is where the ChatGPT function is stored

generic.txt - this is a txt file for testing reader function

mark_scheme.txt - this is the mark scheme from Inversity
Mark scheme from here: https://docs.google.com/spreadsheets/d/1hH1TDBqSC8UYfQsqDrkeexi5l9EdtNnRkdJknYAfZHQ/edit?pli=1&gid=294982527#gid=294982527

requirements.txt - requirements file

test_functions.py - this is a testing file for functions in functions.py to be utilised with Pytest

test_github_api.py - this is a file just to use for running a test of pulling github repos together into one variable

/templates - this folder contains the page templates for flask

/static - this contains static styling data, primarily Inversity favicon and logo and the site CSS (site uses Bootstrap by default)

NOTES: The deployment to Render necessitated creating a GitHub read-only token on User repos (deployment here: https://inversity-learner-guidebot.onrender.com/). Locally, the token wasn't needed but once on render it rate limits all API calls from render without a token, hence the code was updated to reflect this.