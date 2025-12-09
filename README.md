Library Collection (Modern)

This is a small desktop app built with CustomTkinter to manage a local library collection.

Quick start

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the app:

```powershell
python "./Library_app/library_modern"
```

Packaging to a single executable (Windows)

1. Install PyInstaller in your environment:

```powershell
python -m pip install pyinstaller
```

2. Use the provided `build_exe.ps1` script to build:

```powershell
./build_exe.ps1
```

This will create a one-file, windowed executable named `LibraryCollection.exe` in the `dist` folder.

Notes

- The app copies uploaded cover images into the `covers/` folder.
- If you want thumbnails in the details panel, install `Pillow` (already listed in `requirements.txt`).
- The code file `Library_app/library_modern` is the main script used by the launcher.
