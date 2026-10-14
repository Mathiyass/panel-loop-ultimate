import os
import sys

def create_shortcut():
    try:
        import win32com.client
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"])
        import win32com.client

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    target_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "PanelLoopUltimate.exe")
    shortcut_path = os.path.join(desktop, "Panel Loop Ultimate.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = target_exe
    shortcut.WorkingDirectory = os.path.dirname(target_exe)
    shortcut.Description = "Panel Loop Ultimate - Esports 120 FPS Optimizer"
    shortcut.save()
    print(f"[+] Desktop Shortcut created: {shortcut_path}")

if __name__ == "__main__":
    create_shortcut()
