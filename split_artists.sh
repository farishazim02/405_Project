#!/bin/bash

split_artists=10
file="/staging/groups/stat_dscp/group05/discogs_20250401_artists.csv"

split -d -n l/$split_artists --additional-suffix=.csv $file "small_artists"

tail -n +2 small_artists00.csv > temp.csv
cat temp.csv > small_artists00.csv

# Create input_files for ".sub" file's "queue file from input_files" line
ls -1 small_artists0{0..9}.csv > input_artists

rm -f temp.csv