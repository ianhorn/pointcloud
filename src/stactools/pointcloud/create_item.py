import os
import json
import pandas as pd
import concurrent.futures
from stactools.pointcloud.stac import create_item
from tqdm import tqdm

# Set paths for your machine
csv_path = "C:/Users/ian.horn/Documents/stac-repos/pointcloud/csv/laz-phase2.csv"
out_dir = "C:/Users/ian.horn/Documents/stac-repos/pointcloud/items/laz-phase2"

# Ensure output directory exists
os.makedirs(out_dir, exist_ok=True)

# Load paths from CSV
df = pd.read_csv(csv_path)
paths = df['aws_url'].dropna().tolist()  # Use 'aws_url' column

# Safe wrapper for item creation
def safe_create_item(las_path):
    try:
        print(f"Processing: {las_path}")  # helpful if freezing
        item = create_item(las_path)
        out_path = os.path.join(out_dir, f"{item.id}.json")
        with open(out_path, "w") as f:
            f.write(json.dumps(item.to_dict(), indent=2))
        return {"success": True, "id": item.id}
    except Exception as e:
        return {"success": False, "path": las_path, "error": str(e)}

# Run in parallel with processes
results = []
with concurrent.futures.ProcessPoolExecutor() as executor:
    for result in tqdm(executor.map(safe_create_item, paths), total=len(paths)):
        results.append(result)

# Summarize results
successes = [r for r in results if r['success']]
failures = [r for r in results if not r['success']]

print(f"\n✅ Created {len(successes)} items")
print(f"❌ Failed on {len(failures)} items")
if failures:
    print("\nSome failures:")
    for fail in failures[:5]:  # show only first 5
        print(f" - {fail['path']}: {fail['error']}")