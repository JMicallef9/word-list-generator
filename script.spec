# -*- mode: python ; coding: utf-8 -*-

import platform
from pathlib import Path

binaries = []

system = platform.system()

if system == "Windows":
    bin_path = Path("bin/windows")
    binaries = [
        (str(bin_path / "mkvmerge.exe"), "bin/windows"),
        (str(bin_path / "mkvextract.exe"), "bin/windows") 
    ]
elif system == "Linux":
    bin_path = Path("bin/linux")
    binaries = [
        (str(bin_path / "mkvmerge"), "bin/linux"),
        (str(bin_path / "mkvextract"), "bin/linux") 
    ]


a = Analysis(
    ['src/script.py'],
    pathex=[str(Path(__file__).parent)],
    binaries=binaries,
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
    name='script',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
