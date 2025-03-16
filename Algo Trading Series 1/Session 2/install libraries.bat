@echo off
REM Check if the .whl files are in the same directory as the script
set twistedWhl=%~dp0Twisted-20.3.0-cp38-cp38-win_amd64.whl
set taLibWhl=%~dp0TA_Lib-0.4.24-cp38-cp38-win_amd64.whl

if not exist "%twistedWhl%" (
    echo ====================================================================
    echo ERROR: Twisted-20.3.0-cp38-cp38-win_amd64.whl not found in the script directory.
    echo Please ensure the file is in the same directory as this script.
    echo ====================================================================
    timeout /t 20
    exit /b
)

if not exist "%taLibWhl%" (
    echo ====================================================================
    echo ERROR: TA_Lib-0.4.24-cp38-cp38-win_amd64.whl not found in the script directory.
    echo Please ensure the file is in the same directory as this script.
    echo ====================================================================
    timeout /t 20
    exit /b
)

REM Check Python version
set pyversion=
for /f "tokens=2 delims= " %%A in ('python --version 2^>^&1') do set pyversion=%%A
if "%pyversion%"=="" (
    echo ====================================================================
    echo Python is not installed or not added to PATH. Please install Python 3.8.0.
    echo ====================================================================
    timeout /t 20
    exit /b
)

echo Detected Python version: %pyversion%
if "%pyversion%" NEQ "3.8.0" (
    echo ====================================================================
    echo Your Python version is not 3.8.0. Please uninstall all other versions.
    echo If you are using Conda, please uninstall it, as it interferes with library installation.
    echo ====================================================================
    timeout /t 20
    exit /b
)

REM Upgrade pip
echo Upgrading pip to the latest version...
python -m pip install --upgrade pip

REM Generate and add trusted root certificates
echo Generating and adding trusted root certificates...
certutil -generateSSTFromWU roots.sst
if %errorlevel% neq 0 (
    echo ====================================================================
    echo WARNING: Failed to generate the trusted root certificates.
    echo Please ensure you have administrative privileges and internet access.
    echo Continuing without root certificates...
    echo ====================================================================
)

certutil -addstore -f root roots.sst
if %errorlevel% neq 0 (
    echo ====================================================================
    echo WARNING: Failed to add the trusted root certificates to the store.
    echo Please ensure you have administrative privileges.
    echo Continuing without adding certificates...
    echo ====================================================================
)

REM Proceed with library installation
echo Proceeding with library installation...
pip install dhanhq
pip install typing
pip install typing-extensions
pip install logging
pip install pdbpp
pip install Twisted
pip install pyOpenSSL
pip install autobahn
pip install pandas
pip install smartapi-python
pip install websocket-client
pip install xlwings
pip install -Iv xlwings
pip install mibian
pip install numpy
pip install xlrd
pip install plyer
pip install dateparser
pip install halo
pip install ta
pip install pandas-ta
pip install nsepy
pip install scipy
pip install selenium
pip install tapy
pip install dataclasses
pip install openpyxl
pip install urllib3
pip install requests
pip install auto-py-to-exe
pip install chromedriver-autoinstaller

REM Install the .whl files from the script directory
echo Installing local .whl files...
pip install "%~dp0Twisted-20.3.0-cp38-cp38-win_amd64.whl"
pip install "%~dp0TA_Lib-0.4.24-cp38-cp38-win_amd64.whl"

pause
