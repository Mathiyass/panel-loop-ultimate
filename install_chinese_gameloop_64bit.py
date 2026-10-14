r"""
===============================================================================
GameLoop Chinese 64-Bit (TGB) Automated Installer & Optimizer
Based on YouTube Guide: https://www.youtube.com/watch?v=ftez-K9Xu1M (TDR DADDY)
===============================================================================
Features:
1. Verifies/downloads authentic GameLoop Chinese 64-Bit package (1000224174).
2. Initializes host shared staging folders (C:\Temp\TxGameDownload\MobileGamePCShared).
3. Launches installer with elevated permissions.
4. Detects installation paths and applies English UI translation patch (AndroidEmulatorEn.exe).
5. Creates Desktop shortcut with '-vm 100' parameter.
6. Guides the user through in-emulator setup (QQ engine bootstrap, F9 English Android OS, APK install).
"""

import os
import sys
import time
import shutil
import subprocess
import winreg
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import win32com.client
except ImportError:
    win32com = None

INSTALLER_URL = "https://www.dropbox.com/scl/fi/72wgkl8iycjxf1cj5hkgs/Gameloop-Chinese-64-pc-androidemulator.com-1000224174.exe?rlkey=9rn4398dsjgjiop73x9zj5vak&st=edk6xqnz&dl=1"
DOWNLOADS_DIR = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\MATHIYA"), "Downloads")
INSTALLER_PATH = os.path.join(DOWNLOADS_DIR, "Gameloop-Chinese-64-1000224174.exe")

SHARED_DIRS = [
    r"C:\Temp\TxGameDownload\MobileGamePCShared",
    r"D:\Temp\TxGameDownload\MobileGamePCShared",
    os.path.expandvars(r"%TEMP%\TxGameDownload\MobileGamePCShared")
]

SEARCH_UI_DIRS = [
    r"C:\TxGameAssistant\UI",
    r"C:\Program Files\TxGameAssistant\UI",
    r"C:\Program Files (x86)\TxGameAssistant\UI",
    r"D:\TxGameAssistant\UI",
    r"C:\Program Files\Tencent\GameLoop\UI",
    r"D:\Program Files\TxGameAssistant\UI"
]

def log(msg, level="INFO"):
    prefixes = {
        "INFO": "[*]",
        "SUCCESS": "[+]",
        "WARN": "[!]",
        "ERROR": "[-]"
    }
    p = prefixes.get(level, "[*]")
    print(f"{p} {msg}")

def ensure_installer_downloaded():
    log("Checking GameLoop Chinese 64-Bit installer...", "INFO")
    if os.path.exists(INSTALLER_PATH) and os.path.getsize(INSTALLER_PATH) > 1000000:
        log(f"Installer already present: {INSTALLER_PATH} ({os.path.getsize(INSTALLER_PATH)} bytes)", "SUCCESS")
        return INSTALLER_PATH

    log("Downloading Chinese 64-Bit GameLoop installer from mirror...", "INFO")
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    r = requests.get(INSTALLER_URL, stream=True, timeout=30)
    r.raise_for_status()

    total_bytes = 0
    with open(INSTALLER_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
                total_bytes += len(chunk)

    log(f"Downloaded {total_bytes / (1024*1024):.2f} MB to {INSTALLER_PATH}", "SUCCESS")
    with open(INSTALLER_PATH, "rb") as f:
        if f.read(2) == b"MZ":
            log("Verified valid Windows executable binary.", "SUCCESS")
        else:
            log("Warning: Binary header did not match MZ signature.", "WARN")
    return INSTALLER_PATH

def setup_shared_directories():
    log("Setting up host shared directories (MobileGamePCShared)...", "INFO")
    for d in SHARED_DIRS:
        try:
            os.makedirs(d, exist_ok=True)
            log(f"Created/verified shared folder: {d}", "SUCCESS")
        except Exception as e:
            log(f"Failed to create {d}: {e}", "WARN")

def find_installed_ui_dir():
    # 1. Check registry first
    reg_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\MobileGamePC\UI"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\MobileGamePC\UI"),
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent\MobileGamePC\UI"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\TxGameAssistant"),
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent\TxGameAssistant"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\GameLoop"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\GameLoop")
    ]
    for hive, subkey in reg_keys:
        try:
            k = winreg.OpenKey(hive, subkey)
            val, _ = winreg.QueryValueEx(k, "InstallPath")
            winreg.CloseKey(k)
            ui_path = os.path.join(val, "UI") if not val.lower().endswith("ui") else val
            if os.path.exists(ui_path):
                return ui_path
        except Exception:
            pass

    # 2. Check filesystem candidate paths
    for p in SEARCH_UI_DIRS:
        if os.path.exists(p) and (
            os.path.exists(os.path.join(p, "AndroidEmulator.exe")) or 
            os.path.exists(os.path.join(p, "AndroidEmulatorEn.exe"))
        ):
            return p
            
    # 3. Check recursively in common root drives
    for root in [r"C:\TxGameAssistant", r"D:\TxGameAssistant"]:
        ui = os.path.join(root, "UI")
        if os.path.exists(ui):
            return ui

    return None

def apply_english_ui_patch(ui_dir):
    log(f"Applying English UI Localization patch in: {ui_dir}", "INFO")
    cn_exe = os.path.join(ui_dir, "AndroidEmulator.exe")
    en_exe = os.path.join(ui_dir, "AndroidEmulatorEn.exe")
    backup_cn = os.path.join(ui_dir, "AndroidEmulator_CN_Backup.exe")

    if not os.path.exists(en_exe):
        log(f"AndroidEmulatorEn.exe not found in {ui_dir}. Skipping binary swap.", "WARN")
        return False

    try:
        # Backup Chinese executable if not already backed up
        if os.path.exists(cn_exe) and not os.path.exists(backup_cn):
            shutil.copy2(cn_exe, backup_cn)
            log(f"Backed up Chinese emulator shell to: {backup_cn}", "SUCCESS")

        # Copy AndroidEmulatorEn.exe over AndroidEmulator.exe
        shutil.copy2(en_exe, cn_exe)
        log("Successfully swapped AndroidEmulatorEn.exe -> AndroidEmulator.exe! UI is now English.", "SUCCESS")
        return True
    except Exception as e:
        log(f"Failed to swap emulator executables: {e}", "ERROR")
        return False

def create_vm100_desktop_shortcut(ui_dir):
    log("Creating Desktop Shortcut with '-vm 100' argument...", "INFO")
    desktop_dir = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\MATHIYA"), "Desktop")
    shortcut_path = os.path.join(desktop_dir, "GameLoop Chinese 64-Bit.lnk")
    target_exe = os.path.join(ui_dir, "AndroidEmulator.exe")

    if not os.path.exists(target_exe):
        log(f"Target executable does not exist at: {target_exe}", "ERROR")
        return False

    try:
        if win32com:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target_exe
            shortcut.Arguments = "-vm 100"
            shortcut.WorkingDirectory = ui_dir
            shortcut.IconLocation = f"{target_exe},0"
            shortcut.Description = "GameLoop Chinese 64-Bit (English UI with -vm 100)"
            shortcut.Save()
            log(f"Created Desktop shortcut: {shortcut_path}", "SUCCESS")
            log(f"Target: \"{target_exe}\" -vm 100", "SUCCESS")
            return True
        else:
            ps_cmd = (
                f"$ws = New-Object -ComObject WScript.Shell; "
                f"$s = $ws.CreateShortcut('{shortcut_path}'); "
                f"$s.TargetPath = '{target_exe}'; "
                f"$s.Arguments = '-vm 100'; "
                f"$s.WorkingDirectory = '{ui_dir}'; "
                f"$s.IconLocation = '{target_exe},0'; "
                f"$s.Save()"
            )
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            log(f"Created Desktop shortcut via PowerShell: {shortcut_path}", "SUCCESS")
            return True
    except Exception as e:
        log(f"Failed to create desktop shortcut: {e}", "ERROR")
        return False

def print_in_emulator_guide():
    guide = r"""
===============================================================================
       YOUTUBE VIDEO STEP-BY-STEP EMULATOR SETUP (TDR DADDY GUIDE)
===============================================================================

1. LAUNCH CHINESE GAMELOOP:
   - When the installer finishes, click 'Start Now' / '立即启动'.

2. DOWNLOAD 64-BIT ENGINE (QQ TRICK):
   - In the search bar inside GameLoop, type 'QQ' and press Enter.
   - Click the download/install button for QQ.
   - This triggers GameLoop to automatically download and compile the 64-bit Android instance!

3. SET ANDROID SYSTEM TO ENGLISH (F9 TRICK):
   - Once the Android emulator window boots up with QQ:
   - Press 'F9' (or click double-back) to show hidden Android system icons.
   - Open 'Settings' (Gear icon).
   - Scroll down and click the globe icon (Languages & Input / 语言和输入法).
   - Click the first option (Languages / 语言).
   - Click '+ Add a language' (+ 添加语言).
   - Search for 'English' -> Select 'United States'.
   - Drag 'English (United States)' up to position #1.
   - The entire Android interface will instantly switch to English!

4. SIDELOAD APKS VIA HOST SHARED FOLDER:
   - Copy your APK (PUBG Mobile / FX File Explorer) into:
     C:\Temp\TxGameDownload\MobileGamePCShared
   - Inside the emulator, open FX File Explorer (or Android Browser).
   - Navigate to: System (Root) -> data -> share1
   - Click the APK to install via Package Installer.

5. LAUNCHING WITH -VM 100 ENGLISH SHORTCUT:
   - Use the 'GameLoop Chinese 64-Bit' shortcut created on your Desktop.
   - It runs AndroidEmulator.exe with '-vm 100' directly with English UI!

===============================================================================
"""
    print(guide)

def run_installation_process():
    print("===============================================================================")
    print("       GAMELOOP CHINESE 64-BIT AUTOMATED SETUP & CONFIGURATION SUITE           ")
    print("===============================================================================")
    installer = ensure_installer_downloaded()
    setup_shared_directories()

    ui_dir = find_installed_ui_dir()
    if ui_dir:
        log(f"Existing GameLoop UI directory detected at: {ui_dir}", "SUCCESS")
        apply_english_ui_patch(ui_dir)
        create_vm100_desktop_shortcut(ui_dir)
    else:
        log("GameLoop UI directory not detected yet.", "INFO")
        log(f"Starting GameLoop Chinese 64-Bit installer: {installer}", "INFO")
        log("Please complete the on-screen installer wizard (click the main Install button).", "INFO")
        try:
            # Launch elevated installer via powershell Start-Process
            ps_launch = f"Start-Process -FilePath '{installer}' -Verb RunAs"
            subprocess.run(["powershell", "-Command", ps_launch], check=True)
            log("Installer launched on your desktop!", "SUCCESS")
        except Exception as e:
            log(f"Error launching installer: {e}", "ERROR")

    print_in_emulator_guide()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--patch":
        setup_shared_directories()
        ui = find_installed_ui_dir()
        if ui:
            apply_english_ui_patch(ui)
            create_vm100_desktop_shortcut(ui)
        else:
            log("GameLoop UI directory not found yet. Please ensure installation has finished.", "WARN")
    elif len(sys.argv) > 1 and sys.argv[1] == "--guide":
        print_in_emulator_guide()
    else:
        run_installation_process()
