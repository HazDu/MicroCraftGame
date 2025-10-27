import os
from PyInstaller.utils.hooks import collect_submodules, collect_all

block_cipher = None
spec_root = os.path.abspath(SPECPATH)

game_modules = collect_submodules('game')
datas, binaries, hiddenimports = collect_all('game')

a = Analysis(
    ['game/main.py'],
    pathex=[spec_root],
    binaries=binaries,
    datas=datas + [
        ('game/assets', 'game/assets'),
    ],
    hiddenimports=[
        'pygame',
        'numpy',
        'tkinter',
        'json',
        'zipfile',
        'platform',
    ] + game_modules + hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MicroCraftGame',
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
