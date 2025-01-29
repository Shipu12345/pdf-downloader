import os
import re
import time
import urllib.parse
import shutil

from image_processor.image_manipulator import compress_image_with_quality
from image_processor.image_downloader import download_image
from pdf_maker.pdf_maker import make_pdf

def download_and_convert_images( base_url: str, max_retries: int = 10, retry_delay: int = 2) -> str:
    parsed_url = urllib.parse.urlparse(base_url)
    path_parts = parsed_url.path.split('/')
    pdf_name = urllib.parse.unquote(path_parts[-3])
    download_folder = './data/temp_images'

    if os.path.exists(download_folder):
        shutil.rmtree(download_folder)

    os.makedirs(download_folder, exist_ok=True)
    os.makedirs('./data/complete_pdfs', exist_ok=True)
    
    if f'{pdf_name}.pdf' in os.listdir('./data/complete_pdfs'):
        print(f'PDF already exists: {pdf_name}.pdf')
        return f'./data/complete_pdfs/{pdf_name}.pdf'

    # Extract base path
    match = re.search(r'(.*/)00000001\.jpg', base_url)
    if not match:
        print("Invalid URL format")
        return
    
    base_path = match.group(1)
    
    # First pass: Attempt to download sequentially
    image_paths = []
    current_num = 1
    consecutive_failures = 0
    total_downloaded = 0
    
    while consecutive_failures < max_retries:
        padded_num = f'{current_num:08d}'
        img_path = download_image(base_path, padded_num, download_folder)
        
        if img_path:
            compress_image_with_quality(img_path, quality=85, max_width=1200, grayscale=False)
            image_paths.append(img_path)
            consecutive_failures = 0
            current_num += 1
            total_downloaded += 1
                       
        else:
            consecutive_failures += 1
            time.sleep(retry_delay)
    
    # Sort and verify image paths
    image_paths.sort()
    
    # Second pass: Fill in any missing images
    for i in range(1, len(image_paths) + 2):
        padded_num = f'{i:08d}'
        if not any(padded_num in path for path in image_paths):
            img_path = download_image(base_path, padded_num, download_folder)
            if img_path:
                compress_image_with_quality(img_path, quality=85, max_width=1200, grayscale=False)
                image_paths.append(img_path)
                total_downloaded += 1
    
    # Sort image paths again after filling gaps
    image_paths.sort()
    
    # Convert to PDF
    if image_paths:
        make_pdf(pdf_name, image_paths, download_folder)
    
    return f'./data/complete_pdfs/{pdf_name}.pdf'
