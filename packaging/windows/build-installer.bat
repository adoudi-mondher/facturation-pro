@echo off
REM Script de compilation automatique de l'installateur Easy Facture
REM Par Mondher ADOUDI - Sidr Valley AI

echo ============================================================
echo COMPILATION DE L'INSTALLATEUR EASY FACTURE v1.7.0
echo ============================================================
echo.

REM Nettoyer le dossier output
echo [1/3] Nettoyage du dossier output...
if exist output (
    rmdir /s /q output 2>nul
    timeout /t 1 /nobreak >nul
)
mkdir output
echo OK Dossier output nettoye
echo.

REM Compiler avec Inno Setup
echo [2/3] Compilation de l'installateur...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo SUCCES ! L'installateur a ete cree avec succes
    echo ============================================================
    echo.
    echo Fichier cree : output\EasyFacture-Setup-v1.7.0.exe
    echo.

    REM Afficher la taille du fichier
    echo [3/3] Informations sur le fichier :
    dir output\EasyFacture-Setup-v1.7.0.exe | find "EasyFacture"
    echo.
    echo ============================================================
    echo Vous pouvez maintenant tester l'installateur !
    echo ============================================================
) else (
    echo.
    echo ERREUR ! La compilation a echoue.
    echo Verifiez les messages d'erreur ci-dessus.
)

echo.
pause
