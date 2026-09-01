# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['master_hub.py'],
    pathex=[],
    binaries=[
        ('dist/ai_manager.exe', '.'),
        ('dist/bloatware_remover.exe', '.'),
        ('dist/explorer_config.exe', '.'),
        ('dist/system_tweaker.exe', '.')
    ],
    datas=[],
    hiddenimports=[],
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
    name='master_hub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)