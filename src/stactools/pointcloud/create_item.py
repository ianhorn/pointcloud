"""
Ian Horn
11 July 2011

Script: Create stac items using stactools-pointcloud python package. 
"""
import os
import json

import requests

from stactools.pointcloud.stac import create_item
import stactools.core

url = 'https://kyfromabove.s3.us-west-2.amazonaws.com/elevation/PointCloud/Phase1/N017E292.laz'
item = create_item(url)
print(item.to_dict())

with open('item.json', 'w') as f:
    json.dump(item.to_dict(), f, indent=2)
print("STAC item saved to item.json")









# url = 'https://kyfromabove.s3.us-west-2.amazonaws.com/elevation/PointCloud/Phase1/N017E292.laz'
# phase = 'laz-phase1'
# csv = 'f./csv/{phase}'
# api = 'https://spved5ihrl.execute-api.us-west-2.amazonaws.com/'
# item_output = f'items/{phase}'


