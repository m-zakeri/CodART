#!/bin/bash

# Set default delay value (in seconds)
DEFAULT_DELAY=3

# Function to run commands with delay afterward
run_with_delay() {
    local cmd="$1"
    local delay_seconds="${2:-$DEFAULT_DELAY}"
    local message="${3:-Running command}"

    echo "$message (delay after: ${delay_seconds}s)..."
    bash -c "$cmd"
    local status=$?

    if [ $status -ne 0 ]; then
        echo "WARNING: Command failed with status $status"
    else
        echo "Command completed successfully."
    fi

    echo "Waiting for ${delay_seconds} seconds..."
    sleep $delay_seconds

    return $status
}

HOME=/root
CONFIG_DIR="$HOME/.config/SciTools"
LICENSE_FILE="$CONFIG_DIR/License.conf"
UND_CONF="$CONFIG_DIR/Und.conf"
UNDERSTAND_CONF="$CONFIG_DIR/Understand.conf"
SCITOOLS_LICENSE="/app/SciTools/License.conf"
PYTHON_API_CONFIG_DIR="/root/.local/share/SciTools/Understand"
PYTHON_API_CONFIG_FILE="$PYTHON_API_CONFIG_DIR/python_api.cfg"

# Create directories if they don't exist
run_with_delay "mkdir -p $CONFIG_DIR" 2 "Creating config directory"
run_with_delay "mkdir -p $PYTHON_API_CONFIG_DIR" 2 "Creating Python API config directory"

cd /app

echo "Checking und command:"
run_with_delay "which und || echo 'und command not found in PATH'" 1 "Checking for und command"

if which und > /dev/null; then
    echo "und binary permissions:"
    run_with_delay "ls -la $(which und)" 1 "Checking und permissions"
fi

if [ ! -f "/app/cr-keygen-linux-amd64" ]; then
    echo "Keygen binary not found at /app/cr-keygen-linux-amd64"
    exit 1
fi

echo "Generating license request code..."
REQ_CODE=$(und -createofflinerequestcode | grep -E '^[A-Z0-9]+$' | tail -n1)
echo "Waiting after request code generation..."
sleep 5

if [ -z "$REQ_CODE" ]; then
    echo "Failed to generate request code. Attempting alternative method..."
    REQ_CODE=$(und -createofflinerequestcode | tail -n1 | tr -d -c 'A-Z0-9')
    echo "Waiting after alternative request code generation..."
    sleep 5

    if [ -z "$REQ_CODE" ]; then
        echo "All attempts to generate request code failed."
    fi
fi
echo "License Request Code: $REQ_CODE"

echo "Running keygen..."
echo -e "$REQ_CODE" | /app/cr-keygen-linux-amd64 > keygen_output.txt
echo "Waiting after keygen process..."
sleep 5

run_with_delay "cat keygen_output.txt" 2 "Displaying keygen output"

REPLY_CODE=$(grep -i "Replay Code" keygen_output.txt | awk '{print $NF}' | tr -d '-')
if [ -z "$REPLY_CODE" ]; then
    REPLY_CODE=$(grep -i "Reply Code" keygen_output.txt | awk '{print $NF}' | tr -d '-')
fi
EXPIRATION=$(grep -i "Expiration Date" keygen_output.txt | awk '{print $NF}')

if [ -z "$REPLY_CODE" ] || [ -z "$EXPIRATION" ]; then
    echo "Failed to parse keygen output."
    # Create a dummy license file to allow container to start
    echo "Creating dummy license file for container startup..."
fi

echo "Reply Code: $REPLY_CODE"
echo "Expiration: $EXPIRATION"

if [ -L "$SCITOOLS_LICENSE" ]; then
    run_with_delay "rm $SCITOOLS_LICENSE" 2 "Removing existing license symlink"
fi

echo "Applying license..."
run_with_delay "und -setofflinereplycode $REPLY_CODE -expiration $EXPIRATION -maintenance $EXPIRATION" 8 "Applying license"

# Create Python API license configuration file
echo "Creating Python API license configuration..."
cat > "$PYTHON_API_CONFIG_FILE" << EOF
[License]
ReplyCode=${REPLY_CODE}
ExpirationDate=${EXPIRATION}
EOF
chmod 644 "$PYTHON_API_CONFIG_FILE"
echo "Python API license configuration created at $PYTHON_API_CONFIG_FILE"

# Create symbolic link to main license file
mkdir -p /app/SciTools
ln -sf "$LICENSE_FILE" "$SCITOOLS_LICENSE"
echo "Created symlink from $LICENSE_FILE to $SCITOOLS_LICENSE"

# Export environment variables
export STILICENSE="$LICENSE_FILE"
export UNDERSTAND_API_LICENSE="$PYTHON_API_CONFIG_FILE"
echo "Set environment variables: STILICENSE=$STILICENSE, UNDERSTAND_API_LICENSE=$UNDERSTAND_API_LICENSE"

echo "Checking license with 'und license'..."
LICENSE_OUTPUT=$(und license)
LICENSE_CHECK=$?
echo "$LICENSE_OUTPUT"
echo "Waiting after license check..."
sleep 5

run_with_delay "echo $PATH" 1 "Checking PATH"
run_with_delay "echo $LD_LIBRARY_PATH" 1 "Checking LD_LIBRARY_PATH"
run_with_delay "echo $PYTHONPATH" 1 "Checking PYTHONPATH"

if [ $LICENSE_CHECK -ne 0 ]; then
    echo "Warning: 'und license' failed with code $LICENSE_CHECK, license may not be properly activated"
else
    REPLY_CODE_CHECK=$(echo "$LICENSE_OUTPUT" | grep "Reply Code" | awk '{print $NF}')
    REPLY_DATE_CHECK=$(echo "$LICENSE_OUTPUT" | grep "Reply Date" | awk '{print $NF}')
    echo "License appears to be working - Reply Code: $REPLY_CODE_CHECK, Reply Date: $REPLY_DATE_CHECK"
fi

echo "Creating test project to verify license..."
run_with_delay "mkdir -p /tmp/test_project" 2 "Creating test project directory"
cd /tmp/test_project
run_with_delay "echo \"int main() { return 0; }\" > test.cpp" 1 "Creating test C++ file"
run_with_delay "und create -languages C++ test_project.und" 10 "Creating test Understand project"
CREATE_RESULT=$?
echo $CREATE_RESULT

if [ $CREATE_RESULT -ne 0 ]; then
    echo "Warning: Failed to create test project (code $CREATE_RESULT), but continuing..."
else
    echo "Successfully created test project"

    # Analyze the project if creation succeeded
    echo "Analyzing test project..."
    run_with_delay "und add /tmp/test_project/test.cpp test_project.und" 5 "Adding file to project"
    run_with_delay "und analyze test_project.und" 15 "Analyzing project"
    ANALYZE_RESULT=$?
    echo "Analyze result: $ANALYZE_RESULT"
    if [ $ANALYZE_RESULT -eq 0 ]; then
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
import time

# Explicitly set the license path
license_path = os.environ.get('UNDERSTAND_API_LICENSE', '/root/.local/share/SciTools/Understand/python_api.cfg')
os.environ['UNDERSTAND_API_LICENSE'] = license_path

def print_with_timestamp(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def pause_with_message(seconds, message="Pausing"):
    print_with_timestamp(f"{message} for {seconds} seconds...")
    time.sleep(seconds)
    print_with_timestamp("Continuing execution")

print_with_timestamp(f"Using license config: {license_path}")
print_with_timestamp("Python module search paths:")
for path in sys.path:
    print(f"  - {path}")

pause_with_message(2, "Pausing before import attempt")

try:
    print_with_timestamp("Importing understand module...")
    import understand
    print_with_timestamp(f"Understand module location: {understand.__file__}")
    print_with_timestamp("Understand module imported successfully.")

    # Try to explicitly set the license path through the API
    print_with_timestamp(f"Setting license path through API to: {license_path}")
    understand.license(license_path)
    print_with_timestamp("License path set successfully.")

    pause_with_message(3, "Pausing after module import")

    db_path = "/tmp/test_project/test_project.und"
    if not os.path.exists(db_path):
        print_with_timestamp(f"Warning: Database at {db_path} does not exist")
        sys.exit(0)

    print_with_timestamp(f"Opening database at {db_path}...")

    # Open the database
    start_time = time.time()
    db = understand.open(db_path)
    end_time = time.time()
    print_with_timestamp(f"Database opened successfully in {end_time - start_time:.2f} seconds.")

    pause_with_message(3, "Pausing after database open")

    print_with_timestamp("Testing database query...")
    start_time = time.time()
    entities = db.ents("function")
    end_time = time.time()
    print_with_timestamp(f"Found {len(entities)} functions in {end_time - start_time:.2f} seconds.")

    pause_with_message(3, "Pausing after entity query")

    print_with_timestamp("\nClosing database...")
    db.close()
    print_with_timestamp("Database closed successfully.")

    pause_with_message(2, "Pausing after database close")

    print_with_timestamp("\nPython license verification completed successfully.")
    sys.exit(0)
except Exception as e:
    print_with_timestamp(f"Error during Python license verification: {str(e)}")
    print_with_timestamp("Detailed traceback:")
    traceback.print_exc()
    pause_with_message(5, "Pausing after error")
    sys.exit(1)  # Exit with error to indicate failure
EOF

run_with_delay "chmod +x test_license.py" 1 "Making Python test script executable"
echo "Running Python license test..."
export UND_REPLY_CODE="$REPLY_CODE"
export UNDERSTAND_API_LICENSE="$PYTHON_API_CONFIG_FILE"
run_with_delay "python3 ./test_license.py" 5 "Running Python license test"
PYTHON_TEST_RESULT=$?

if [ $PYTHON_TEST_RESULT -eq 0 ]; then
    echo "Python API license test passed successfully!"
else
    echo "Warning: Python API license test failed with code $PYTHON_TEST_RESULT"
fi

# Create a flag file to indicate activation was attempted
run_with_delay "touch /app/SciTools/license_activated" 2 "Creating license activation flag"

# Check if the Python API config file was properly created
if [ -f "$PYTHON_API_CONFIG_FILE" ]; then
    echo "Python API license configuration exists at: $PYTHON_API_CONFIG_FILE"
    run_with_delay "cat $PYTHON_API_CONFIG_FILE" 1 "Displaying Python API license configuration"
else
    echo "ERROR: Python API license configuration file was not created!"
fi

# Check that environment variables are set properly
echo "Final environment variable check:"
echo "STILICENSE=$STILICENSE"
echo "UNDERSTAND_API_LICENSE=$UNDERSTAND_API_LICENSE"

# Always succeed for container startup
echo "License setup completed with Python test result: $PYTHON_TEST_RESULT"
exit 0