# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['wrapper.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('models', 'models'), ('generators', 'generators'), ('instance', 'instance')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'sqlalchemy', 'jinja2', 'werkzeug', 'openpyxl', 'click', 'blinker', 'itsdangerous', 'markupsafe'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RFID管理系统控制台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
