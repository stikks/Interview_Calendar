# -*- mode: python -*-

block_cipher = None


a = Analysis(['setup.py'],
             pathex=['/home/stikks/Documents/projects/Interview_Calendar/venv/lib/python3.5/site-packages', '/home/stikks/Documents/projects/Interview_Calendar'],
             binaries=[],
             datas=[('endpoints', 'endpoints'), ('app', 'app'), ('services', 'services'), ('templates', 'templates')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='setup',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
