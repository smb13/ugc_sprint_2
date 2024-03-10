#!/bin/bash

# Check if there are two command line arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <ssh-private-key> <repository-url>"
    exit 1
fi

# Assign command line arguments to variables
SSH_PRIVATE_KEY_CONTENT="$1"
REPO_URL="$2"
SSH_DIR="$HOME/.ssh"
REPO_DIR="$HOME/src"

# Add the SSH private key to the specified file
echo "$SSH_PRIVATE_KEY_CONTENT" > "$SSH_DIR/id_ed25519"
chmod 600 "$SSH_DIR/id_ed25519"

# Start the ssh-agent in the background and add the private key
eval "$(ssh-agent -s)"
ssh-add "$SSH_DIR/id_ed25519"

# Clone the repository to the desired directory
git clone "$REPO_URL" "$REPO_DIR"
