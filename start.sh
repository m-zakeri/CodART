#!/bin/bash
/app/activate_license.sh && uvicorn application.main:app --host 0.0.0.0 --port 8000
