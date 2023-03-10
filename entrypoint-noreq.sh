#!/bin/sh -l

python -m pip install --upgrade pip

# Working directory
cd /vdet

# Install dependencies
pip install -r requirements.txt

# Run the detector
python src/analyse.py "$1" "$2"

mv results.sarif /github/workspace
