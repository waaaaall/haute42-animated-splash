@echo off
setlocal enabledelayedexpansion
title Haute42 Animated Splash Screen Firmware Generator

echo ========================================================
echo   Haute42 G16 Custom Animated Splash Firmware Generator
echo ========================================================
echo.

:: 1. Check Python installation
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.8 or later from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: 2. Check Pillow dependency
python -c "import PIL" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing required dependency (Pillow)...
    python -m pip install --quiet pillow
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install Pillow. Please run: pip install pillow
        pause
        exit /b 1
    )
)

:: 3. Run Patcher
echo [INFO] Generating custom firmware from custom_gif/ (or sample_gif/)...
python "%~dp0patch_splash.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Firmware generation failed! See error message above.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   [SUCCESS] firmware_custom.uf2 has been created!
echo ========================================================
echo.
echo Flash instructions:
echo  1. Unplug your Haute42 G16 controller.
echo  2. Hold down the BOOTSEL button (or UP button / BOOT key).
echo  3. Plug the USB cable into your PC (an 'RPI-RP2' drive appears).
echo  4. Drag and drop 'firmware_custom.uf2' onto the 'RPI-RP2' drive.
echo  5. The controller will reboot automatically and enjoy your animated splash!
echo.
pause
