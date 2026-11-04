@echo off

REM Django project folder
cd C:\iMentor_Github\imentor

REM Activate virtualenv
call venv\Scripts\activate.bat

REM Run backup script
python backup.py