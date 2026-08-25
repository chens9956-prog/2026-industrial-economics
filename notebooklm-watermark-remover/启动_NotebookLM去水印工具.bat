@echo off
cd /d "%~dp0"
if exist "C:\Users\ausu\AppData\Local\Programs\Python\Python312\pythonw.exe" (
    start "" "C:\Users\ausu\AppData\Local\Programs\Python\Python312\pythonw.exe" "app.pyw"
) else (
    start "" pyw -3.12 "app.pyw"
)
exit
