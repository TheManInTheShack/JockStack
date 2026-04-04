@echo off
:: ------------------------------------------------------------------------------
:: JockStack — update.bat
:: Run from the repo root after pulling changes to keep your local environment
:: current. Creates the venv on first run if it doesn't exist.
:: Usage: update
:: ------------------------------------------------------------------------------

echo.
echo [JockStack] Pulling latest changes...
git pull
if errorlevel 1 (
    echo [ERROR] git pull failed. Check your network or branch status.
    exit /b 1
)

:: Create venv if it doesn't exist
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo [JockStack] No venv found — creating one...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv. Is Python installed and on PATH?
        exit /b 1
    )
    echo [JockStack] venv created.
)

:: Activate and install dependencies
echo.
echo [JockStack] Installing/updating backend dependencies...
call venv\Scripts\activate.bat
python -m pip install -q -r backend\requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed. See output above.
    exit /b 1
)

echo.
echo [JockStack] Done. To start the dev server:
echo.
echo     python -m uvicorn main:app --app-dir backend --reload
echo.
echo Then open: http://localhost:8000/docs
echo.
