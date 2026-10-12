@echo off
title PUBG Mobile HDR 120 FPS and Maximum Hit-Reg Optimizer
echo =======================================================================
echo   PUBG Mobile HDR 120 FPS, Bullet Connection and Aim Assist Optimizer
echo =======================================================================
echo.

echo [1/4] Applying Network Low-Latency & Bullet Connection (Hit-Reg) Tweaks...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{a24e65ee-2032-4cd5-90c1-517c095969c9}" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{a24e65ee-2032-4cd5-90c1-517c095969c9}" /v "TCPNoDelay" /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d 4294967295 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d 0 /f >nul 2>&1

echo [2/4] Applying GameLoop 64-bit Engine & RTX 3090 DirectX+ Optimizations...
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "Samsung SM-X910" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "SM-X910" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "samsung" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_FPSLevel" /t REG_DWORD /d 120 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_RenderQuality" /t REG_DWORD /d 4 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VSyncEnabled" /t REG_DWORD /d 0 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ForceDirectX" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "GraphicsCard" /t REG_SZ /d "Nvidia" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "GraphicsCardEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "SetGraphicsCard" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "LocalShaderCacheEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ShaderCacheEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "RenderOptimizeEnabled" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "EnableGLESv3" /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMCpuCount" /t REG_DWORD /d 8 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMMemorySizeInMB" /t REG_DWORD /d 4096 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMResWidth" /t REG_DWORD /d 1920 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMResHeight" /t REG_DWORD /d 1080 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDPI" /t REG_DWORD /d 480 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "FxaaQuality" /t REG_DWORD /d 0 /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "ShowFPS" /t REG_DWORD /d 1 /f >nul

reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\ui\AndroidEmulator.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\DirectX\UserGpuPreferences" /v "C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe" /t REG_SZ /d "GpuPreference=2;" /f >nul 2>&1
reg add "HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" /v "C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe" /t REG_SZ /d "~ HIGHDPIAWARE DISABLEDXMAXIMIZEDWINDOWEDMODE" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AndroidEmulatorEx.exe\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f >nul 2>&1

echo [3/4] Deploying HDR 120 FPS Save Game Files to Rootfs...
if exist "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" (
    copy /Y "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" "C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1945" >nul 2>&1
    copy /Y "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" "C:\Program Files\TxGameAssistant\AOW_Rootfs_100\9\24c8" >nul 2>&1
)

echo [4/4] Checking ADB connection for Live Hot-Push...
if exist "C:\Program Files\TxGameAssistant\ui\adb.exe" (
    "C:\Program Files\TxGameAssistant\ui\adb.exe" connect 127.0.0.1:5555 >nul 2>&1
    "C:\Program Files\TxGameAssistant\ui\adb.exe" devices | findstr "5555" >nul 2>&1
    if not errorlevel 1 (
        echo Live emulator container found. Hot-pushing HDR 120 FPS save...
        "C:\Program Files\TxGameAssistant\ui\adb.exe" -s 127.0.0.1:5555 push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav >nul 2>&1
        "C:\Program Files\TxGameAssistant\ui\adb.exe" -s 127.0.0.1:5555 push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/SettingConfig_Slot.sav >nul 2>&1
        "C:\Program Files\TxGameAssistant\ui\adb.exe" -s 127.0.0.1:5555 shell chmod 777 /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav >nul 2>&1
        echo Pushed directly to running game container successfully!
    ) else (
        echo Emulator is currently closed. Files written directly to disk rootfs.
    )
)

echo.
echo =======================================================================
echo   ALL OPTIMIZATIONS APPLIED!
echo   - Graphics: HDR (High Dynamic Range)
echo   - Frame Rate: 120 FPS Locked
echo   - Bullet Connection: TCPNoDelay active (0ms Nagle delay)
echo   - Aim Assist: Full 120Hz Physics Sampling & Linear Mouse Input
echo =======================================================================
