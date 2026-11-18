@echo off
chcp 65001 > nul
cd /d "%~dp0.."
title CSV Express - Gerador de Executável Windows (.EXE)

echo ======================================================
echo    CSV Express - PDF para CSV - Versão Windows
echo ======================================================
echo.

:: 1. Verifica se o Python está instalado no Windows
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não foi encontrado no PATH do Windows!
    echo Por favor, instale o Python em https://www.python.org/downloads/
    echo Lembre-se de marcar a opção "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b 1
)

echo [1/3] Instalando dependências necessárias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install "pyinstaller>=6.0.0"
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências.
    pause
    exit /b 1
)

echo.
echo [2/3] Compilando executável portátil (.exe) usando a implementação compartilhada...
python -m PyInstaller --noconfirm --onefile --windowed --paths . --icon=versao_windows\app_icon.ico --add-data "icone.png;." --add-data "csv_express_ilustracao.png;." --name "CSVExpress" main_windows.py
if %errorlevel% neq 0 (
    echo [ERRO] Falha na compilação do executável.
    pause
    exit /b 1
)

echo.
echo [3/3] Finalizando e organizando arquivos...
if exist "dist\CSVExpress.exe" (
    copy /y "dist\CSVExpress.exe" "versao_windows\CSVExpress.exe" > nul
    echo.
    echo ======================================================
    echo  SUCESSO TOTAL!
    echo  O executável portátil foi gerado:
    echo  -^> versao_windows\CSVExpress.exe
    echo.
    echo  Basta dar 2 cliques no arquivo CSVExpress.exe para usar!
    echo ======================================================
) else (
    echo [AVISO] O executável foi gerado dentro da pasta "dist\".
)

echo.
pause
