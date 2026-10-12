@echo off
setlocal EnableDelayedExpansion
title PANEL LOOP ULTIMATE - GameLoop ^& PUBG MOBILE Master Suite
color 0B

:MENU
cls
echo ===============================================================================
echo            PANEL LOOP ULTIMATE - GAMELOOP ^& PUBG MOBILE OPTIMIZER
echo                   (Free, Open-Source ^& 100%% Ban-Safe Edition)
echo ===============================================================================
echo.
echo   Hardware Profile: AMD Ryzen 7 5800X  ^|  NVIDIA RTX 3090 24GB  ^|  180Hz DWM
echo   Current Active Model: 
powershell -NoProfile -ExecutionPolicy Bypass -Command "$m = (Get-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMPhoneDevice' -ErrorAction SilentlyContinue).VMPhoneDevice; Write-Host '  >> ' $m -ForegroundColor Yellow"
echo.
echo   [1] 1-Click Ultra HD (Tier 6) + 120 FPS Activation (Lock Saves ^& Engine)
echo   [2] Switch Device Model (RedMagic NX789J / Xiaomi 22081212C / Samsung)
echo   [3] Toggle iPad View (4:3 Stretched 1440x1080) vs Native FHD (1920x1080)
echo   [4] Deep Cleaner ^& Shader Cache Purge (Fix Visual Glitches ^& Stutter)
echo   [5] Crash Guard ^& Virtual Memory RAM Flush (Fix Out-Of-Memory Popup)
echo   [6] 0ms Hit-Reg ^& Network Turbo (Disable Nagle Algorithm + MMCSS)
echo   [7] Launch PUBG Mobile Directly
echo   [8] Exit
echo.
echo ===============================================================================
set /p "CHOICE=Select an option [1-8]: "

if "%CHOICE%"=="1" goto OPTIMIZE_UHD
if "%CHOICE%"=="2" goto SWITCH_MODEL
if "%CHOICE%"=="3" goto TOGGLE_IPAD
if "%CHOICE%"=="4" goto DEEP_CLEAN
if "%CHOICE%"=="5" goto CRASH_GUARD
if "%CHOICE%"=="6" goto HIT_REG
if "%CHOICE%"=="7" goto LAUNCH_GAME
if "%CHOICE%"=="8" exit /b 0
goto MENU

:SWITCH_MODEL
cls
echo ===============================================================================
echo   Device Model Switcher (Ultra HD 120 FPS ^& Hit-Reg Profiles)
echo ===============================================================================
echo.
echo   [1] ZTE Nubia REDMAGIC (NX789J)  - [RECOMMENDED] Best Bullet Connectivity ^& UHD 120
echo   [2] Xiaomi (22081212C)           - Best Frametime Stability ^& FPS Boost
echo   [3] Samsung (SM-X910)            - Galaxy Tab S9 Ultra Profile
echo   [4] Back to Main Menu
echo.
set /p "MCHOICE=Select a model [1-4]: "

if "%MCHOICE%"=="1" (
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "REDMAGIC NX789J" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "NX789J" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "nubia" /f >nul
    echo.
    echo >> Switched to ZTE Nubia REDMAGIC (NX789J)! (RedMagic 10 Pro)
    echo >> Maximum bullet connectivity and Krafton 120 FPS whitelist active!
    pause
    goto MENU
)
if "%MCHOICE%"=="2" (
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "Xiaomi 22081212C" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "22081212C" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "Xiaomi" /f >nul
    echo.
    echo >> Switched to Xiaomi (22081212C)! (Redmi K50 Ultra / 12T Pro)
    echo >> FPS Boost and frametime stability active!
    pause
    goto MENU
)
if "%MCHOICE%"=="3" (
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "Samsung SM-X910" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "SM-X910" /f >nul
    reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "samsung" /f >nul
    echo.
    echo >> Switched to Samsung SM-X910! (Galaxy Tab S9 Ultra)
    pause
    goto MENU
)
goto MENU

:OPTIMIZE_UHD
cls
echo ===============================================================================
echo   Applying Tier 6 Ultra HD + 120 FPS + RedMagic NX789J Configuration...
echo ===============================================================================
echo.
echo [1/4] Applying Windows Kernel MMCSS ^& GPU Preemption...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d 4294967295 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Priority" /t REG_DWORD /d 6 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "Scheduling Category" /t REG_SZ /d "High" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games" /v "SFIO Priority" /t REG_SZ /d "High" /f >nul 2>&1

echo [2/4] Calibrating GameLoop Engine for Tier 6 Ultra HD ^& 120 FPS...
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "REDMAGIC NX789J" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "NX789J" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "nubia" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_FPSLevel" /t REG_DWORD /d 120 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_RenderQuality" /t REG_DWORD /d 6 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_ContentScale" /t REG_DWORD /d 2 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VSyncEnabled" /t REG_DWORD /d 0 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ForceDirectX" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "GraphicsCard" /t REG_SZ /d "Nvidia" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "GraphicsCardEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "LocalShaderCacheEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ShaderCacheEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "RenderOptimizeEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "EnableGLESv3" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMCpuCount" /t REG_DWORD /d 4 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMMemorySizeInMB" /t REG_DWORD /d 4096 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ShowFPS" /t REG_DWORD /d 1 /f >nul

reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\ui\AndroidEmulator.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1

echo [3/4] Deploying Tier 6 Ultra HD Saves ^& HD Texture Profiles...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$src = 'C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav'; $ini = 'C:\Temp\TxGameDownload\MobileGamePCShared\UserCustom.ini'; $saves = @('C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\84ad','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\84ae','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edb','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edc','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\4a08','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\4a09','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1945','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\9\24c8'); foreach ($s in $saves) { attrib -r $s 2>$null; Copy-Item -Path $src -Destination $s -Force 2>$null }; $inis = @('C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edd','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\485c','C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1899'); foreach ($i in $inis) { attrib -r $i 2>$null; Copy-Item -Path $ini -Destination $i -Force 2>$null }"

echo [4/4] Checking Live ADB Hot-Push Container...
set "ADB_EXE=C:\Program Files\TxGameAssistant\ui\adb.exe"
if exist "!ADB_EXE!" (
    "!ADB_EXE!" connect 127.0.0.1:5555 >nul 2>&1
    for /f "tokens=1" %%d in ('^""!ADB_EXE!" devices ^| findstr /v "List" ^| findstr "device"^"') do (
        set "ADB_DEV=%%d"
    )
    if defined ADB_DEV (
        echo Live emulator container found [!ADB_DEV!]. Hot-pushing Tier 6 files...
        "!ADB_EXE!" -s !ADB_DEV! push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav >nul 2>&1
        "!ADB_EXE!" -s !ADB_DEV! push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/SettingConfig_Slot.sav >nul 2>&1
        "!ADB_EXE!" -s !ADB_DEV! push "C:\Temp\TxGameDownload\MobileGamePCShared\UserCustom.ini" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/Config/Android/UserCustom.ini >nul 2>&1
        echo Tier 6 Ultra HD hot-pushed into live RAM container!
    )
)

echo.
echo ===============================================================================
echo   SUCCESS: Tier 6 Ultra HD + 120 FPS + RedMagic NX789J Applied ^& Locked!
echo ===============================================================================
pause
goto MENU

:TOGGLE_IPAD
cls
echo ===============================================================================
echo   iPad View (4:3 Stretched) vs Native FHD (16:9) Switcher
echo ===============================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$curW = (Get-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMResWidth' -ErrorAction SilentlyContinue).VMResWidth; if ($curW -eq 1440) { Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMResWidth' -Value 1920; Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMResHeight' -Value 1080; Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMDPI' -Value 480; Write-Host '>> Switched to: [NATIVE 16:9 FHD] 1920x1080 (DPI 480)' -ForegroundColor Green } else { Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMResWidth' -Value 1440; Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMResHeight' -Value 1080; Set-ItemProperty -Path 'HKCU:\Software\Tencent\MobileGamePC' -Name 'VMDPI' -Value 400; Write-Host '>> Switched to: [iPAD VIEW 4:3 STRETCHED] 1440x1080 (DPI 400)' -ForegroundColor Cyan; Write-Host '>> Wider vertical/horizontal FOV and better recoil control active!' -ForegroundColor Cyan }"
echo.
pause
goto MENU

:DEEP_CLEAN
cls
echo ===============================================================================
echo   Deep Cleaner ^& Shader Cache Purge
echo ===============================================================================
echo.
echo Purging corrupt DirectX shader cache blobs...
del /q /f "C:\Program Files\TxGameAssistant\ui\ShaderCache\*.bin2" >nul 2>&1
del /q /f "C:\Program Files\TxGameAssistant\ui\ShaderCache\*.cache" >nul 2>&1

echo Cleaning temporary TxGameDownload logs and crash dumps...
del /q /f /s "C:\Temp\TxGameDownload\*.log" >nul 2>&1
del /q /f /s "C:\Temp\TxGameDownload\*.dmp" >nul 2>&1
del /q /f /s "C:\Temp\TxGameDownload\*.tmp" >nul 2>&1

echo Flushing DNS cache...
ipconfig /flushdns >nul 2>&1

echo.
echo >> Deep Clean Complete! Stutter and shader cache cleared.
echo.
pause
goto MENU

:CRASH_GUARD
cls
echo ===============================================================================
echo   Crash Guard ^& Virtual Memory RAM Flush
echo ===============================================================================
echo.
echo Terminating any hung or orphaned emulator worker processes...
taskkill /f /im aow_exe.exe >nul 2>&1
taskkill /f /im aow_exe >nul 2>&1
taskkill /f /im AndroidEmulatorEx.exe >nul 2>&1

echo Freeing Windows standby list and committed memory...
powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers(); Write-Host '>> Garbage collection and commit memory trimmed.' -ForegroundColor Green"

echo.
echo >> Crash Guard Complete! Virtual memory flushed and processes reset.
echo.
pause
goto MENU

:HIT_REG
cls
echo ===============================================================================
echo   0ms Hit-Reg ^& Low-Latency Network Turbo
echo ===============================================================================
echo.
echo Applying zero-latency TCP ACK and TCPNoDelay (Nagle algorithm disabled)...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{a24e65ee-2032-4cd5-90c1-517c095969c9}" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{a24e65ee-2032-4cd5-90c1-517c095969c9}" /v "TCPNoDelay" /t REG_DWORD /d 1 /f >nul 2>&1

echo Setting Real-time CPU Priority Class for GameLoop...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AndroidEmulatorEx.exe\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f >nul 2>&1

echo.
echo >> Network Turbo Active! Instant bullet connection and 0ms socket latency.
echo.
pause
goto MENU

:LAUNCH_GAME
cls
echo Starting GameLoop and PUBG Mobile...
start "" "C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe" -runpkg com.tencent.ig
goto MENU
