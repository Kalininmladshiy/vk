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
