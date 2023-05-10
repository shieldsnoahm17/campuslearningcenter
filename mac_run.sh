#!/bin/bash

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo Creating virtual environment...
    python3 -m venv "$VENV_DIR"
fi

echo Activating virtual environment...
source "$VENV_DIR"/bin/activate

echo Installing dependencies...
pip3 install -r "$REQUIREMENTS_FILE"

echo Setting environment variables...
export FLASK_APP=app.py

echo Opening web browser...
xdg-open "http://127.0.0.1:5000/"

echo Starting Flask app...
nohup flask run