#!/bin/bash

set -euo pipefail

# Navigate to the app directory
cd "$(dirname "$0")"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: current directory is not a git repository."
  exit 1
fi

if ! git remote get-url space >/dev/null 2>&1; then
  echo "Error: git remote 'space' is not configured."
  echo "Add it with: git remote add space https://huggingface.co/spaces/<username>/<space-name>"
  exit 1
fi

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

if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "$msg"
fi

# Push to Hugging Face
echo "Pushing to Hugging Face..."
git push space main

echo "Deployment complete!"
