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

def get_file_extension(url):
    url_parts = urlparse(url)
    path, file_extension = os.path.splitext(url_parts.path)
    return file_extension
