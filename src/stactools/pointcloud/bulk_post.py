import os
import requests
import json
from concurrent.futures import ProcessPoolExecutor

product = 'laz'
phase = 'phase2'
folder_path = f'C:/Users/Ian.Horn/Documents/stac-repos/pointcloud/items/{product}-{phase}'
api = 'https://spved5ihrl.execute-api.us-west-2.amazonaws.com/'
post_url = f'{api}collections/{product}-{phase}/items'

def post_item(item_path):
    try:
        with open(item_path, 'r', encoding='utf-8') as f:
            item_data = json.load(f)

        response = requests.post(
            post_url,
            headers={'Content-Type': 'application/geo+json'},
            json=item_data
        )

        print(f"{os.path.basename(item_path)} -> {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error posting {item_path}: {e}")
        return None

if __name__ == "__main__":
    # Collect all full paths to the items
    item_paths = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    with ProcessPoolExecutor(max_workers=18) as executor:
        results = list(executor.map(post_item, item_paths))