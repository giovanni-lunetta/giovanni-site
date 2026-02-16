#!/bin/bash

# Define paths (text-based resume after PDF-to-text conversion)
SOURCE="my_app/me/resume.txt"
DEST="assets/resume.txt"

# Check if source exists
if [ -f "$SOURCE" ]; then
    echo "Syncing resume from $SOURCE to $DEST..."
    cp "$SOURCE" "$DEST"
    echo "Done!"
else
    echo "Error: Source resume not found at $SOURCE"
    exit 1
fi
