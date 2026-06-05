#!/usr/bin/env bash

python3 -m venv __venv

source __venv\Scripts\activate

pip3 install --upgrade -r requirements.txt

python3 mksite.py

deactivate