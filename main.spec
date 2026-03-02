# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and metadata for problematic packages
nidaqmx_datas, nidaqmx_binaries, nidaqmx_hiddenimports = collect_all('nidaqmx')
mysql_datas, mysql_binaries, mysql_hiddenimports = collect_all('mysql.connector')
reportlab_datas, reportlab_binaries, reportlab_hiddenimports = collect_all('reportlab')
serial_datas, serial_binaries, serial_hiddenimports = collect_all('serial')
openpyxl_datas, openpyxl_binaries, openpyxl_hiddenimports = collect_all('openpyxl')
et_xmlfile_datas, et_xmlfile_binaries, et_xmlfile_hiddenimports = collect_all('et_xmlfile')

# Add libmysql.dll manually
libmysql_path = r'C:\Users\tgerardin\AppData\Roaming\Python\lib\site-packages\libmysql.dll'
if os.path.exists(libmysql_path):
    mysql_binaries.append((libmysql_path, '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[] + nidaqmx_binaries + mysql_binaries + reportlab_binaries + serial_binaries + openpyxl_binaries + et_xmlfile_binaries,
    datas=[
        ('assets\\logo-big.png', '.'),
        ('steps', 'steps'),
        ('modules', 'modules'),
        ('assets', 'assets'),
    ] + nidaqmx_datas + mysql_datas + reportlab_datas + serial_datas + openpyxl_datas + et_xmlfile_datas,

    hiddenimports=[
        # PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        
        # Database connectivity
        'mysql.connector',
        'mysql.connector.errors',
        
        # Serial communication
        'serial',
        'serial.tools',
        'serial.tools.list_ports',
        
        # National Instruments DAQ
        'nidaqmx',
        'nidaqmx.system',
        'nidaqmx.task',
        'nidaqmx.constants',
        
        # PDF generation
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib.pagesizes',
        'reportlab.lib.units',
        'reportlab.lib.colors',

        # Configuration module
        'configuration',
        
        # Excel support
        'openpyxl',
        
        # Module Windows pour le son
        'winsound',
    ] + nidaqmx_hiddenimports + mysql_hiddenimports + reportlab_hiddenimports + serial_hiddenimports + openpyxl_hiddenimports + et_xmlfile_hiddenimports,
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
    name='main',
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
    icon='assets\\logo-big.png',
)