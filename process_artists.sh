#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <small_artists_file>"
    exit 0
fi

small_artists_file=$(echo $1)

Rscript process_artists.R "$small_artists_file"