#!/bin/bash

# Get the latest snapshot of Discogs data (April 2025)

all_csvs=(
  "discogs_20250401_masters.csv"
  "discogs_20250401_releases.csv"
  "discogs_20250401_artists.csv"
)


if [[ ! -f "Discogs.tar" ]]; then
  echo "Discogs.tar not found, downloading…"
  wget https://uwmadison.box.com/shared/static/0udwxbzd1nmu6heal7qmzyz9rwn412ps.tar
else
  echo "Discogs.tar already exists, skipping download."
fi


for csv in "${all_csvs[@]}"; do
  if [[ ! -f $csv ]]; then
    echo "Extracting $csv..."
    tar -xvf Discogs.tar $csv
  else
    echo "$csv already exists, skipping extraction."
  fi
done
