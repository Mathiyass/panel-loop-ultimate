r"""
Purge GameLoop - Full Uninstaller & Deep System Cleaner
Completely terminates, unregisters, deletes, and verifies GameLoop (TxGameAssistant)
and all downloaded caches, APKs, setups, services, drivers, and registry entries.
PROTECTS: C:\Program Files\TAC Panel Loop and C:\Users\MATHIYA\Documents\saasassasa.
"""

import os
import sys
import shutil
import subprocess
import winreg
import time
import stat

PROTECTED_DIRS = [
    os.path.normpath(r"C:\Program Files\TAC Panel Loop").lower(),
    os.path.normpath(r"C:\Users\MATHIYA\Documents\saasassasa").lower()
]

TARGET_DIRS = [
    r"C:\Program Files\TxGameAssistant",
    r"C:\GameLoopSetup",
    r"C:\Temp\TxGameDownload",
    r"C:\Program Files (x86)\GameLoopHub",
    r"C:\Windows\Temp\Tencent",
    r"C:\ProgramData\Tencent",
    r"C:\Users\MATHIYA\AppData\Roaming\Tencent",
    r"C:\Users\MATHIYA\AppData\Local\Tencent"
]

TARGET_SHORTCUTS = [
    r"C:\Users\MATHIYA\Desktop\AndroidEmulator - Shortcut.lnk"
]

TARGET_PROCESSES = [
    "QMEmulatorService.exe",
    "AppMarket.exe",
    "AndroidEmulator.exe",
    "AndroidEmulatorEn.exe",
    "AndroidEmulatorEx.exe",
    "aow_exe.exe",
    "render_service.exe",
    "TInstQ.exe",
    "TSettingCenter.exe"
]

TARGET_SERVICES = [
    "QMEmulatorService",
    "aow_drv"
]

def log(msg):
    print(f"[*] {msg}")

def remove_readonly(func, path, exc_info):
    """Error handler for shutil.rmtree to remove read-only attribute and retry."""
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
        subprocess.run(["attrib", "-r", "-s", "-h", path], capture_output=True)
        func(path)
    except Exception as e:
        log(f"    Notice on {path}: {e}")

def step1_terminate_processes():
    log("=== STEP 1: TERMINATING GAMELOOP PROCESSES ===")
    for proc in TARGET_PROCESSES:
        res = subprocess.run(["taskkill", "/f", "/im", proc, "/t"], capture_output=True, text=True)
        if "SUCCESS" in res.stdout.upper() or "PID" in res.stdout:
            log(f"  Terminated: {proc}")
    time.sleep(1)

def step2_stop_and_delete_services():
    log("=== STEP 2: STOPPING AND DELETING SERVICES & DRIVERS ===")
    for svc in TARGET_SERVICES:
        log(f"  Stopping service/driver: {svc}")
        subprocess.run(["sc", "stop", svc], capture_output=True)
        time.sleep(1)
        res = subprocess.run(["sc", "delete", svc], capture_output=True, text=True)
        log(f"  Delete {svc} result: {res.stdout.strip()}")

    log("  Deleting scheduled task: \\RunGameLoopInstaller")
    res = subprocess.run(["schtasks", "/delete", "/tn", "\\RunGameLoopInstaller", "/f"], capture_output=True, text=True)
    log(f"  Task result: {res.stdout.strip() if res.stdout else res.stderr.strip()}")

def step3_cleanup_firewall_and_defender():
    log("=== STEP 3: CLEANING FIREWALL RULES & DEFENDER EXCLUSIONS ===")
    for rule in ["AndroidEmulator", "AndroidEmulatorEn", "AndroidEmulatorEx", "AppMarket"]:
        res = subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule}"], capture_output=True, text=True)
        log(f"  Firewall rule {rule} removed: {res.stdout.strip()}")

    ps_defender = (
        "Remove-MpPreference -ExclusionPath 'C:\\Program Files\\TxGameAssistant' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionPath 'C:\\Temp\\TxGameDownload' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'AndroidEmulator.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'AndroidEmulatorEn.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'AndroidEmulatorEx.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'aow_exe.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'AppMarket.exe' -ErrorAction SilentlyContinue"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_defender], capture_output=True)
    log("  Windows Defender exclusions for GameLoop cleaned.")

def step4_purge_registry():
    log("=== STEP 4: PURGING REGISTRY TREES & ENTRIES ===")
    reg_keys_to_delete = [
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\QMEmulatorService"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\aow_drv")
    ]
    for root, path in reg_keys_to_delete:
        root_name = "HKCU" if root == winreg.HKEY_CURRENT_USER else "HKLM"
        res = subprocess.run(["reg", "delete", f"{root_name}\\{path}", "/f"], capture_output=True, text=True)
        log(f"  Reg delete {root_name}\\{path}: {res.stdout.strip() if res.stdout else res.stderr.strip()}")

    ifeo_base = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
    for exe in ["AndroidEmulator.exe", "AndroidEmulatorEn.exe", "AndroidEmulatorEx.exe", "aow_exe.exe", "AppMarket.exe", "render_service.exe"]:
        subprocess.run(["reg", "delete", f"{ifeo_base}\\{exe}", "/f"], capture_output=True)
        log(f"  Removed IFEO entry: {exe}")

    # UserGpuPreferences
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectX\UserGpuPreferences", 0, winreg.KEY_READ | winreg.KEY_SET_VALUE)
        names = []
        i = 0
        while True:
            try:
                name, _, _ = winreg.EnumValue(k, i)
                if any(x in name.lower() for x in ["txgame", "androidemulator", "aow", "appmarket"]):
                    names.append(name)
                i += 1
            except OSError:
                break
        for n in names:
            winreg.DeleteValue(k, n)
            log(f"  Removed UserGpuPreferences: {n}")
        winreg.CloseKey(k)
    except Exception as e:
        log(f"  UserGpuPreferences notice: {e}")

    # AppCompatFlags Layers
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers", 0, winreg.KEY_READ | winreg.KEY_SET_VALUE)
        names = []
        i = 0
        while True:
            try:
                name, _, _ = winreg.EnumValue(k, i)
                if any(x in name.lower() for x in ["txgame", "androidemulator", "aow", "appmarket"]):
                    names.append(name)
                i += 1
            except OSError:
                break
        for n in names:
            winreg.DeleteValue(k, n)
            log(f"  Removed AppCompatFlags Layer: {n}")
        winreg.CloseKey(k)
    except Exception as e:
        log(f"  AppCompatFlags notice: {e}")

def step5_purge_filesystem():
    log("=== STEP 5: DELETING GAMELOOP DIRECTORIES & DOWNLOADS ===")
    # Remove shortcuts
    for sc in TARGET_SHORTCUTS:
        if os.path.exists(sc):
            try:
                os.remove(sc)
                log(f"  Deleted shortcut: {sc}")
            except Exception as e:
                log(f"  Failed deleting shortcut {sc}: {e}")

    for target in TARGET_DIRS:
        norm = os.path.normpath(target).lower()
        if any(norm == p or norm.startswith(p + os.sep) for p in PROTECTED_DIRS):
            log(f"  SAFETY CHECK PREVENTED DELETION OF PROTECTED PATH: {target}")
            continue

        if os.path.exists(target):
            log(f"  Unlocking and purging: {target}")
            # Unlock attributes
            subprocess.run(["attrib", "-r", "-s", "-h", f"{target}\\*", "/s", "/d"], capture_output=True)
            subprocess.run(["takeown", "/f", target, "/r", "/d", "y"], capture_output=True)
            subprocess.run(["icacls", target, "/grant", "Administrators:F", "/t", "/c", "/q"], capture_output=True)

            try:
                shutil.rmtree(target, onerror=remove_readonly)
            except Exception as e:
                log(f"  shutil.rmtree notice on {target}: {e}, trying cmd rd /s /q...")
                subprocess.run(["cmd", "/c", f'rd /s /q "{target}"'], capture_output=True)

            if os.path.exists(target):
                subprocess.run(["cmd", "/c", f'rd /s /q "{target}"'], capture_output=True)

            if not os.path.exists(target):
                log(f"  [SUCCESS] Completely removed: {target}")
            else:
                log(f"  [WARNING] Path still present (may be locked): {target}")
        else:
            log(f"  Already clean: {target}")

def main():
    log("Starting Full GameLoop & Download Files Deep Purge...")
    step1_terminate_processes()
    step2_stop_and_delete_services()
    step3_cleanup_firewall_and_defender()
    step4_purge_registry()
    step5_purge_filesystem()
    log("=== PURGE COMPLETE ===")

if __name__ == "__main__":
    main()
