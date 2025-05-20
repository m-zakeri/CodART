#!/bin/bash

# Full path to the und command
UND_CMD="/app/scitools/bin/linux64/und"

# License file paths
LICENSE_FILE="/root/.config/SciTools/License.conf"
PYTHON_API_LICENSE_FILE="/root/.local/share/SciTools/Understand/python_api.cfg"

check_license() {
    echo "Checking license validity..."
    license_output=$("${UND_CMD}" license 2>&1)

    # Check if the output contains the invalid license message
    if echo "${license_output}" | grep -q "No valid Und license found"; then
        echo "License is invalid or not found."
        return 1
    fi

    # Check if the output contains both "Reply Code :" and "Reply Date :" patterns
    if echo "${license_output}" | grep -q "Reply Code :" && echo "${license_output}" | grep -q "Reply Date :"; then
        reply_date=$(echo "${license_output}" | grep "Reply Date :" | awk -F ': ' '{print $2}')
        echo "License is valid with Reply Date: ${reply_date}"
        return 0
    else
        echo "License output format is unexpected. Will reactivate."
        return 1
    fi
}

remove_existing_license() {
    echo "Removing existing license files..."
    rm -f "${LICENSE_FILE}"
    rm -f "${PYTHON_API_LICENSE_FILE}"
    echo "License files removed."
}

# Check license and run activation if needed
if check_license; then
    echo "License is valid. Proceeding with application startup."
else
    echo "License is invalid or missing. Removing any existing license files..."
    remove_existing_license

    echo "Running license activation..."
    /app/activate_license.sh

    # Verify license files after activation
    if [ ! -f "${LICENSE_FILE}" ]; then
        echo "ERROR: License file not created properly"
        exit 1
    fi

    if [ ! -f "${PYTHON_API_LICENSE_FILE}" ]; then
        echo "ERROR: Python API license file not created properly"
        exit 1
    fi

    # Verify license is now valid
    echo "Verifying license after activation..."
    license_output=$("${UND_CMD}" license 2>&1)

    if echo "${license_output}" | grep -q "No valid Und license found"; then
        echo "ERROR: License activation failed. License is still invalid."
        echo "License output: ${license_output}"
        exit 1
    fi

    if ! (echo "${license_output}" | grep -q "Reply Code :" && echo "${license_output}" | grep -q "Reply Date :"); then
        echo "ERROR: License activation failed. Unexpected license output format."
        echo "License output: ${license_output}"
        exit 1
    fi

    echo "License activated successfully."
fi

# Start the application
cd /app
exec uvicorn application.main:app --host 0.0.0.0 --port 8000