# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\afoaic.py'],
    pathex=[],
    datas=[('.\\src\\sounds\\*.ogg', '.\\sounds'), ('.\\src\\locale\\hr\\LC_MESSAGES\\*.mo', '.\\locale\\hr\\LC_MESSAGES')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='afoaic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='afoaic',
)
