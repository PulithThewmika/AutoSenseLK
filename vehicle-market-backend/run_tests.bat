@echo off
REM run_tests.bat
cd %~dp0
call "..\.venv\Scripts\activate.bat"
python -m pytest tests\ -v
