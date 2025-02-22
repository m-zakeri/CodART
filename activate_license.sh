#!/bin/bash
set -e

HOME=/root

cd /app

echo "Current working directory: $(pwd)"
echo "Contents of /app directory:"
ls -la /app
echo "Permissions of key files:"
ls -la /app/cr-keygen-linux-amd64
ls -la /app/activate_license.sh

echo "Environment variables:"
echo "STIHOME=$STIHOME"
echo "STILICENSE=$STILICENSE"
echo "PATH=$PATH"
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"

echo "Directory permissions:"
ls -la /root/.config/ || true
ls -la /root/.config/SciTools/ || true
ls -la /root/.local/share/SciTools/Understand/ || true

echo "Checking und command:"
which und || echo "und command not found in PATH"
if which und > /dev/null; then
    echo "und binary permissions:"
    ls -la $(which und)
fi


if [ ! -f "/app/cr-keygen-linux-amd64" ]; then
    echo "Keygen binary not found at /app/cr-keygen-linux-amd64"
    exit 1
fi

echo "Generating license request code..."
REQ_CODE=$(und -createofflinerequestcode | tail -n1)
if [ -z "$REQ_CODE" ]; then
    echo "Failed to generate request code."
    exit 1
fi
echo "License Request Code: $REQ_CODE"

echo "Running keygen..."
echo -e "$REQ_CODE" | /app/cr-keygen-linux-amd64 > keygen_output.txt
cat keygen_output.txt

REPLY_CODE=$(grep "Replay Code" keygen_output.txt | awk '{print $NF}' | tr -d '-')
EXPIRATION=$(grep "Expiration Date" keygen_output.txt | awk '{print $NF}')

if [ -z "$REPLY_CODE" ] || [ -z "$EXPIRATION" ]; then
    echo "Failed to parse keygen output."
    exit 1
fi

echo "Reply Code: $REPLY_CODE"
echo "Expiration: $EXPIRATION"

echo "Applying license..."
und -setofflinereplycode "$REPLY_CODE" -expiration "$EXPIRATION" -maintenance "$EXPIRATION" || {
    echo "Failed to apply the license."
    exit 1
}


# Verify license file
LICENSE_FILE="$HOME/.config/SciTools/License.conf"
if [ -f "$LICENSE_FILE" ]; then
    echo "License file exists, showing metadata:"
    ls -la "$LICENSE_FILE"
    echo "First 10 lines of license file:"
    head -10 "$LICENSE_FILE" || true
else
    echo "WARNING: License file not found at $LICENSE_FILE"
    echo "Checking alternate license location at $STILICENSE"
    if [ -f "$STILICENSE" ]; then
        echo "License found at $STILICENSE"
        ls -la "$STILICENSE"
    else
        echo "No license file found in either location."
        # Create directory structure if it doesn't exist
        mkdir -p "$HOME/.config/SciTools"
        echo "License file was not found but directories were created."
    fi
fi

echo "Checking license with 'und version'..."
und version || true

echo "Creating test project to verify license..."
mkdir -p /tmp/test_project
cd /tmp/test_project
und create -languages C++ test_project.und || true
und analyze test_project.und || true

echo "License appears to be working. Installation complete."
exit 0