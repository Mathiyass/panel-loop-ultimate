r"""
===============================================================================
NVIDIA APP & RTX 3090 GAMELOOP INTEGRATION ENGINE
===============================================================================
Configures:
1. Windows Graphics Performance: Forces RTX 3090 Dedicated GPU (GpuPreference=2)
   for aow_exe.exe, AndroidEmulatorEx.exe, and AndroidEmulator.exe.
2. DWM Direct Scanout: Injects Independent Flip flags to eliminate desktop compositing lag.
3. Automatically sets Windows Clipboard to 'C:\Program Files\TxGameAssistant\ui\aow_exe.exe'.
4. Highlights the executable in Windows Explorer.
5. Displays optimal NVIDIA App driver tuning parameters for 180Hz / RTX 3090 esports.
===============================================================================
"""

import os
import sys
import winreg
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TARGET_EXECUTABLES = [
    r"C:\Program Files\TxGameAssistant\ui\aow_exe.exe",
    r"C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe",
    r"C:\Program Files\TxGameAssistant\ui\AndroidEmulator.exe",
    r"C:\Program Files\TxGameAssistant\ui\AndroidRenderer.exe",
    r"C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe"
]

PRIMARY_3D_EXE = r"C:\Program Files\TxGameAssistant\ui\aow_exe.exe"
PRIMARY_SHELL_EXE = r"C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe"

def log(msg, level="INFO"):
    p = {"INFO": "[*]", "SUCCESS": "[+]", "WARN": "[!]", "ERROR": "[-]"}.get(level, "[*]")
    print(f"{p} {msg}")

def configure_windows_gpu_preferences():
    log("=== STEP 1: CONFIGURING WINDOWS USER GPU PREFERENCES (RTX 3090) ===", "INFO")
    key_path = r"Software\Microsoft\DirectX\UserGpuPreferences"
    try:
        k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(k, "DirectXUserGlobalSettings", 0, winreg.REG_SZ, "GpuPreference=2;")
        
        for exe_path in TARGET_EXECUTABLES:
            if os.path.exists(exe_path):
                winreg.SetValueEx(k, exe_path, 0, winreg.REG_SZ, "GpuPreference=2;")
                log(f"Locked GpuPreference=2 (High Performance RTX 3090) for: {os.path.basename(exe_path)}", "SUCCESS")
        winreg.CloseKey(k)
    except Exception as e:
        log(f"Error setting UserGpuPreferences: {e}", "ERROR")

def configure_dwm_direct_scanout():
    log("=== STEP 2: ENFORCING DWM DIRECT SCANOUT (INDEPENDENT FLIP) ===", "INFO")
    key_path = r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
    flags = "~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE"
    try:
        k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        for exe_path in TARGET_EXECUTABLES[:3]:
            if os.path.exists(exe_path):
                winreg.SetValueEx(k, exe_path, 0, winreg.REG_SZ, flags)
                log(f"Injected Direct Scanout flags for: {os.path.basename(exe_path)}", "SUCCESS")
        winreg.CloseKey(k)
    except Exception as e:
        log(f"Error setting AppCompatFlags: {e}", "ERROR")

def set_clipboard(text):
    try:
        cmd = f"Set-Clipboard -Value '{text}'"
        subprocess.run(["powershell", "-NoProfile", "-Command", cmd], check=True)
        log(f"Copied primary 3D executable path to clipboard: {text}", "SUCCESS")
        return True
    except Exception as e:
        log(f"Could not set clipboard: {e}", "WARN")
        return False

def highlight_in_explorer(file_path):
    if os.path.exists(file_path):
        try:
            subprocess.Popen(["explorer.exe", f"/select,{file_path}"])
            log(f"Opened Explorer with {os.path.basename(file_path)} highlighted.", "SUCCESS")
        except Exception as e:
            log(f"Could not open Explorer: {e}", "WARN")

def print_nvidia_app_instructions():
    guide = r"""
===============================================================================
        NVIDIA APP CONFIGURATION GUIDE (PROGRAM SETTINGS)
===============================================================================

In your NVIDIA App window (currently open under 'Graphics' -> 'Program Settings'):

1. CLICK 'ADD A PROGRAM' (or the 3-dots menu -> 'Add a program'):
   - When the file picker opens, the path to the 3D game engine is already copied
     to your clipboard:
     C:\Program Files\TxGameAssistant\ui\aow_exe.exe
   - In the 'File name' box of the file picker, press Ctrl+V and click Open.
   - Also repeat to add the emulator launcher:
     C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe

2. CONFIGURE DRIVER SETTINGS FOR BOTH IN NVIDIA APP:
   ┌──────────────────────────────────────────────┬────────────────────────────┐
   │ Setting Name                                 │ Optimal Value              │
   ├──────────────────────────────────────────────┼────────────────────────────┤
   │ Power management mode                        │ Prefer maximum performance │
   │ Low Latency Mode                             │ Ultra                      │
   │ Max Frame Rate                               │ Off (or 180 FPS)           │
   │ Threaded optimization                        │ On                         │
   │ Texture filtering - Quality                  │ High performance           │
   │ Texture filtering - Anisotropic optimization │ On                         │
   │ Texture filtering - Negative LOD bias        │ Allow                      │
   │ Vulkan/OpenGL present method                 │ Prefer layered on DXGI     │
   └──────────────────────────────────────────────┴────────────────────────────┘

3. CLICK SAVE / APPLY:
   - Your NVIDIA RTX 3090 will now lock to maximum clocks and enforce sub-frame
     rendering whenever GameLoop or PUBG Mobile is running!

===============================================================================
"""
    print(guide)

def main():
    print("===============================================================================")
    print("          NVIDIA APP & RTX 3090 GAMELOOP OPTIMIZATION SUITE                    ")
    print("===============================================================================")
    configure_windows_gpu_preferences()
    configure_dwm_direct_scanout()
    set_clipboard(PRIMARY_3D_EXE)
    highlight_in_explorer(PRIMARY_3D_EXE)
    print_nvidia_app_instructions()

if __name__ == "__main__":
    main()
