import os
import json
from app import app
from flask import render_template

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'data.json')

@app.route('/')
def index():
    # Load the data from the JSON file
    with open (DATA_FILE_PATH, 'r') as json_file:
        data = json.load(json_file)

    projects = data['projects']
    work_experience = data['work_experience']
    print(projects)
    print(work_experience)

    return render_template('index.html', projects=projects, work_experience=work_experience)