@echo off
:loop
python main.py
if %errorlevel% equ 100 (
    cls
    goto loop
)
pause