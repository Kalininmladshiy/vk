import requests
import random
import os
from utils import download_pictures, send_picture_to_web_site
from pathlib import Path
from dotenv import load_dotenv


def get_comics(comics_num=None):
    if not comics_num:
        url = f'https://xkcd.com/info.0.json'
    else:
        url = f'https://xkcd.com/{comics_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def make_post_request_to_vk(method_name, payload):
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


def make_get_request_to_vk(method_name, payload):
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()    


if __name__ == '__main__':
    load_dotenv()
    client_id = os.environ['VK_CLIENT_ID']
    group_id = os.environ['VK_GROUP_ID']
    access_token = os.environ['VK_ACCESS_TOKEN']
    last_comics = get_comics()
    comics_num = random.randint(1, last_comics['num'])
    random_comics = get_comics(comics_num)
    download_pictures(Path.cwd(), 'python.png', random_comics['img'])
    comment = random_comics['alt']
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
     }
    wall_server = make_get_request_to_vk('photos.getWallUploadServer', payload)
    upload_url = wall_server['response']['upload_url']
    params_for_save_image = send_picture_to_web_site(
        upload_url,
        Path.cwd(),
        'python.png',
        'photo'
     )
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
        'photo': params_for_save_image['photo'],
        'server': params_for_save_image['server'],
        'hash': params_for_save_image['hash'],
     }
    params_for_post_photo = make_post_request_to_vk('photos.saveWallPhoto', payload)
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
    make_post_request_to_vk('wall.post', payload)
    os.remove(Path.cwd() / 'python.png')
    