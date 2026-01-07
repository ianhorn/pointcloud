#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/Users/ianhorn/Documents/stac-repos/pointcloud/items/laz-phase3"

cd "$WORKDIR"

for j in *.json; do
  echo "Posting $j"

  curl -X POST \
    'https://spved5ihrl.execute-api.us-west-2.amazonaws.com/collections/laz-phase3/items' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    --data-binary @"$j"
done