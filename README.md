# Inversity Learner Guidebot
 Repo for submission to Inversity Learner 1.0

# Flask framework built off of existing projects, Bellingcat Challenge submission was used as a start template

Summary: This project is the technical side of the submission for the Inversity Learner 1.0 challenge. It functions as a web app built using Flask, where users can input the submission so far, and using AI there is a quick check to help the user determine if it as at a respectable standard for submission. Currently ChatGPT API can't read video files, so it is just the GitHub repo that is used to form a judgement.

app.py - this is the main file used for the application, it contains 




Mark scheme from here: https://docs.google.com/spreadsheets/d/1hH1TDBqSC8UYfQsqDrkeexi5l9EdtNnRkdJknYAfZHQ/edit?pli=1&gid=294982527#gid=294982527




test_functions.py - this is a testing file for functions in functions.py to be utilised with Pytest
test_github_api.py - this is a file just to use for running a test of pulling github repos together into one variable