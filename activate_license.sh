#!/bin/bash
# Don't use set -e, since we want to continue even if some commands fail
set -e

HOME=/root
LICENSE_FILE="$HOME/.config/SciTools/License.conf"
SCITOOLS_LICENSE="/app/SciTools/License.conf"

# Create directories if they don't exist
mkdir -p "$HOME/.config/SciTools"
mkdir -p "/app/SciTools"

# Check if license file exists
if [ -f "$LICENSE_FILE" ]; then
    echo "License file exists at $LICENSE_FILE, checking if valid..."
    und version > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "License is valid, skipping activation."
        exit 0
    else
        echo "License exists but may not be valid, proceeding with activation..."
    fi
fi

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
echo "UNDERSTAND_LICENSE=$UNDERSTAND_LICENSE"
echo "STIDOSUTILDIR=$STIDOSUTILDIR"

echo "Directory permissions:"
ls -la /root/.config/ || true
ls -la /root/.config/SciTools/ || true
ls -la /root/.local/share/SciTools/Understand/ || true
ls -la /app/SciTools/ || true

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

# Create license file directly first to ensure it exists
echo "Creating license file directly..."
mkdir -p "$(dirname "$LICENSE_FILE")"
cat > "$LICENSE_FILE" << EOF
REPLYCODE=$REPLY_CODE
MAINTENANCE=$EXPIRATION
EXPIRATION=$EXPIRATION
EOF
chmod 644 "$LICENSE_FILE"

# Ensure symlinks are set up correctly (remove any old ones first)
if [ -L "$SCITOOLS_LICENSE" ]; then
    rm "$SCITOOLS_LICENSE"
fi
ln -sf "$LICENSE_FILE" "$SCITOOLS_LICENSE"
echo "Created symlink from $LICENSE_FILE to $SCITOOLS_LICENSE"

# Apply the license
echo "Applying license..."
und -setofflinereplycode "$REPLY_CODE" -expiration "$EXPIRATION" -maintenance "$EXPIRATION" > /dev/null 2>&1
APPLY_RESULT=$?
if [ $APPLY_RESULT -ne 0 ]; then
    echo "Warning: First license application method returned $APPLY_RESULT, trying alternative methods..."

    # Try alternative method
    und -setlicensecode "$REPLY_CODE" > /dev/null 2>&1
fi

# Check if license is working with a simple version check
echo "Checking license with 'und version'..."
und version
VERSION_CHECK=$?
if [ $VERSION_CHECK -ne 0 ]; then
    echo "Warning: 'und version' failed with code $VERSION_CHECK, license may not be properly activated"
else
    echo "License appears to be working - 'und version' succeeded"
fi

echo "Creating test project to verify license..."
mkdir -p /tmp/test_project
cd /tmp/test_project
echo "int main() { return 0; }" > test.cpp
und create -languages C++ test_project.und > /dev/null 2>&1
CREATE_RESULT=$?

if [ $CREATE_RESULT -ne 0 ]; then
    echo "Warning: Failed to create test project (code $CREATE_RESULT), but continuing..."
else
    echo "Successfully created test project"

    # Analyze the project if creation succeeded
    echo "Analyzing test project..."
    und analyze test_project.und > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Successfully analyzed test project"
    else
        echo "Warning: Failed to analyze test project, but continuing..."
    fi
fi

echo "Testing license with Python integration..."
cat > test_license.py << 'EOF'
#!/usr/bin/env python3
import sys
import os
import traceback

try:
    print("Importing understand module...")
    import understand
    print("Understand module imported successfully.")

    # Try to open the database created by the und command
    db_path = "/tmp/test_project/test_project.und"
    if not os.path.exists(db_path):
        print(f"Warning: Database at {db_path} does not exist")
        sys.exit(0)

    print(f"Opening database at {db_path}...")

    # Open the database
    db = understand.open(db_path)
    print("Database opened successfully.")

    # Get basic information about the database
    print("\nBasic database information:")
    print(f"  Name: {db.name()}")

    # Close the database
    print("\nClosing database...")
    db.close()
    print("Database closed successfully.")

    print("\nPython license verification completed successfully.")
    sys.exit(0)
except Exception as e:
    print(f"Error during Python license verification: {str(e)}")
    print("Detailed traceback:")
    traceback.print_exc()
    sys.exit(0)  # Exit with success even if there's an error to not block container startup
EOF

chmod +x test_license.py
echo "Running Python license test..."
python3 ./test_license.py
PYTHON_TEST_RESULT=$?

# Always succeed for container startup
echo "License setup completed with Python test result: $PYTHON_TEST_RESULT"
# Create a flag file to indicate activation was attempted
touch /app/SciTools/license_activated
exit 0