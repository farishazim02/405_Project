#!/bin/bash

for file in survival_small_releases_*.csv; do
    tail -n +2 -q $file > temp_$file
done

head -n 1 survival_small_releases_000.csv > survival_releases.csv
 
#sort -t ',' -m -k 2,2n 
cat temp_*.csv >> survival_releases.csv

rm -f temp_*.csv