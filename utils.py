import requests
import os
from pathlib import Path
from urllib.parse import urlparse


def download_picture(
    path_to_pictures,
    filename,
    url,
     ):
    response = requests.get(url)
    response.raise_for_status()
    with open(Path() / path_to_pictures / filename, 'wb') as file:
        file.write(response.content)


def upload_picture_to_vk(url, path_to_pictures, filename):
    with open(Path() / path_to_pictures / filename, 'rb') as file:
        files = {
            'photo': file,
         }
        response = requests.post(url, files=files)
    response.raise_for_status()
    params_for_save_image = response.json()
    return params_for_save_image['photo'], params_for_save_image['server'], params_for_save_image['hash']
