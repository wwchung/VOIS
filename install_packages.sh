#!/bin/bash

set -x

PREV_CREDENTIAL=$HOME"/.credentials/client_secret.json"
rm -rf $PREV_CREDENTIAL

pip install kivy

pip install bs4

pip install --upgrade google-api-python-client

pip install oauth2client

pip install arrow

pip install docx
