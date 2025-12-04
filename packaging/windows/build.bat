@echo off
REM ===============================================
REM Easy Facture - Script de build Windows
REM Par Mondher ADOUDI - Sidr Valley AI
REM ===============================================

echo.
echo ================================================
echo    EASY FACTURE - BUILD WINDOWS .EXE
echo    Version 1.5.0
echo ================================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

echo [1/5] Python detecte : OK
echo.

REM Vérifier PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [2/5] Installation de PyInstaller...
    pip install pyinstaller
) else (
    echo [2/5] PyInstaller deja installe : OK
)
echo.

REM Nettoyer les builds precedents
echo [3/5] Nettoyage des builds precedents...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist EasyFacture.spec del /q EasyFacture.spec
echo     Nettoyage termine
echo.

REM Creer le .spec file
echo [4/5] Creation du fichier de configuration...
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
echo         ^('../../config.py', '.'^)
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
echo         'email_validator'
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
echo     icon='icon.ico'
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
echo [5/5] Build de l'executable...
echo     Ceci peut prendre 2-5 minutes...
echo.
pyinstaller EasyFacture.spec --clean

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
echo Executable : dist\EasyFacture\EasyFacture.exe
echo.
echo Pour tester :
echo   cd dist\EasyFacture
echo   EasyFacture.exe
echo.
echo Pour distribuer :
echo   Compressez le dossier dist\EasyFacture en ZIP
echo.
pause
