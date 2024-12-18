import json
import requests
import os
from urllib.parse import urlparse



def sanitize_filename(filename):
    filename = os.path.basename(filename)
    return filename.replace('/', ' ').strip()


def download(json_filepath, download_path):
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    pdf_links =[link for link in data.values()]
    for link in pdf_links:
        response = requests.get(link, stream=True)
        response.raise_for_status()
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            file_name = content_disposition.split('filename=')[1].strip(' "')

        else:
            parsed_url = urlparse(link)
            file_name = os.path.basename(parsed_url.path)
        file_name = sanitize_filename(file_name)
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'wb') as r:
            for chunk in response.iter_content(chunk_size=1024):
                r.write(chunk)

        print(f'Download {file_name}')


jsonFilePath = 'Dataset.json'
downloadPath = 'database'
download(jsonFilePath,downloadPath)