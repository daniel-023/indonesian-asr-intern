#!/bin/bash

in_dir=${1%/}
# Define the number of files per subfolder
FILES_PER_SUBFOLDER=in_dir=$2

# Define the prefix for subfolder names
SUBFOLDER_PREFIX="batch_"

# Initialize a counter for files processed
i=0

# Initialize a counter for subfolders
subfolder_num=1

# Loop through all files in the current directory
for f in "${in_dir}"/*.webm; do
    # Check if the current item is a file
    if [[ -f "$f" ]]; then
        # Create the subfolder if it doesn't exist
        mkdir -p "${SUBFOLDER_PREFIX}$(printf %03d "$subfolder_num")"

        # Move the file to the current subfolder
        mv -- "$f" "${SUBFOLDER_PREFIX}$(printf %03d "$subfolder_num")/"

        # Increment the file counter
        ((i++))

        # If the file counter reaches the limit, reset it and increment the subfolder counter
        if (( i % FILES_PER_SUBFOLDER == 0 )); then
            ((subfolder_num++))
        fi
    fi
done