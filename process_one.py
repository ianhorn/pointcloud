# process_one.py
import os
import json
import sys
from stactools.pointcloud.stac import create_item

url = sys.argv[1]
out_dir = sys.argv[2]

fname = os.path.basename(url)
json_name = os.path.splitext(fname)[0] + ".json"
outfile = os.path.join(out_dir, json_name)

if os.path.exists(outfile):
    print(f" Skipping {json_name}")
    sys.exit(0)

item = create_item(url)
with open(outfile, 'w', encoding='utf-8') as f:
    json.dump(item.to_dict(), f, indent=2)
print(f"✔ {item.id}")