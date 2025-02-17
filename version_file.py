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
           StringStruct(u'FileDescription', u'Windows Whisper Speech Recognition'),
           StringStruct(u'FileVersion', u'1.0.0'),
           StringStruct(u'InternalName', u'Windows Whisper'),
           StringStruct(u'LegalCopyright', u'MIT License'),
           StringStruct(u'OriginalFilename', u'Windows Whisper.exe'),
           StringStruct(u'ProductName', u'Windows Whisper'),
           StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
