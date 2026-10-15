@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Creando entorno virtual...
  py -m venv .venv
)
call .venv\Scripts\activate.bat
echo Instalando dependencias necesarias...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo No se pudieron instalar las dependencias. Revisa tu conexion a Internet.
  pause
  exit /b 1
)
echo Abriendo el sistema en http://127.0.0.1:5000
python app.py
pause
