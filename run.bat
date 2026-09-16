@echo off
title Udhyami Yojna Server
echo ===================================================
echo Starting Udhyami Yojna Platform...
echo Government Scheme Discovery & AI Subsidy Advisory
echo ===================================================
echo.

if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    ".venv\Scripts\uvicorn.exe" backend.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    echo Virtual environment not found, falling back to system python...
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
)

pause
