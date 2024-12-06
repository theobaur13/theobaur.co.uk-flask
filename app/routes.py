import os
import json
from app import app
from flask import render_template, abort

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'data.json')
ALBUMS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'albums.json')
ALBUMS_PHOTO_PATH = os.path.join(os.path.dirname(__file__), 'static', 'albums')

@app.route('/')
def index():
    # Load the data from the JSON file
    with open (DATA_FILE_PATH, 'r') as json_file:
        data = json.load(json_file)

    projects = data['projects']
    employment = data['employment']

    return render_template('index.html', projects=projects, employment=employment)

@app.route('/albums')
def albums():
    # Load the data from the JSON file
    with open (ALBUMS_FILE_PATH, 'r') as json_file:
        data = json.load(json_file)

    albums = data['albums']

    return render_template('albums.html', albums=albums)

@app.route('/albums/<album_id>')
def album(album_id):
    # Load the data from the JSON file
    with open (ALBUMS_FILE_PATH, 'r') as json_file:
        data = json.load(json_file)

    # Find the album with the matching album_id
    album = next((album for album in data['albums'] if album['album_id'] == album_id), None)

    if album is None:
        # If no matching album is found, handle the error (e.g., show a 404 page)
        return abort(404)
    
    # Get the photo directory path for the specific album
    photo_directory = os.path.join(ALBUMS_PHOTO_PATH, album_id)

    # Check if the directory exists, if not return a 404
    if not os.path.exists(photo_directory):
        return abort(404)

    # List all the images in that directory
    photos = []
    for file in os.listdir(photo_directory):
        # Check if the file has an image extension
        if file.endswith(('.jpg', '.png', '.jpeg', '.JPG')):
            # Construct the full file path for the image
            photo_path = os.path.join(f'albums/{album_id}', file).replace('\\', '/')
            photos.append(photo_path)
    
    # Sort photos newest first as my best photos are normally later on
    photos.sort(reverse=True)

    return render_template('album.html', album=album, photos=photos)