#!/usr/bin/env bash

python3 -m venv __venv

source __venv/bin/activate

pip3 install --upgrade -r requirements.txt

python3 utils/getAudioFileInfo.py $1

deactivate
