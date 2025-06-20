#!/bin/bash

# Exit on error
set -e

# Create virtual environment if it doesnt exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run Flask development server
flask run
