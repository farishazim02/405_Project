#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "usage: $0 <.R> <small_artists_file>"
    exit 0
fi

r_file=$(echo $1)
small_releases_file=$(echo $2)

Rscript "$r_file" "$small_releases_file"