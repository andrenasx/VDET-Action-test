#!/bin/bash

cd ${{ github.action_path }}

ls

pip install -r ./requirements.txt

python ./src/detector.py
