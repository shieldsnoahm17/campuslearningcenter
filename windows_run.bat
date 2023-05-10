@echo off
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Setting environment variables...
set FLASK_APP=app.py

echo Starting Flask app...
start "" "http://127.0.0.1:5000/"
flask run
