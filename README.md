# Paperless File Uploader

Small script to upload files to Paperless on Windows. Ease automation with scanners.

Tested with Python 3.11. Requirements are only required to build an executable file. Otherwise, the script only uses the standard libraries.

## Setup

Prepare the virtual env.

```powershell
python -m venv .env
.\.env\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Build

From the virtual env.

```powershell
pyinstaller.exe --onefile --noconsole .\upload_to_paperless.py
```

Executable file will be available in the `dist` folder. From PowerShell, [`build.ps1`](build.ps1) can alternatively be used.
