@echo off
REM ===============================================
REM Build GetMachineID.exe - Utilitaire client
REM Par Mondher ADOUDI - Sidr Valley AI
REM ===============================================

echo.
echo ================================================
echo    BUILD GETMACHINEID.EXE
echo    Utilitaire pour clients distants
echo ================================================
echo.

REM Vérifier PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [1/3] Installation de PyInstaller...
    pip install pyinstaller
) else (
    echo [1/3] PyInstaller detecte : OK
)
echo.

REM Nettoyer
echo [2/3] Nettoyage...
if exist build\GetMachineID rmdir /s /q build\GetMachineID
if exist dist\GetMachineID.exe del /q dist\GetMachineID.exe
echo     Nettoyage termine
echo.

REM Build
echo [3/3] Compilation de GetMachineID.exe...
echo     Ceci peut prendre 1-2 minutes...
echo.

pyinstaller --onefile ^
    --name "GetMachineID" ^
    --icon icons\icon.ico ^
    --console ^
    --clean ^
    get_machine_id.py

if errorlevel 1 (
    echo.
    echo [ERREUR] La compilation a echoue
    pause
    exit /b 1
)

echo.
echo ================================================
echo    BUILD TERMINE !
echo ================================================
echo.
echo Executable : dist\GetMachineID.exe
echo Taille     :
dir dist\GetMachineID.exe | find "GetMachineID.exe"
echo.
echo Pour distribuer :
echo   1. Envoyez dist\GetMachineID.exe au client
echo   2. Client l'execute et vous envoie son Machine ID
echo   3. Vous generez sa licence avec generate_customer_license.py
echo.
pause
