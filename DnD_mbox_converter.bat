@echo off
REM Batch file for mbox_converter
REM Usage: Drag & drop a .mbox file onto this .bat file

SETLOCAL

REM Path to the directory containing this BAT file
SET "SCRIPT_DIR=%~dp0"
SET "VENV_DIR=%SCRIPT_DIR%.venv"

REM Get absolute path of the dragged .mbox file
SET "MBOX_FILE=%~f1"

IF "%MBOX_FILE%"=="" (
    echo [ERROR] Please drag an .mbox file onto this .bat file.
    pause
    EXIT /B 1
)

REM Step 1: Create virtual environment if it doesn't exist
IF NOT EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment in %VENV_DIR% ...
    python -m venv "%VENV_DIR%"
)

REM Step 2: Activate virtual environment
CALL "%VENV_DIR%\Scripts\activate.bat"

REM Step 3: Install dependencies if requirements.txt exists
IF EXIST "%SCRIPT_DIR%requirements.txt" (
    echo [INFO] Installing dependencies ...
    pip install -r "%SCRIPT_DIR%requirements.txt"
) ELSE (
    echo [WARNING] No requirements.txt found!
)

REM Step 4: Change to script directory and run module
CD /D "%SCRIPT_DIR%"
python -m mbox_converter.cli "%MBOX_FILE%"

echo.
echo Done processing: %MBOX_FILE%
pause
ENDLOCAL
