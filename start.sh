#!/bin/bash

# Run the license activation script
/app/activate_license.sh
ACTIVATION_RESULT=$?

# Check if activation was successful
if [ $ACTIVATION_RESULT -ne 0 ]; then
    echo "WARNING: License activation script exited with code $ACTIVATION_RESULT"
    # Continue anyway, as it might still work
fi

# Check if the license file exists
if [ ! -f "/app/SciTools/License.conf" ] && [ ! -f "/root/.config/SciTools/License.conf" ]; then
    echo "ERROR: No license file found. Creating empty license file to try to continue..."
    mkdir -p /root/.config/SciTools
    touch /root/.config/SciTools/License.conf
    mkdir -p /app/SciTools
    ln -sf /root/.config/SciTools/License.conf /app/SciTools/License.conf
fi

# Start the main application
echo "Starting application..."
uvicorn application.main:app --host 0.0.0.0 --port 8000