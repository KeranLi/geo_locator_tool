@echo off
cd /d "%~dp0"
echo Installing build dependencies...
python -m pip install pyinstaller requests
if errorlevel 1 (
  echo PyInstaller installation failed. Check network or Python installation.
  pause
  exit /b 1
)
python -m PyInstaller --noconfirm --clean --onefile --windowed --name geo_locator geo_locator_ui.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)
echo.
echo Build complete: %~dp0dist\geo_locator.exe
pause
