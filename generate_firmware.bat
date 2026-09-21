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
echo [INFO] Generating custom firmware from sample_gif/...
python "%~dp0patch_splash.py" %*

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
echo Flash instructions (Official Haute42 & GP2040-CE methods):
echo  1. Put controller into BOOTSEL mode:
echo     - Hold the small BOOT button while plugging in USB cable, OR
echo     - Hold Start+X+Y (or Start+Select+Up) for 5 seconds while connected, OR
echo     - Hold START while connecting -^> open http://192.168.7.1 -^> Reboot -^> Bootsel.
echo  2. An 'RPI-RP2' USB drive will appear on your PC.
echo  3. Drag and drop 'firmware_custom.uf2' onto the 'RPI-RP2' drive.
echo  4. The device will automatically reboot with your new animated splash!
echo.
echo Note: If Windows prompts you to format the drive, do NOT format.
echo.
pause
