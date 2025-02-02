import os
import json
from app import app
from flask import render_template, abort, request
from PIL import Image, ExifTags
from io import BytesIO
from flask import send_file
from math import ceil

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
    with open (ALBUMS_FILE_PATH, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    albums = data['albums']

    return render_template('albums.html', albums=albums)

@app.route('/albums/<album_id>')
def album(album_id):
    # Load the data from the JSON file
    with open (ALBUMS_FILE_PATH, 'r', encoding='utf-8') as json_file:
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
    pointer = 0
    for file in os.listdir(photo_directory):
        # Check if the file has an image extension
        if file.endswith(('.jpg', '.png', '.jpeg', '.JPG')):
            # Construct the full file path for the image
            photo_path = os.path.join(f'albums/{album_id}', file).replace('\\', '/')
            aspect_ratio = get_aspect_ratio(os.path.join(photo_directory, file))
            photos.append({'path': photo_path, 'aspect_ratio': aspect_ratio, 'name': file})
            pointer += 1
    
    # Sort photos newest first as my best photos are normally later on
    # photos.sort(reverse=True)
    photos.sort(key=lambda x: x['name'], reverse=True)

    # Pagination settings
    per_page = 20  # Number of photos per page
    page = request.args.get('page', 1, type=int)  # Get the current page, default to 1
    total_photos = len(photos)
    total_pages = ceil(total_photos / per_page)

    # Slice the photos for the current page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_photos = photos[start:end]

    return render_template('album.html', album=album, photos=paginated_photos, page=page, total_pages=total_pages)

@app.route('/albums/<album_id>/image/<filename>')
def dynamic_image(album_id, filename):
    # Construct the path to the image
    photo_directory = os.path.join(ALBUMS_PHOTO_PATH, album_id)
    image_path = os.path.join(photo_directory, filename)

    # Check if the image exists, if not return a 404
    if not os.path.exists(image_path):
        return abort(404)

    # Get the query parameters for width and height (defaulting to 800x800 if not provided)
    width = request.args.get('width', default=800, type=int)
    height = request.args.get('height', default=800, type=int)

    # Resize the image
    img_io = resize_image(image_path, width, height)

    # Return the resized image as a response
    return send_file(img_io, mimetype='image/jpeg')

def resize_image(image_path, max_width, max_height):
    with Image.open(image_path) as img:
        # Handle EXIF orientation (rotation)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(orientation)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # In case the image has no EXIF data or we can't access it, just skip
            pass

        # Resize the image
        img.thumbnail((max_width, max_height))      # Resize the image to fit within the dimensions
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=80)        # Save the image into memory (in JPEG format)
        img_io.seek(0)                              # Move the pointer to the start of the BytesIO object
        return img_io
    
def get_aspect_ratio(image_path):
    # Open the image
    img = Image.open(image_path)

    # Fetch the width and height 
    width, height = img.size

    # Attempt to read EXIF data for orientation
    try:
        exif_data = img._getexif()  # Get EXIF data
        if exif_data:
            # Extract orientation tag value (only check 'Orientation' once)
            orientation = next((value for tag, value in exif_data.items() if ExifTags.TAGS.get(tag) == 'Orientation'), None)
            
            # If the orientation requires flipping or rotating, adjust accordingly
            if orientation in {3, 6, 8}:  # Check if it's 180° flip, 90° rotation, or 270° rotation
                return height / width  # The aspect ratio remains unchanged after rotation
    except (AttributeError, KeyError, IndexError):
        pass

    # Get the size (width, height)
    width, height = img.size
    return width / height