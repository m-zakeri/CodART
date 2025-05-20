#!/bin/bash

# Generate license request code
REQ_CODE=$(und -createofflinerequestcode | grep -E '^[A-Z0-9]+$' | tail -n1)
if [ -z "$REQ_CODE" ]; then
    REQ_CODE=$(und -createofflinerequestcode | tail -n1 | tr -d -c 'A-Z0-9')
    if [ -z "$REQ_CODE" ]; then
        echo "Failed to generate request code."
        exit 1
    fi
fi
echo "License Request Code: $REQ_CODE"

# Run keygen
echo -e "$REQ_CODE" | /app/cr-keygen-linux-amd64 > keygen_output.txt

# Extract license details
REPLY_CODE=$(grep -i "Reply Code\|Replay Code" keygen_output.txt | awk '{print $NF}' | tr -d '-')
EXPIRATION=$(grep -i "Expiration Date" keygen_output.txt | awk '{print $NF}')

if [ -z "$REPLY_CODE" ] || [ -z "$EXPIRATION" ]; then
    echo "Failed to parse keygen output."
    exit 1
fi

echo "Reply Code: $REPLY_CODE"
echo "Expiration: $EXPIRATION"

# Apply license - this should create the necessary directories and files
und -setofflinereplycode $REPLY_CODE -expiration $EXPIRATION -maintenance $EXPIRATION

# Create symbolic link if needed
if [ -f "/root/.config/SciTools/License.conf" ]; then
    mkdir -p /app/SciTools
    ln -sf "/root/.config/SciTools/License.conf" "/app/SciTools/License.conf"
fi

echo "License setup completed."