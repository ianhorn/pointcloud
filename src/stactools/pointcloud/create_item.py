import os
import json
import pandas as pd
import concurrent.futures
from stactools.pointcloud.stac import create_item
from tqdm import tqdm

file_format = "laz"
phase = "phase2"

csv_path = f'C:/Users/Ian.Horn/Documents/stac-repos/pointcloud/csv/{file_format}-{phase}.csv'
out_dir = f'C:/Users/Ian.Horn/Documents/stac-repos/pointcloud/items/{file_format}-{phase}'
os.makedirs(out_dir, exist_ok=True)

df = pd.read_csv(csv_path)


def create_laz_item(url):
    fname = os.path.basename(url)
    json_name = os.path.splitext(fname)[0] + ".json"
    outfile = os.path.join(out_dir, json_name)

    try:
        if not os.path.exists(outfile):
            item = create_item(url)
            with open(outfile, 'w') as f:
                json.dump(item.to_dict(), f, indent=2)
            print(f"✔ {item.id}")
        else:
            print(f"⏩ Skipping {json_name}")
    except Exception as e:
        print(f"❌ Error for {url}: {e}")


def main():
    urls = df['aws_url'].tolist()
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        list(tqdm(executor.map(create_laz_item, urls), total=len(urls)))


if __name__ == "__main__":
    main()