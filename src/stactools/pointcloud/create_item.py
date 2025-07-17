"""
Ian Horn
11 July 2011

Script: Create STAC items using stactools-pointcloud python package.
"""

import os
import json
import pandas as pd
import concurrent.futures

from stactools.pointcloud.stac import create_item

# Configuration
file_format = "laz"
phase = "phase3"

csv_path = f'csv/{file_format}-{phase}.csv'
out_dir = f'items/{file_format}-{phase}'

os.makedirs(out_dir, exist_ok=True)

# Read CSV of URLs
df = pd.read_csv(csv_path)

def create_laz_item(url):
    fname = os.path.basename(url)
    json_name = os.path.splitext(fname)[0] + ".json"
    outfile = os.path.join(out_dir, json_name)

    try:
        # Only create the item if it doesn't exist already
        if not os.path.exists(outfile):
            item = create_item(url)
            print(f'Item {item.id} created')

            with open(outfile, 'w') as f:
                json.dump(item.to_dict(), f, indent=2)
            print(f'STAC Item saved to {outfile}')
        else:
            print(f'Skipping {outfile}, already exists.')

    except Exception as e:
        print(f"Error processing {url}: {e}")

def main():
    urls = df['url'].tolist()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_laz_item, urls)

if __name__ == "__main__":
    main()