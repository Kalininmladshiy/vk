import requests
import random
import os
from utils import download_pictures
from pathlib import Path
from dotenv import load_dotenv


def get_comics(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def send_picture(url, path_to_pictures, filename, key):
    with open(Path() / path_to_pictures / filename, 'rb') as file:
        files = {
            key: file,
         }
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()


def dowload_picture_to_vk(url, payload):
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    client_id = os.environ['VK_CLIENT_ID']
    group_id = os.environ['VK_GROUP_ID']
    access_token = os.environ['VK_ACCESS_TOKEN']
    last_comics_url = 'https://xkcd.com/info.0.json'
    get_wall_server_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    save_wall_photo_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    wall_post_url = 'https://api.vk.com/method/wall.post'
    last_comics = get_comics(last_comics_url)
    comics_num = random.randint(1, last_comics['num'])
    random_comics_url = f'https://xkcd.com/{comics_num}/info.0.json'
    random_comics = get_comics(random_comics_url)
    download_pictures(Path.cwd(), 'python.png', random_comics['img'])
    comment = random_comics['alt']
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
     }
    response = requests.get(get_wall_server_url, params=payload)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    params_for_save_image = send_picture(upload_url, Path.cwd(), 'python.png', 'photo')
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
        'photo': params_for_save_image['photo'],
        'server': params_for_save_image['server'],
        'hash': params_for_save_image['hash'],
     }
    params_for_post_photo = dowload_picture_to_vk(save_wall_photo_url, payload)
    owner_id = params_for_post_photo['response'][0]['owner_id']
    media_id = params_for_post_photo['response'][0]['id']
    payload = {
        'access_token': access_token,
        'v': '5.131',
        'owner_id': f'-{group_id}',
        'from_group': 0,
        'message': comment,
        'attachments': f"photo{owner_id}_{media_id}",
     }
    dowload_picture_to_vk(wall_post_url, payload)
    os.remove(Path.cwd() / 'python.png')
    