#!/bin/bash

/app/activate_license.sh

# Verify license files
if [ ! -f "/root/.config/SciTools/License.conf" ]; then
    echo "ERROR: License file not created properly"
    exit 1
fi

if [ ! -f "/root/.local/share/SciTools/Understand/python_api.cfg" ]; then
    echo "ERROR: Python API license file not created properly"
    exit 1
fi

# Test the license
und license
if [ $? -ne 0 ]; then
    echo "LICENSE ERROR: License validation failed"
    # Don't exit to allow container to start anyway
fi

# Create a dummy project to verify license
echo "Testing license with a simple project..."
mkdir -p /tmp/test
cd /tmp/test
echo "public class Test { public static void main(String[] args) { } }" > Test.java
und create -languages java test.und
if [ $? -ne 0 ]; then
    echo "WARNING: Could not create test project, license may not be working"
else
    echo "License appears to be working correctly!"
fi

# Start the application
echo "Starting application..."
exec uvicorn application.main:app --host 0.0.0.0 --port 8000