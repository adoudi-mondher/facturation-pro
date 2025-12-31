@echo off
REM ===============================================
REM Easy Facture - Build VERSION CLIENT (propre)
REM Par Mondher ADOUDI - Sidr Valley AI
REM Version 1.6.0
REM ===============================================

echo.
echo ================================================
echo    EASY FACTURE - BUILD VERSION CLIENT
echo    Version 1.6.0 (Distribution propre)
echo ================================================
echo.
echo ATTENTION: Ce build sera SANS vos donnees de test
echo    Utiliser pour: Distribution aux clients
echo    Ne PAS utiliser pour: Votre version perso
echo.
set /p confirm="Continuer? (o/n): "
if /i not "%confirm%"=="o" (
    echo Build annule
    exit /b 0
)
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo [1/6] Python detecte : OK
echo.

REM Vérifier PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [2/6] Installation de PyInstaller...
    pip install pyinstaller
) else (
    echo [2/6] PyInstaller deja installe : OK
)
echo.

REM Nettoyer SANS sauvegarder (build propre pour client)
echo [3/6] Nettoyage complet (SANS sauvegarde)...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist EasyFacture.spec del /q EasyFacture.spec
echo     Nettoyage termine (build propre pour client)
echo.

REM Créer le .spec file (identique au build normal)
echo [4/6] Creation du fichier de configuration...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis^(
echo     ['../../run.py'^],
echo     pathex=[],
echo     binaries=[],
echo     datas=[
echo         ^('../../app', 'app'^),
echo         ^('../../data', 'data'^),
echo         ^('../../static', 'static'^),
echo         ^('../../config.py', '.'^),
echo         ^('../../icons', 'icons'^)
echo     ],
echo     hiddenimports=[
echo         'flask',
echo         'flask_sqlalchemy',
echo         'flask_migrate',
echo         'flask_wtf',
echo         'flask_mail',
echo         'werkzeug',
echo         'jinja2',
echo         'openpyxl',
echo         'reportlab',
echo         'sqlalchemy',
echo         'wtforms',
echo         'email_validator',
echo         'cryptography',
echo         'cryptography.fernet',
echo         'PIL',
echo         'PIL.Image',
echo         'dateutil',
echo         'dateutil.parser'
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo ^)
echo.
echo pyz = PYZ^(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE^(
echo     pyz,
echo     a.scripts,
echo     [],
echo     exclude_binaries=True,
echo     name='EasyFacture',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     console=True,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon='../../icons/icon.ico'
echo ^)
echo.
echo coll = COLLECT^(
echo     exe,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     name='EasyFacture'
echo ^)
) > EasyFacture.spec

echo     Configuration creee : EasyFacture.spec
echo.

REM Build
echo [5/6] Build de l'executable...
echo     Ceci peut prendre 2-5 minutes...
echo.
pyinstaller EasyFacture.spec --clean

if errorlevel 1 (
    echo.
    echo [ERREUR] La compilation a echoue
    pause
    exit /b 1
)

REM Créer structure data vide pour le client
echo.
echo [6/6] Creation d'un dossier data/ vide pour le client...
if exist dist\EasyFacture\EasyFacture.exe (
    mkdir dist\EasyFacture\data\uploads\logos 2>nul
    mkdir dist\EasyFacture\data\uploads\factures 2>nul
    mkdir dist\EasyFacture\data\backups 2>nul

    REM Créer fichiers .gitkeep
    type nul > dist\EasyFacture\data\uploads\.gitkeep
    type nul > dist\EasyFacture\data\backups\.gitkeep

    echo     Dossier data/ vide cree
    echo     Structure: data/uploads/, data/backups/
) else (
    echo     ERREUR: EasyFacture.exe non trouve
    pause
    exit /b 1
)

REM Vérifier qu'il n'y a pas de base de données
if exist dist\EasyFacture\data\facturation.db (
    echo     ATTENTION: Base de donnees detectee (suppression...)
    del /q dist\EasyFacture\data\facturation.db
)

echo     Aucune donnee personnelle detectee
echo.

echo ================================================
echo    BUILD CLIENT TERMINE !
echo ================================================
echo.
echo Package client (PROPRE) : dist\EasyFacture\
echo Sans donnees personnelles: OUI
echo.
echo Pour distribuer :
echo   1. Compresser le dossier dist\EasyFacture\
echo      (clic droit ^> Envoyer vers ^> Dossier compresse)
echo.
echo   2. Renommer en: EasyFacture-v1.6.0-Client.zip
echo.
echo   3. Envoyer au client
echo.
echo   4. Le client decompresse et lance EasyFacture.exe
echo      - L'app creera automatiquement la base de donnees vide
echo      - Le client entrera sa licence au premier lancement
echo.
echo Package pret pour distribution !
echo.
pause
