@echo off
REM Windows start script: creates venv, installs requirements and runs the app
cd /d %~dp0

if not exist venv (
  echo Creating virtual environment...
  python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
