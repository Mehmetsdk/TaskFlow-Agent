$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root ".venv\Scripts\python.exe"
if (-Not (Test-Path $python)) {
    Write-Error "Python executable not found at $python. Activate your venv or run from project root."
    exit 1
}
Start-Process -FilePath $python -ArgumentList "main.py" -WorkingDirectory $root
