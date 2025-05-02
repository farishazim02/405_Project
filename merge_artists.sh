#!/bin/bash

for file in sorted_small_artists*.csv; do
    tail -n +2 -q $file > temp_$file
done

echo $(head -n 1 sorted_small_artists01.csv) | cat - temp_*.csv > artists.csv

rm -f temp_*.csv small_artists*.csv sorted_small_artists*.csv