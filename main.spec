# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\PU\\PycharmProjects\\SmartSecurityQuote'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('logo.jpg','C:\\Users\\PU\\PycharmProjects\\SmartSecurityQuote\\logo.jpg','DATA'),
			('logo_small.jpg','C:\\Users\\PU\\PycharmProjects\\SmartSecurityQuote\\logo_small.jpg','DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='logo.ico' )
		  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')


