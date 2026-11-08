# PyInstaller build recipe for the Windows .exe
#
# Build:   pyinstaller PasswordManager.spec --noconfirm
# Output:  dist/PasswordManager.exe

a = Analysis(
    ["main.py"],
    datas=[("logo.png", ".")],  # bundled next to the code inside the .exe
    excludes=["PIL", "numpy", "unittest", "pydoc", "test"],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PasswordManager",
    icon="assets/icon.ico",
    console=False,  # no black command window behind the app
    upx=False,      # UPX-packed files trigger more antivirus false positives
)
