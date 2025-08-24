Write-Host "Building Paperless File Uploader executable..." -ForegroundColor Green

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not detected. Activating..." -ForegroundColor Yellow
    & ".\.env\Scripts\Activate.ps1"
}

pyinstaller --onefile --noconsole .\upload_to_paperless.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully! Executable available in dist folder." -ForegroundColor Green
} else {
    Write-Host "Build failed with exit code $LASTEXITCODE" -ForegroundColor Red
}