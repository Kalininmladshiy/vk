import requests
import os
from pathlib import Path
from urllib.parse import urlparse


def download_pictures(
    path_to_pictures,
    filename,
    url,
     ):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path() / path_to_pictures / filename, 'wb') as file:
        file.write(response.content)


def send_picture_to_web_site(url, path_to_pictures, filename, key):
    with open(Path() / path_to_pictures / filename, 'rb') as file:
        files = {
            key: file,
         }
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()
