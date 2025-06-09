@echo off
REM Batch file for Poetry-based mbox_converter
REM Usage: Drag & drop a .mbox file onto this .bat file

SETLOCAL

REM Path to the directory containing this BAT file
SET "SCRIPT_DIR=%~dp0"

REM Get absolute path of the dragged .mbox file
SET "MBOX_FILE=%~f1"

IF "%MBOX_FILE%"=="" (
    echo [ERROR] Please drag an .mbox file onto this .bat file.
    pause
    EXIT /B 1
)

REM Step 1: Change to project directory
CD /D "%SCRIPT_DIR%"

REM Step 2: Install Poetry environment (only if needed)
where poetry >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Poetry not found. Please install Poetry first.
    pause
    EXIT /B 1
)

REM Step 3: Install dependencies via Poetry (if not already installed)
echo [INFO] Installing dependencies via Poetry ...
poetry install

REM Step 4: Run script using Poetry
echo [INFO] Running mbox_converter ...
poetry run python -m mbox_converter.cli "%MBOX_FILE%"

echo.
echo Done processing: %MBOX_FILE%
pause
ENDLOCAL
