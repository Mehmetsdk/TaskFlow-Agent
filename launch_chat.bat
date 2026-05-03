@echo off
pushd %~dp0
if exist .venv\Scripts\python.exe (
  .\.venv\Scripts\python.exe main.py
) else (
  echo Virtualenv python not found. Activate your environment or run: python main.py
)
popd
