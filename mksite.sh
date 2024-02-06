#!/bin/bash

echo Creating virtual environment...
python3 -m venv  _venv/

echo Entering virtual environment...
source _venv/bin/activate

echo Installing dependencies in virtual environment...
pip3 install -q --upgrade pip
pip3 install -q -r requirements.txt

echo Running site generator...
python3 mksite.py

echo Leaving virtual environment...
deactivate

echo Cleaning up...
rm -rf _venv/
rm -rf __pycache__/

echo
echo Done.

exit 0
