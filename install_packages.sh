#!/bin/bash

set -x

PREV_CREDENTIAL=$HOME"/.credentials/client_secret.json"
rm -rf $PREV_CREDENTIAL

sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python-pip python-dev build-essential
pip install --upgrade pip
pip install --upgrade virtualenv

brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install Cython==0.26.1
pip install kivy
pip install https://github.com/kivy/kivy/archive/master.zip

pip install bs4

pip install --upgrade google-api-python-client

pip install oauth2client

pip install arrow
