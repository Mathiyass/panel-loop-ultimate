@echo off
title PUBG Mobile 120 FPS & GameLoop Max Optimizer
echo ========================================================
echo   PUBG Mobile 120 FPS & GameLoop Max Optimizer
echo ========================================================
echo.

echo [1/3] Applying Engine & Registry Optimizations...
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMPhoneDevice" /t REG_SZ /d "Asus ROG 8 Pro" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceModel" /t REG_SZ /d "ASUS_AI2401_A" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "VMDeviceManufacturer" /t REG_SZ /d "asus" /f >nul
reg add "HKCU\Software\Tencent\MobileGamePC" /v "com.tencent.ig_FPSLevel" /t REG_DWORD /d 120 /f >nul
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
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AndroidEmulatorEx.exe\PerfOptions" /v "CpuPriorityClass" /t REG_DWORD /d 3 /f >nul 2>&1

echo [2/3] Deploying 120 FPS Active.sav to GameLoop filesystem...
if exist "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" (
    copy /Y "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" "C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1945" >nul 2>&1
    copy /Y "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" "C:\Program Files\TxGameAssistant\AOW_Rootfs_100\9\24c8" >nul 2>&1
)

echo [3/3] Checking if ADB emulator is connected...
if exist "C:\Program Files\TxGameAssistant\ui\adb.exe" (
    "C:\Program Files\TxGameAssistant\ui\adb.exe" devices | findstr "emulator" >nul 2>&1
    if not errorlevel 1 (
        echo ADB emulator found. Pushing directly to PUBG Mobile directory...
        "C:\Program Files\TxGameAssistant\ui\adb.exe" push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav
        "C:\Program Files\TxGameAssistant\ui\adb.exe" push "C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav" /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/SettingConfig_Slot.sav
        "C:\Program Files\TxGameAssistant\ui\adb.exe" shell chmod 777 /sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved/SaveGames/Active.sav
        echo Deployed to running game container successfully!
    ) else (
        echo Emulator is not currently active via ADB. Rootfs files deployed directly to disk.
    )
)

echo.
echo ========================================================
echo   OPTIMIZATION & 120 FPS COMPLETE!
echo   Launch PUBG Mobile and select Graphics -> Smooth + 120 FPS (Ultra Extreme).
echo ========================================================
timeout /t 5
