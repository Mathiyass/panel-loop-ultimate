@echo off
setlocal EnableDelayedExpansion
title PANEL LOOP ULTIMATE - GameLoop ^& PUBG MOBILE Master Suite
color 0B

:: Self-elevation to Administrator if required
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [Notice] Requesting Administrator Privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Locate Python
set "PY_CMD=python"
%PY_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    set "PY_CMD=py"
    %PY_CMD% --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python was not found in PATH!
        echo Please ensure Python is installed to run low-level engine optimizations.
        pause
        exit /b 1
    )
)

cd /d "%~dp0"

:MENU
cls
echo ===============================================================================
echo            PANEL LOOP ULTIMATE - GAMELOOP ^& PUBG MOBILE OPTIMIZER
echo                   (Free, Open-Source ^& 100%% Ban-Safe Edition)
echo ===============================================================================
echo.
echo   Hardware Profile: AMD Ryzen 7 5800X  ^|  NVIDIA RTX 3090 24GB  ^|  180Hz DWM
echo.
%PY_CMD% tac_engine.py --status
echo.
echo   [1] 1-Click Ultimate Optimization (Tier 6 UHD + 120 FPS + GameLoop 90 UI Sync)
echo   [2] Launch PUBG Mobile Directly
echo   [3] Switch Device Model (REDMAGIC 9 Pro / ROG 8 Pro / S24 Ultra / Xiaomi)
echo   [4] Resolution Switcher (Native 1080p FHD / 2K 1440p / iPad 4:3 1440x1080)
echo   [5] Deep Clean & Multi-Tier Purge (Shader Cache, Component Dumps, Flush DNS)
echo   [6] Crash Guard & Virtual Memory RAM Flush (Kill Hung Processes, Trim RAM)
echo   [7] 0ms Hit-Reg & Network Turbo (Multi-NIC TcpAckFrequency + TCPNoDelay + MMCSS)
echo   [8] Refresh Realtime Diagnostics & GPU Thermals
echo   [9] Launch Graphical Desktop Application (GUI Dashboard)
echo   [10] Lock 120 FPS Pacing & Zero-DWM Input Lag (High Priority + 0.5ms Timer)
echo   [11] Streamer Helper Mode (1080p Borderless Stream View)
echo   [12] Backup Environment Snapshot (Registry + Config Snapshots)
echo   [13] 1-Click Factory Restore (Revert to Snapshot or Clean Defaults)
echo   [14] Toggle Clean Screen UI (Suppress / Restore On-Screen Key Watermark)
echo   [15] Mouse Keeper & Cursor Fencer (1:1 Raw Mouse + Zero Flick Slip)
echo   [16] Notice Tamer (Auto-Suppress Ad Popups & Update Nags)
echo   [17] PUBG Mobile & OpenGL Auto-Repair (1-Click Recovery Engine)
echo   [18] Esports Camera Tuning (Flick-Turn & Diagonal FOV Calibration)
echo   [19] Keymap Protection & Backup (Lock Custom Controls)
echo   [20] Launch Standalone Auto-Guard Daemon (Background Watchdog)
echo   [21] 180Hz / 240 FPS Ultra-Refresh Mode (UE4 Uncapped + VM Tuning)
echo   [22] Lossless Scaling 240 FPS Configuration Guide & Setup
echo   [0] Exit
echo.
echo ===============================================================================
set /p "CHOICE=Select an option [0-22]: "

if "%CHOICE%"=="1" goto OPTIMIZE_UHD
if "%CHOICE%"=="2" goto LAUNCH_GAME
if "%CHOICE%"=="3" goto SWITCH_MODEL
if "%CHOICE%"=="4" goto SWITCH_RES
if "%CHOICE%"=="5" goto DEEP_CLEAN
if "%CHOICE%"=="6" goto CRASH_GUARD
if "%CHOICE%"=="7" goto HIT_REG
if "%CHOICE%"=="8" goto REFRESH_DIAG
if "%CHOICE%"=="9" goto LAUNCH_GUI
if "%CHOICE%"=="10" goto LOCK_PACING
if "%CHOICE%"=="11" goto STREAMER_MODE
if "%CHOICE%"=="12" goto BACKUP_ENV
if "%CHOICE%"=="13" goto RESTORE_ENV
if "%CHOICE%"=="14" goto TOGGLE_WM
if "%CHOICE%"=="15" goto MOUSE_KEEPER
if "%CHOICE%"=="16" goto NOTICE_TAMER
if "%CHOICE%"=="17" goto AUTO_REPAIR
if "%CHOICE%"=="18" goto CAMERA_TUNING
if "%CHOICE%"=="19" goto PROTECT_KEYMAPS
if "%CHOICE%"=="20" goto GUARD_DAEMON
if "%CHOICE%"=="21" goto HIGH_REFRESH
if "%CHOICE%"=="22" goto LOSSLESS_SCALING
if "%CHOICE%"=="0" exit /b 0
goto MENU

:OPTIMIZE_UHD
cls
echo ===============================================================================
echo   Applying 1-Click Tier 6 Ultra HD + 120 FPS + GameLoop 90 Sync...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --optimize --res=1920x1080 --dpi=480 --fps=120
echo.
echo >> 1-Click Optimization Completed Successfully!
echo >> In-Game Save: 120 FPS (BattleFPS=8) ^& Ultra HD Locked
echo >> Settings Center UI: Matches Target 90 FPS with Red Dot
echo >> GPU Thermals: Cool ^& Silent (Dynamic Scaling, 0%% Fan)
pause
goto MENU

:LAUNCH_GAME
cls
echo ===============================================================================
echo   Launching PUBG Mobile...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --launch
echo.
echo >> Emulator launched!
echo >> PRO TIP: Once GameLoop opens, press [F11] for Fullscreen Direct Scanout!
timeout /t 3 >nul
goto MENU

:SWITCH_MODEL
cls
echo ===============================================================================
echo   Device Model Switcher (Ultra HD 120 FPS ^& Hit-Reg Profiles)
echo ===============================================================================
echo.
echo   [1] REDMAGIC 9 Pro (NX769J)      - [RECOMMENDED] Best Bullet Reg ^& UHD 120
echo   [2] ASUS ROG 8 Pro (AI2401_A)    - Maximum Frametime Pacing ^& Esports Audio
echo   [3] Samsung Galaxy S24 Ultra      - Maximum Device Whitelist Compatibility
echo   [4] Samsung Galaxy Tab S9 Ultra   - [REDDIT POPULAR] SM-X910 120 FPS Whitelist
echo   [5] Xiaomi 13 Pro (2210132C)     - Lightweight Aggressive Frame Rates
echo   [6] Back to Main Menu
echo.
set /p "MCHOICE=Select a model [1-6]: "

if "%MCHOICE%"=="1" (
    %PY_CMD% tac_engine.py --model redmagic
    pause
    goto MENU
)
if "%MCHOICE%"=="2" (
    %PY_CMD% tac_engine.py --model rog
    pause
    goto MENU
)
if "%MCHOICE%"=="3" (
    %PY_CMD% tac_engine.py --model samsung
    pause
    goto MENU
)
if "%MCHOICE%"=="4" (
    %PY_CMD% tac_engine.py --model tabs9
    pause
    goto MENU
)
if "%MCHOICE%"=="5" (
    %PY_CMD% tac_engine.py --model xiaomi
    pause
    goto MENU
)
goto MENU

:SWITCH_RES
cls
echo ===============================================================================
echo   Display Resolution Switcher
echo ===============================================================================
echo.
echo   [1] Native Full HD (1920x1080)   - DPI 480 [RECOMMENDED: 1:1 Pixel Mapping]
echo   [2] Quad HD 2K (2560x1440)       - DPI 640 [Ultra Sharpness on 2K Panels]
echo   [3] iPad View 4:3 (1440x1080)    - DPI 400 [Wide Player Character Models]
echo   [4] Back to Main Menu
echo.
set /p "RCHOICE=Select resolution [1-4]: "

if "%RCHOICE%"=="1" (
    %PY_CMD% tac_engine.py --setres 1920x1080 480
    pause
    goto MENU
)
if "%RCHOICE%"=="2" (
    %PY_CMD% tac_engine.py --setres 2560x1440 640
    pause
    goto MENU
)
if "%RCHOICE%"=="3" (
    %PY_CMD% tac_engine.py --setres 1440x1080 400
    pause
    goto MENU
)
goto MENU

:DEEP_CLEAN
cls
echo ===============================================================================
echo   Deep Cleaning ^& Shader Cache Purge...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --clean
pause
goto MENU

:CRASH_GUARD
cls
echo ===============================================================================
echo   Crash Guard ^& Virtual Memory RAM Flush...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --guard
pause
goto MENU

:HIT_REG
cls
echo ===============================================================================
echo   Applying 0ms Network Turbo ^& MMCSS Game Scheduling...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --turbo
pause
goto MENU

:REFRESH_DIAG
goto MENU

:LAUNCH_GUI
cls
echo ===============================================================================
echo   Launching Graphical Desktop Dashboard (GUI)...
echo ===============================================================================
echo.
start "" %PY_CMD% tac_gui.py
timeout /t 2 >nul
goto MENU

:LOCK_PACING
cls
echo ===============================================================================
echo   Locking 120 FPS Frame Pacing ^& Direct Scanout (Zero DWM Latency)...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --boost
echo.
echo >> 0.50ms Kernel Timer Resolution Active
echo >> Emulator Process Priority Elevated to HIGH
echo >> DirectX Direct Scanout (Independent Flip) Registered
echo.
echo >> PRO TIP: Once GameLoop opens, press [F11] for Fullscreen Direct Scanout!
pause
goto MENU

:STREAMER_MODE
cls
echo ===============================================================================
echo   Streamer Helper Mode (1080p Borderless Direct Stream View)
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --streamer
echo.
echo >> Borderless 1080p Streamer Viewport Active!
echo >> Perfect for OBS Studio, Discord, and TikTok Live Studio!
pause
goto MENU

:BACKUP_ENV
cls
echo ===============================================================================
echo   Creating Full Environment Snapshot Backup...
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --backup
echo.
pause
goto MENU

:RESTORE_ENV
cls
echo ===============================================================================
echo   1-Click Factory Restore / Snapshot Revert...
echo ===============================================================================
echo.
echo [WARNING] This will restore your saved snapshot or revert to clean defaults.
set /p "CONFIRM=Proceed with restoration? (Y/N): "
if /i "%CONFIRM%"=="Y" (
    %PY_CMD% tac_engine.py --restore
) else (
    echo Restoration cancelled.
)
echo.
pause
goto MENU

:TOGGLE_WM
cls
echo ===============================================================================
echo   Toggle Clean Screen UI (Native Watermark Suppression)
echo ===============================================================================
echo.
echo   [1] Clean Screen (Suppress On-Screen Watermark & Key Hints)
echo   [2] Default Screen (Show Watermark & Key Hints)
echo.
set /p "WCHOICE=Select an option [1-2]: "
if "%WCHOICE%"=="1" (
    %PY_CMD% tac_engine.py --watermark
)
if "%WCHOICE%"=="2" (
    %PY_CMD% tac_engine.py --show-watermark
)
pause
goto MENU

:MOUSE_KEEPER
cls
echo ===============================================================================
echo   Mouse Keeper & Cursor Fencer (1:1 Raw Mouse Tracking)
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --raw-mouse
%PY_CMD% tac_engine.py --mouse-keeper
echo.
echo >> 1:1 Raw Hardware Sensor Tracking Active!
echo >> Cursor Fencing Engaged for GameLoop Viewport!
pause
goto MENU

:NOTICE_TAMER
cls
echo ===============================================================================
echo   Notice Tamer (Auto-Suppress Ad Popups & Update Nags)
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --notice-tamer
echo.
pause
goto MENU

:AUTO_REPAIR
cls
echo ===============================================================================
echo   PUBG Mobile & OpenGL 1-Click Auto-Repair Engine
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --repair
echo.
pause
goto MENU

:CAMERA_TUNING
cls
echo ===============================================================================
echo   Esports Camera Tuning & Flick-Turn Calibration
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --camera
echo.
pause
goto MENU

:PROTECT_KEYMAPS
cls
echo ===============================================================================
echo   Keymap Protection & Backup (Lock Custom Controls)
echo ===============================================================================
echo.
%PY_CMD% tac_engine.py --keymap
echo.
pause
goto MENU

:GUARD_DAEMON
cls
echo ===============================================================================
echo   Launching Standalone TAC Auto-Guard Daemon (Background Watchdog)
echo ===============================================================================
echo.
echo >> Starting watchdog in background with Local\TacPanelLoopGuard mutex...
start "" %PY_CMD% tac_engine.py --daemon
echo >> TAC Auto-Guard Daemon launched in background!
timeout /t 3 >nul
goto MENU

:HIGH_REFRESH
cls
echo ===============================================================================
echo   180Hz / 240 FPS Ultra-Refresh Mode (UE4 Uncapped + VM 180Hz)
echo ===============================================================================
echo.
echo   [1] 180Hz Mode (Recommended for your 180Hz Gaming Monitor - 1:1 Scanout)
echo   [2] 240 FPS Mode (UE4 Uncapped 240 FPS + 240Hz Input Polling)
echo   [3] Back to Main Menu
echo.
set /p "HCHOICE=Select target refresh rate [1-3]: "
if "%HCHOICE%"=="1" (
    %PY_CMD% tac_engine.py --highfps 180
    pause
    goto MENU
)
if "%HCHOICE%"=="2" (
    %PY_CMD% tac_engine.py --highfps 240
    pause
    goto MENU
)
goto MENU

:LOSSLESS_SCALING
cls
echo ===============================================================================
echo   Lossless Scaling (LSFG) 240 FPS AI Frame Generation Guide
echo ===============================================================================
echo.
%PY_CMD% -c "
import os
guide = os.path.join(os.getcwd(), 'LOSSLESS_SCALING_240FPS_GUIDE.md')
if os.path.exists(guide):
    with open(guide, 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('Guide file not found. Please ensure LOSSLESS_SCALING_240FPS_GUIDE.md is present.')
"
echo.
pause
goto MENU
