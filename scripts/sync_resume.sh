#!/bin/bash

# Define paths
SOURCE="my_app/me/resume.pdf"
DEST="assets/resume.pdf"

# Check if source exists
if [ -f "$SOURCE" ]; then
    echo "Syncing resume from $SOURCE to $DEST..."
    cp "$SOURCE" "$DEST"
    echo "Done!"
else
    echo "Error: Source resume not found at $SOURCE"
    exit 1
fi
