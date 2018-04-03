#!/bin/bash

set -x

PREV_CREDENTIAL=$HOME"/.credentials/client_secret.json"
rm -rf $PREV_CREDENTIAL

sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python-pip3 python-dev build-essential
pip3 install --upgrade pip
pip3 install --upgrade virtualenv

brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip3 install Cython==0.26.1
pip3 install kivy
pip3 install https://github.com/kivy/kivy/archive/master.zip

pip3 install bs4

pip3 install --upgrade google-api-python-client

pip3 install oauth2client

pip3 install arrow

pip3 install boto3

pip3 install awscli

pip3 install lxml

pip3 install pynput
