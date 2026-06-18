Write-Host ""
Write-Host "=== Secretariat Checks ==="
Write-Host ""

Write-Host "Running tests..."
python -m pytest

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Tests failed."
    exit 1
}

Write-Host ""
Write-Host "Compiling Python files..."
python -m compileall .

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Compilation failed."
    exit 1
}

python -c "from app import app; print('app import ok')"

Write-Host ""
Write-Host "All checks passed."