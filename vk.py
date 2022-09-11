import requests
import random
import os
from utils import download_picture, upload_picture_to_web_site
from pathlib import Path
from dotenv import load_dotenv


def get_comic_img_num_comment(comics_num=None):
    if not comics_num:
        url = f'https://xkcd.com/info.0.json'
    else:
        url = f'https://xkcd.com/{comics_num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_info = response.json()
    return comic_info['img'], comic_info['num'], comic_info['alt']


def make_post_request_to_vk(method_name, payload):
    url = f'https://api.vk.com/method/{method_name}'
    response = requests.post(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_upload_url_for_vk():
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
    client_id = os.environ['VK_CLIENT_ID']
    group_id = os.environ['VK_GROUP_ID']
    access_token = os.environ['VK_ACCESS_TOKEN']
    comics_num = random.randint(1, get_comic_img_num_comment()[1])
    img, num, comment = get_comic_img_num_comment(comics_num)
    download_picture(Path.cwd(), 'python.png', img)
    try:
        upload_url = get_upload_url_for_vk()
        params_for_save_image = upload_picture_to_web_site(
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
    finally:
        os.remove(Path.cwd() / 'python.png')
    