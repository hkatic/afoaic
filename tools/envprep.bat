@echo off

rem Create a virtual environment named .venv
python -m venv ..\.venv

rem Activate the virtual environment
call ..\.venv\Scripts\activate

rem Install dependencies from requirements.txt
pip install -r ..\requirements.txt

rem Deactivate the virtual environment
deactivate
