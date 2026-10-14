r"""
===============================================================================
BUILD SCRIPT: STANDALONE PORTABLE EXECUTABLE FOR MATHIYA GAMELOOP PANEL
Packages python GUI + dependencies into portable --onedir distribution
Embeds Cyberpunk Esports icon and bundles assets and gl_optimized_files
Includes UAC Admin Manifest for Windows Registry & Inode Elevation
===============================================================================
"""

import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(BASE_DIR, "panel_loop_gui.py")
DIST_DIR = os.path.join(BASE_DIR, "dist")
BUILD_DIR = os.path.join(BASE_DIR, "build")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "mathiya_icon.ico")

def build_exe():
    print("[*] ========================================================")
    print("[*] BUILDING PORTABLE STANDALONE EXECUTABLE: MathiyaGameLoopPanel.exe")
    print("[*] Embedding Custom Esports Icon: assets/mathiya_icon.ico")
    print("[*] ========================================================")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--uac-admin",
        "--name", "MathiyaGameLoopPanel",
        "--icon", ICON_PATH,
        "--collect-all", "customtkinter",
        "--collect-all", "darkdetect",
        "--collect-all", "PIL",
        "--add-data", f"{os.path.join(BASE_DIR, 'gl_optimized_files')};gl_optimized_files",
        "--add-data", f"{ASSETS_DIR};assets",
        MAIN_SCRIPT
    ]

    print(f"[*] Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE_DIR)

    if result.returncode == 0:
        exe_path = os.path.join(DIST_DIR, "MathiyaGameLoopPanel", "MathiyaGameLoopPanel.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"[+] SUCCESS! Portable executable built: {exe_path} ({size_mb:.2f} MB)")
            
            # Ensure assets are also copied directly into dist folder alongside exe
            dist_assets = os.path.join(DIST_DIR, "MathiyaGameLoopPanel", "assets")
            if not os.path.exists(dist_assets):
                shutil.copytree(ASSETS_DIR, dist_assets)
                print(f"[+] Synced assets folder to: {dist_assets}")

            # Create a top-level launcher batch
            bat_path = os.path.join(BASE_DIR, "Run_Mathiya_GameLoop_Panel.bat")
            with open(bat_path, "w") as f:
                f.write('@echo off\n')
                f.write('start "" "%~dp0dist\\MathiyaGameLoopPanel\\MathiyaGameLoopPanel.exe"\n')
            print(f"[+] Created launcher: {bat_path}")

            # Create silent VBS launcher
            vbs_path = os.path.join(BASE_DIR, "Run_Mathiya_GameLoop_Panel.vbs")
            with open(vbs_path, "w") as f:
                f.write('Set WshShell = CreateObject("WScript.Shell")\n')
                f.write('WshShell.Run chr(34) & WshShell.CurrentDirectory & "\\dist\\MathiyaGameLoopPanel\\MathiyaGameLoopPanel.exe" & chr(34), 0\n')
                f.write('Set WshShell = Nothing\n')
            print(f"[+] Created silent VBS launcher: {vbs_path}")

            # Create Desktop Shortcut with Custom Esports Icon
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                desktop = shell.SpecialFolders("Desktop")
                shortcut_path = os.path.join(desktop, "Mathiya GameLoop Panel.lnk")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = vbs_path
                shortcut.WorkingDirectory = BASE_DIR
                shortcut.IconLocation = ICON_PATH + ",0"
                shortcut.Description = "Mathiya GameLoop Panel - Mathiya Tournament Setup (120 FPS Locked)"
                shortcut.save()
                print(f"[+] Created Desktop shortcut with Custom Esports Icon: {shortcut_path}")
            except Exception as e:
                print(f"[!] Desktop shortcut notice: {e}")

            return True
        else:
            print("[-] Error: Executable was not found in dist directory.")
            return False
    else:
        print(f"[-] PyInstaller build failed with exit code: {result.returncode}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
