import os
import requests
from PIL import Image

def download_image(base_path, padded_num, download_folder):
    img_url = base_path + padded_num + '.jpg'
    try:
        response = requests.get(img_url, timeout=10)
        
        if response.status_code == 200:
            img_path = os.path.join(download_folder, f'{padded_num}.jpg')
            with open(img_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f'Downloaded: {padded_num}.jpg')
            return img_path
        return None
    
    except requests.RequestException as e:
        print(f'Error downloading {padded_num}.jpg: {e}')
        return None