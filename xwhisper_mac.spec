# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['speech_engine.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/icon.icns', 'assets')],
    hiddenimports=['PyQt6.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

app = BUNDLE(
    EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name='XWhisper',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    ),
    name='XWhisper.app',
    icon='assets/icon.icns',
    bundle_identifier='com.xwhisper.app',
    info_plist={
        'CFBundleName': 'XWhisper',
        'CFBundleDisplayName': 'XWhisper',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
        'NSHumanReadableCopyright': 'MIT License',
    },
)