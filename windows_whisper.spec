# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

version_info = VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=(1, 0, 0, 0),
        prodvers=(1, 0, 0, 0),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    u'040904B0',
                    [StringStruct(u'CompanyName', u''),
                     StringStruct(u'FileDescription', u'XWhisper Speech Recognition'),
                     StringStruct(u'FileVersion', u'1.0.0'),
                     StringStruct(u'InternalName', u'XWhisper'),
                     StringStruct(u'LegalCopyright', u'MIT License'),
                     StringStruct(u'OriginalFilename', u'XWhisper.exe'),
                     StringStruct(u'ProductName', u'XWhisper'),
                     StringStruct(u'ProductVersion', u'1.0.0')])
            ]),
        VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
    ]
)

block_cipher = None

a = Analysis(
    ['speech_engine.py'],
    pathex=[],
    binaries=[],
    datas=[(r'C:/Users/Daniel/CascadeProjects/windows_whisper/assets/icon.ico', 'assets')],
    hiddenimports=['PyQt6.sip'],
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
    version=version_info,
    icon=r'C:/Users/Daniel/CascadeProjects/windows_whisper/assets/icon.ico'
)
