@echo off
rem Caminho do diretório atual do .bat
set "PROJECT_DIR=%~dp0"

rem Muda para esse diretório
cd /d "%PROJECT_DIR%"

:: (opcional) ativar venv
call "%PROJECT_DIR%\venv\Scripts\activate.bat"

:: roda o script como módulo; o cwd entra no sys.path
python -m metarelogio
