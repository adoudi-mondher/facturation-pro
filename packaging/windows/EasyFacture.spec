# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../../run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../../app', 'app'),
        ('../../data', 'data'),
        ('../../static', 'static'),
        ('../../config.py', '.'),
        ('../../icons', 'icons')
    ],
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'flask_migrate',
        'flask_wtf',
        'flask_mail',
        'werkzeug',
        'jinja2',
        'openpyxl',
        'reportlab',
        'sqlalchemy',
        'wtforms',
        'email_validator',
        'cryptography',
        'cryptography.fernet',
        'PIL',
        'PIL.Image',
        'dateutil',
        'dateutil.parser'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EasyFacture',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../../icons/icon.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EasyFacture'
)
