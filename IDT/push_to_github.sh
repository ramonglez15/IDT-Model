#!/bin/bash

# Script to push the class_public repository to a new GitHub repository
# Created for user: ramonglez15
# Repository name: IDT

echo "This script will help you push your local class_public repository to your GitHub account."
echo "Before running this script, please make sure you have:"
echo "1. Created a new repository named 'IDT' on your GitHub account (ramonglez15)"
echo "2. The repository should be empty (no README, no .gitignore, etc.)"
echo ""
echo "Have you created the repository on GitHub? (y/n)"
read -r answer

if [[ "$answer" != "y" ]]; then
  echo "Please create the repository first at: https://github.com/new"
  echo "Repository name: IDT"
  echo "Make it public or private as you prefer"
  echo "Do NOT initialize it with a README, .gitignore, or license"
  echo "Then run this script again."
  exit 1
fi

# Change directory to class_public
cd "$(dirname "$0")/class_public" || {
  echo "Error: Could not change to class_public directory"
  exit 1
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Error: The class_public directory is not a git repository"
  exit 1
fi

# Change the remote URL
echo "Changing remote URL to your GitHub repository..."
git remote set-url origin "https://github.com/ramonglez15/IDT.git"

# Verify the remote URL
echo "New remote URL:"
git remote -v

echo ""
echo "Ready to push to GitHub. You will be prompted for your GitHub username and password."
echo "Note: For the password, you might need to use a personal access token instead of your regular password."
echo "See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel"
read -r

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin master

if [ $? -eq 0 ]; then
  echo "Success! Your repository has been pushed to GitHub."
  echo "You can view it at: https://github.com/ramonglez15/IDT"
else
  echo "There was an error pushing to GitHub."
  echo "Please check your credentials and try again."
fi
