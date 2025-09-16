# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# List all DLL files that need to be included
binaries = [
    ('dlls/libzbar-64.dll', 'pyzbar'),
    ('dlls/libiconv.dll', 'pyzbar'),
    ('dlls/zlib1.dll', 'pyzbar'),
    ('dlls/libjpeg.dll', 'pyzbar'),
]

# Data files to include in the bundle (IMPORTANT: must be before Analysis)
datas = [
    ('fonts', 'fonts'),  # Include entire fonts directory with all Arial variants
    ('data', 'data'),  # Include entire data directory
    ('logo', 'logo'),  # Include entire logo directory with multi-size icon
    ('database', 'database'),  # Include database module
    ('utils', 'utils'),  # Include utils module
    ('resources', 'resources'),  # Include resources directory
    ('MASTER_RECOVERY_KEYS.txt', '.'),  # Include master recovery keys
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,  # Now properly included
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'sqlite3',
        'barcode',
        'barcode.writer',
        'qrcode',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib.pagesizes',
        'reportlab.lib.colors',
        'reportlab.platypus',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.figure',
        'openpyxl',
        'openpyxl.utils',
        'pandas',
        'numpy',
        'win32print',
        'win32api',
        'win32con',
        'win32gui',
        'win32ui',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.ImageEnhance',
        'pyzbar',
        'pyzbar.pyzbar',
        'cv2',
        'bcrypt',
        'pythoncom',
        'win32com.client',
        'database.models',
        'utils.barcode',
        'utils.barcode_scanner',
        'utils.data_manager',
        'utils.report_generator',
        'utils.database',
    ],
    hookspath=['.'],  # For custom hook files
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
    name='JewelryManagementSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed mode (no console)
    icon='logo/256x256.ico',  # Use high-quality 256x256 ICO for best taskbar icon
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    onefile=True  # Single executable output - no COLLECT needed
)