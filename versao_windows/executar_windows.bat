@echo off
chcp 65001 > nul
cd /d "%~dp0"

if exist "CSVExpress.exe" (
    start "" "CSVExpress.exe" %*
) else if exist "dist\CSVExpress.exe" (
    start "" "dist\CSVExpress.exe" %*
) else (
    echo Iniciando via Python a partir de main_windows.py...
    start "" pythonw main_windows.py %*
)
