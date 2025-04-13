@echo off

if not exist ".venv" (
    py -m venv .venv
    echo Virtual environment created.
)

call .venv\Scripts\activate.bat

pip install -r requirements.txt
@REM pip install .