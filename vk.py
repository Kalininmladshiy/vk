import requests
import random
import os
from utils import download_picture, upload_picture_to_vk
from pathlib import Path
from dotenv import load_dotenv


def get_random_comic_img_and_comment():
    last_comic_url = f'https://xkcd.com/info.0.json'
    response = requests.get(last_comic_url)
    response.raise_for_status()    
    last_comic_num = response.json()['num']
    random_comic_num = random.randint(1, last_comic_num)
    random_comic_url = f'https://xkcd.com/{random_comic_num}/info.0.json'
    response = requests.get(random_comic_url)
    response.raise_for_status()
    comic_info = response.json()
    return comic_info['img'], comic_info['alt']


def save_comic_in_vk(group_id, access_token, photo, server, hash_):
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
        'photo': photo,
        'server': server,
        'hash': hash_,
     }    
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    params_for_post_photo = response.json()
    return params_for_post_photo['response'][0]['owner_id'], params_for_post_photo['response'][0]['id']


def publish_comic_in_vk(access_token, group_id, comment, owner_id, media_id):
    payload = {
        'access_token': access_token,
        'v': '5.131',
        'owner_id': f'-{group_id}',
        'from_group': 0,
        'message': comment,
        'attachments': f"photo{owner_id}_{media_id}",
     }    
    url = f'https://api.vk.com/method/wall.post'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_upload_url_for_vk(group_id, access_token):
    payload = {
        'group_id': group_id,
        'access_token': access_token,
        'v': '5.131',
     }    
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']    


if __name__ == '__main__':
    load_dotenv()
    group_id = os.environ['VK_GROUP_ID']
    access_token = os.environ['VK_ACCESS_TOKEN']
    img, comment = get_random_comic_img_and_comment()
    download_picture(Path.cwd(), 'python.png', img)
    try:
        upload_url = get_upload_url_for_vk(group_id, access_token)
        photo, server, hash_ = upload_picture_to_vk(
            upload_url,
            Path.cwd(),
            'python.png',
         )
        owner_id, media_id = save_comic_in_vk(
            group_id,
            access_token,
            photo,
            server,
            hash_,
         )
        publish_comic_in_vk(access_token, group_id, comment, owner_id, media_id)
    finally:
        os.remove(Path.cwd() / 'python.png')
    