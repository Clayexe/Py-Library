# Build an executable with PyInstaller (Windows PowerShell)
# Updated for reorganized package structure
# Usage: Open PowerShell, activate your venv, then run:
#    ./build_exe.ps1

# Ensure PyInstaller is installed
Write-Host "Installing PyInstaller..." -ForegroundColor Cyan
python -m pip install --quiet pyinstaller

# Get the current directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Determine paths
$entryPoint = Join-Path $scriptDir "run_library_modern.py"
$distDir = Join-Path $scriptDir "dist"
$workDir = Join-Path $scriptDir "build"

Write-Host "Building LibraryCollection.exe..." -ForegroundColor Cyan
Write-Host "Entry point: $entryPoint" -ForegroundColor Gray

# Create one-file, windowed executable (no console)
# Includes the Library_app package
& python -m PyInstaller --noconfirm --onefile --windowed --name LibraryCollection --add-data "Library_app:Library_app" --distpath "$distDir" --workpath "$workDir" --specpath "$scriptDir" "$entryPoint"

$buildExitCode = $LASTEXITCODE

if ($buildExitCode -eq 0) {
    Write-Host "`nBuild finished successfully!" -ForegroundColor Green
    Write-Host "Executable location: $distDir\LibraryCollection.exe" -ForegroundColor Green
    
    # Optional: Show file info
    $exePath = Join-Path $distDir "LibraryCollection.exe"
    if (Test-Path $exePath) {
        $fileSize = (Get-Item $exePath).Length / 1MB
        Write-Host "File size: $([Math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
    }
} else {
    Write-Host "`nBuild failed with exit code $buildExitCode" -ForegroundColor Red
    Write-Host "Check build output above for details." -ForegroundColor Yellow
    exit $buildExitCode
}
