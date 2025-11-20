#!/bin/bash

# Navigate to the app directory
cd "$(dirname "$0")"

# Add all changes
git add .

# Commit changes (prompt for message or use default)
if [ -z "$1" ]; then
  read -p "Enter commit message: " msg
else
  msg="$1"
fi

if [ -z "$msg" ]; then
  msg="Update app"
fi

git commit -m "$msg"

# Push to Hugging Face
echo "Pushing to Hugging Face..."
git push space main

echo "Deployment complete!"
