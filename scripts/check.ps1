Write-Host "Running tests..."
python -m pytest
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nTests failed."
    exit 1
}

Write-Host "`nCompiling Python files..."
python -m compileall .
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nCompilation failed."
    exit 1
}

Write-Host "`nValidating app import..."
python -c "from app import app; print('app import ok')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nImport validation failed."
    exit 1
}

Write-Host "`nAll checks passed."