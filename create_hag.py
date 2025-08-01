"""
This script will create a function to process a COPC LAZ file for
Height Above Ground Value (HAG).  This is the basis for creating
phase2 elevation DSM, except values with be HAG and not elevation,
eliminating the need to perform DHSM = DSM-DEM.

Date:  July 31 2025,
Author: Ian Horn
"""

import os
import json
import pdal
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(
    filename='failed_hag_files.log',
    filemode='a',  # append mode
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

source_dir = 'J:/pointcloud/project/laz-phase2'
file_paths = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith(".laz")]
dest_dir = 'T:/Elevation/TEMP_LAS_HAG_Phase2'


def create_hag_file(source_laz):
    copc = source_laz
    basename = os.path.basename(copc).replace('LAS_Phase2.copc.laz', 'HAG_Phase2.tif')
    dest_hag_tif = os.path.join(dest_dir, basename)

    if os.path.exists(dest_hag_tif):
        print(f'{os.path.basename(dest_hag_tif)} already exists, skipping')
        return None,
    else:
        json_pipe = [
            {
                "type": "readers.copc",  # read the file
                "filename": source_laz
            },
            {
                "type": "filters.expression",
                "expression": "ReturnNumber == 1 || NumberOfReturns == 1"  # grabs all first returns, import to use "Or"
            },
            {
                "type": "filters.hag_delaunay",  # Height Above Ground step
                "allow_extrapolation": True
            },
            {
                "type": "filters.ferry",  # Ferries, or takes the calculated HAG values with through the pipeline.
                "dimensions": "HeightAboveGround=>Z"
            },
            {
                "type":  "writers.gdal",
                "filename":  dest_hag_tif,
                "resolution":  2,
                "output_type":  "max",
                "nodata": -999999,
                "gdalopts":  [
                    "COMPRESS=LZW",
                    "TILED=YES",
                    "BLOCKXSIZE=256",
                    "BLOCKYSIZE=256"
                ]
            }
        ]

        pipeline = pdal.Pipeline(json.dumps(json_pipe))
        try:
            pipeline.execute()
            return dest_hag_tif
        except RuntimeError as e:
            logging.error(f"Failed to process {source_laz}: {e}")
            return None

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # optional but good for Windows

    # You can also add tqdm here if you like
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(create_hag_file, path) for path in file_paths]

        for future in as_completed(futures):
            try:
                result = future.result()
                print(f"Finished: {result}")
            except Exception as e:
                print(f"Error: {e}")
