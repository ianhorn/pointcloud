import concurrent.futures
import os

import pandas as pd
from pystac import Item

from stactools.pointcloud.stac import create_item

# Input CSV and output directory
csv = "/Users/ianhorn/Documents/stac-repos/pointcloud/csv/laz-phase1.csv"
output_dir = "/Users/ianhorn/Documents/stac-repos/pointcloud/items/laz-phase1"

# Load the CSV
df = pd.read_csv(csv)

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)


# Define the function to create and save a STAC item
def create_laz_item(row):
    url = row["aws_url"]  # Make sure your CSV has a column named 'url'
    try:
        item: Item = create_item(url)
        item_path = os.path.join(output_dir, f"{item.id}.json")
        item.save_object(dest_href=item_path)
        print(f"Saved: {item.id}")
        return item.id
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


# Use ThreadPoolExecutor to parallelize the item creation
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(create_laz_item, row) for _, row in df.iterrows()]
    for future in concurrent.futures.as_completed(futures):
        future.result()
