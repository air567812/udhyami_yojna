# Udhyami Yojna PowerShell Launcher
Write-Host "===================================================" -ForegroundColor Green
Write-Host " Starting Udhyami Yojna Platform" -ForegroundColor Yellow
Write-Host " Government Scheme Discovery & Subsidy Advisory" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

$venvPython = ".\.venv\Scripts\python.exe"
$venvUvicorn = ".\.venv\Scripts\uvicorn.exe"

if (Test-Path $venvUvicorn) {
    Write-Host "Starting server via virtual environment on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
    & $venvUvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
} else {
    Write-Host "Virtual environment not found, invoking system uvicorn..." -ForegroundColor Yellow
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
}
