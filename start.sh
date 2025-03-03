#!/bin/bash

# Run the license activation script
/app/activate_license.sh
ACTIVATION_RESULT=$?

# Create runtime directory
mkdir -p /tmp/runtime-root
chmod 700 /tmp/runtime-root

# Set Qt environment variables for better container compatibility
export QT_OPENGL=software
export QT_GRAPHICSSYSTEM=native
export QT_NO_GLIB=1
export QT_QPA_PLATFORM=offscreen
export XDG_RUNTIME_DIR=/tmp/runtime-root

# Additional Qt fixes for mutex and threading issues
export QT_THREAD_PRIORITY_SCALE=0
export QTWEBENGINE_DISABLE_SANDBOX=1
export QSG_RENDER_LOOP=basic

# Make sure Qt destroys mutexes properly
export QT_MUTEX_WAIT_TIME=60000

# Set core dump pattern to help with debugging if needed
echo "/tmp/core.%e.%p.%t" > /proc/sys/kernel/core_pattern

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

# Increase resource limits
ulimit -c unlimited
ulimit -n 65536
ulimit -s 16384

# Start the main application with resource monitoring
echo "Starting application..."
exec uvicorn application.main:app --host 0.0.0.0 --port 8000