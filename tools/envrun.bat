@echo off
set VENV_NAME=.venv

rem Activate the virtual environment
call ..\%VENV_NAME%\Scripts\activate

rem Change directory to the location of main.py (assuming it's in the /src folder)
cd ..\src

rem Run the main.py script
pythonw afoaic.py

rem Deactivate the virtual environment when the script is done (optional)
deactivate
