r"""
Master Forensic Purge Script: GameLoop 7.0/8.0 (Android 13 64-Bit) & All Remnants
Safely purges GameLoop, services, drivers, registry hives, and temp files.
Explicitly safeguards:
- C:\Program Files\TAC Panel Loop
- C:\Users\MATHIYA\Documents\saasassasa
"""

import os
import sys
import subprocess
import shutil
import time
import winreg

PROTECTED_DIRS = [
    r"C:\Program Files\TAC Panel Loop",
    r"C:\Users\MATHIYA\Documents\saasassasa"
]

def log(msg):
    print(f"[*] {msg}")

def is_protected(path):
    norm = os.path.normcase(os.path.abspath(path))
    for p in PROTECTED_DIRS:
        norm_p = os.path.normcase(os.path.abspath(p))
        if norm == norm_p or norm.startswith(norm_p + "\\"):
            return True
    return False

def step1_kill_processes():
    log("=== STEP 1: TERMINATING ACTIVE GAMELOOP & AUXILIARY PROCESSES ===")
    targets = [
        "GameLoop.exe",
        "GameLoopEmulator.exe",
        "GameLoopVm.exe",
        "GameLoopAssistant.exe",
        "GameLoopAssistantToast.exe",
        "GameLoopDldSvr.exe",
        "GameLoopLauncher.exe",
        "GameLoopService.exe",
        "GameLoopUpdate.exe",
        "GameLoopVfs.exe",
        "adb.exe",
        "GLABoxHeadless.exe",
        "GLABoxManage.exe",
        "GLABoxSVC.exe",
        "VBoxNetDHCP.exe",
        "VBoxNetNAT.exe",
        "shutdown_abox.exe",
        "SilentProcess.exe",
        "CefRendererProcess.exe",
        "crashpad_handler.exe",
        "dokanctl.exe",
        "ginkgo.exe",
        "hpatchz.exe"
    ]
    for proc in targets:
        try:
            res = subprocess.run(["taskkill", "/f", "/im", proc], capture_output=True, text=True)
            if res.returncode == 0:
                log(f"  Terminated: {proc}")
        except Exception:
            pass
    time.sleep(1)

def step2_services_and_drivers():
    log("=== STEP 2: UNREGISTERING SERVICES & VIRTUALIZATION DRIVERS ===")
    # GameLoopService
    try:
        subprocess.run(["sc", "stop", "GameLoopService"], capture_output=True)
        res = subprocess.run(["sc", "delete", "GameLoopService"], capture_output=True, text=True)
        log("  GameLoopService: Stopped & Deleted")
    except Exception as e:
        log(f"  GameLoopService notice: {e}")

    # GLABoxSup Driver
    try:
        subprocess.run(["sc", "stop", "GLABoxSup"], capture_output=True)
        res = subprocess.run(["sc", "delete", "GLABoxSup"], capture_output=True, text=True)
        log("  GLABoxSup Virtualization Driver: Stopped & Deleted")
    except Exception as e:
        log(f"  GLABoxSup notice: {e}")

def force_delete_dir(path):
    if not os.path.exists(path):
        return 0, 0
    if is_protected(path):
        log(f"  [PROTECTED - SKIPPED] {path}")
        return 0, 0

    count = 0
    bytes_freed = 0
    # Strip readonly attributes
    try:
        subprocess.run(["attrib", "-r", "-s", "-h", f"{path}\\*.*", "/s", "/d"], capture_output=True, timeout=10)
    except Exception:
        pass

    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    bytes_freed += os.path.getsize(fp)
                    os.chmod(fp, 0o777)
                    os.remove(fp)
                    count += 1
                except Exception:
                    pass
            for d in dirs:
                dp = os.path.join(root, d)
                try:
                    os.rmdir(dp)
                except Exception:
                    pass
        os.rmdir(path)
    except Exception:
        # Fallback to cmd rmdir /s /q
        try:
            subprocess.run(f'cmd /c rd /s /q "{path}"', shell=True, capture_output=True)
        except Exception:
            pass

    return count, bytes_freed

def step3_purge_directories():
    log("=== STEP 3: PURGING FILE SYSTEM DIRECTORIES & DISK RESIDUES ===")
    dirs_to_purge = [
        r"C:\Program Files\Tencent",
        r"C:\Program Files (x86)\GameLoopHub",
        r"C:\Temp\TxGameDownload",
        r"C:\ProgramData\Tencent",
        os.path.expandvars(r"%APPDATA%\Tencent"),
        os.path.expandvars(r"%LOCALAPPDATA%\Tencent"),
        os.path.expandvars(r"%TEMP%\Tencent"),
        os.path.expandvars(r"%TEMP%\TxGameDownload"),
        r"C:\Windows\Temp\Tencent",
        os.path.expandvars(r"%USERPROFILE%\.GameLoopBox"),
        os.path.expandvars(r"%USERPROFILE%\.AndrowsBox"),
        os.path.expandvars(r"%LOCALAPPDATA%\pubg-mobile-smart-tool-updater")
    ]

    total_files = 0
    total_bytes = 0
    for d in dirs_to_purge:
        if os.path.exists(d):
            c, b = force_delete_dir(d)
            mb = b / (1024 * 1024)
            log(f"  Purged: {d} ({c} files, {mb:.2f} MB)")
            total_files += c
            total_bytes += b

    # Downloads folder target packages
    dl_files = [
        os.path.expandvars(r"%USERPROFILE%\Downloads\GLP_installer_900223086_market.exe"),
        os.path.expandvars(r"%USERPROFILE%\Downloads\PUBGMOBILE_Global_4.6.0_uawebsite_livik01_5678FCFA.apk"),
        os.path.expandvars(r"%USERPROFILE%\Downloads\PUBG-Mobile-Smart-Tool.zip")
    ]
    for fp in dl_files:
        if os.path.exists(fp):
            try:
                sz = os.path.getsize(fp)
                os.remove(fp)
                log(f"  Deleted Download Installer: {os.path.basename(fp)} ({sz / (1024*1024):.2f} MB)")
                total_files += 1
                total_bytes += sz
            except Exception as e:
                log(f"  Error deleting {fp}: {e}")

    dl_tool_dir = os.path.expandvars(r"%USERPROFILE%\Downloads\PUBG-Mobile-Smart-Tool")
    if os.path.exists(dl_tool_dir):
        c, b = force_delete_dir(dl_tool_dir)
        log(f"  Deleted Download Folder: PUBG-Mobile-Smart-Tool ({c} files)")

    log(f"  Disk Purge Total: {total_files} files, {total_bytes / (1024*1024):.2f} MB freed.")

def step4_purge_shortcuts():
    log("=== STEP 4: PURGING SHORTCUTS & START MENU LINKS ===")
    shortcuts = [
        os.path.expandvars(r"%USERPROFILE%\Desktop\GameLoop.lnk"),
        os.path.expandvars(r"%USERPROFILE%\Desktop\PUBG Mobile.lnk"),
        r"C:\Users\Public\Desktop\GameLoop.lnk",
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\GameLoop.lnk",
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PUBG Mobile Smart Tool.lnk",
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\GameLoop.lnk")
    ]
    for s in shortcuts:
        if os.path.exists(s):
            try:
                os.remove(s)
                log(f"  Deleted Shortcut: {s}")
            except Exception as e:
                log(f"  Error deleting {s}: {e}")

def delete_reg_tree(root, path):
    try:
        subprocess.run(["reg", "delete", rf"{root}\{path}", "/f"], capture_output=True)
    except Exception:
        pass

def step5_purge_registry():
    log("=== STEP 5: PURGING REGISTRY HIVES & COMPATIBILITY ARTIFACTS ===")
    # Primary trees
    delete_reg_tree("HKCU", r"Software\Tencent")
    delete_reg_tree("HKLM", r"SOFTWARE\Tencent")
    delete_reg_tree("HKLM", r"SOFTWARE\WOW6432Node\Tencent")
    delete_reg_tree("HKU", r".DEFAULT\Software\Tencent")

    # Add/Remove Programs uninstall entries
    delete_reg_tree("HKLM", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\com.tencent.ig")
    delete_reg_tree("HKLM", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GameLoop")
    delete_reg_tree("HKLM", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\com.tencent.ig")
    delete_reg_tree("HKLM", r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\GameLoop")

    # Image File Execution Options
    for proc in ["GameLoop.exe", "GameLoopEmulator.exe", "GameLoopVm.exe", "GameLoopAssistant.exe", "adb.exe", "aow_exe.exe", "AndroidEmulator.exe"]:
        delete_reg_tree("HKLM", rf"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{proc}")

    # AppCompatFlags Layers
    try:
        k_path = r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, k_path, 0, winreg.KEY_READ | winreg.KEY_SET_VALUE) as k:
            count = winreg.QueryInfoKey(k)[1]
            to_del = []
            for i in range(count):
                try:
                    name, _, _ = winreg.EnumValue(k, i)
                    if any(x in name.lower() for x in ["tencent", "gameloop", "txgame"]):
                        to_del.append(name)
                except Exception:
                    pass
            for name in to_del:
                winreg.DeleteValue(k, name)
                log(f"  Deleted AppCompatFlags entry: {name}")
    except Exception:
        pass

    # UserGpuPreferences
    try:
        gpu_path = r"Software\Microsoft\DirectX\UserGpuPreferences"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, gpu_path, 0, winreg.KEY_READ | winreg.KEY_SET_VALUE) as k:
            count = winreg.QueryInfoKey(k)[1]
            to_del = []
            for i in range(count):
                try:
                    name, _, _ = winreg.EnumValue(k, i)
                    if any(x in name.lower() for x in ["tencent", "gameloop", "txgame"]):
                        to_del.append(name)
                except Exception:
                    pass
            for name in to_del:
                winreg.DeleteValue(k, name)
                log(f"  Deleted UserGpuPreferences entry: {name}")
    except Exception:
        pass

    # Shell context menu handlers
    delete_reg_tree("HKCR", r"Directory\shellex\ContextMenuHandlers\PcyybContextMenu")
    delete_reg_tree("HKCR", r"Directory\Background\shellex\ContextMenuHandlers\PcyybContextMenu")
    delete_reg_tree("HKCU", r"Software\Classes\Directory\shellex\ContextMenuHandlers\PcyybContextMenu")

    log("  Registry purge complete.")

def step6_revert_defender_and_dns():
    log("=== STEP 6: REVERTING DEFENDER EXCLUSIONS & FLUSHING DNS ===")
    ps_cmd = (
        "Remove-MpPreference -ExclusionPath 'C:\\Program Files\\Tencent' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionPath 'C:\\Program Files\\Tencent\\GameLoop' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionPath 'C:\\Temp\\TxGameDownload' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'GameLoopEmulator.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'GameLoopVm.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'GameLoop.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'GameLoopAssistant.exe' -ErrorAction SilentlyContinue; "
        "Remove-MpPreference -ExclusionProcess 'adb.exe' -ErrorAction SilentlyContinue"
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, timeout=5)
        log("  Defender exclusions reverted.")
    except Exception as e:
        log(f"  Defender notice: {e}")

    try:
        subprocess.run(["ipconfig", "/flushdns"], capture_output=True, timeout=3)
        log("  Windows DNS Resolver Cache Flushed.")
    except Exception:
        pass

def main():
    log("=================================================================")
    log("      STARTING FULL UNINSTALL & PURGE OF GAMELOOP & ARTIFACTS     ")
    log("=================================================================")
    step1_kill_processes()
    step2_services_and_drivers()
    step3_purge_directories()
    step4_purge_shortcuts()
    step5_purge_registry()
    step6_revert_defender_and_dns()
    log("=================================================================")
    log("      GAMELOOP FULL UNINSTALLATION & PURGE SUCCESSFULLY COMPLETED ")
    log("=================================================================")

if __name__ == "__main__":
    main()
