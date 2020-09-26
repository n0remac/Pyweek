# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import arcade
import pymunk
import os

a = Analysis(['run_game.py'],
             pathex=['/home/free/code/Pyweek'],
             binaries=[ (pymunk.chipmunk_path, '.') ],
             datas=[(os.path.abspath(arcade.__file__ + '/../'), 'arcade')],
             hiddenimports=['arcade', 'pymunk'],
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
          [],
          exclude_binaries=True,
          name='acolyte',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='run_game')
