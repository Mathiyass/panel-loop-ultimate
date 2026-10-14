r"""
===============================================================================
RELEASE PACKAGING SCRIPT: MATHIYA GAMELOOP PANEL v4.0
Packages the portable distribution and standalone executable into release ZIP
===============================================================================
"""

import os
import sys
import zipfile
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
RELEASE_DIR = os.path.join(BASE_DIR, "release")
os.makedirs(RELEASE_DIR, exist_ok=True)

ZIP_PATH = os.path.join(RELEASE_DIR, "Mathiya_GameLoop_Panel_v4.0_Setup.zip")
PORTABLE_EXE = os.path.join(DIST_DIR, "Mathiya_GameLoop_Panel_Portable.exe")
ONEDIR_FOLDER = os.path.join(DIST_DIR, "MathiyaGameLoopPanel")

def make_zip():
    print("[*] Packaging Mathiya GameLoop Panel v4.0 Setup...")

    readme_content = """===============================================================================
⚡ MATHIYA GAMELOOP PANEL v4.0 (MATHIYA TOURNAMENT SETUP)
Universal Locked 120 FPS, True HDR, and 0.50ms Kernel Timer Suite
===============================================================================

HOW TO RUN:

OPTION 1 (FASTEST - SINGLE PORTABLE EXE):
  Double click "Mathiya_GameLoop_Panel_Portable.exe" directly!
  No installation, no extraction required. Runs on any Windows 10/11 PC.

OPTION 2 (SILENT BACKGROUND LAUNCHER):
  Run "Run_Mathiya_GameLoop_Panel.vbs" for silent execution without console popups.

COMPATIBILITY:
  - GameLoop Chinese 64-Bit (AOW_Rootfs_100)
  - GameLoop Global 64-Bit (AOW_Rootfs_64)
  - GameLoop Global 32-Bit (TxGameAssistant)
  - All Editions: Global, BGMI, Korea, Vietnam, Taiwan
  - Hardware: AMD Ryzen & Intel Core processors

GitHub Repository & Updates:
https://github.com/Mathiyass/panel-loop-ultimate
"""
    readme_path = os.path.join(RELEASE_DIR, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add single portable exe
        if os.path.exists(PORTABLE_EXE):
            zf.write(PORTABLE_EXE, arcname="Mathiya_GameLoop_Panel_Portable.exe")
            print(f"[+] Added to ZIP: Mathiya_GameLoop_Panel_Portable.exe")

        # Add README
        zf.write(readme_path, arcname="README.txt")

        # Add Launchers
        vbs = os.path.join(BASE_DIR, "Run_Mathiya_GameLoop_Panel.vbs")
        bat = os.path.join(BASE_DIR, "Run_Mathiya_GameLoop_Panel.bat")
        if os.path.exists(vbs):
            zf.write(vbs, arcname="Run_Mathiya_GameLoop_Panel.vbs")
        if os.path.exists(bat):
            zf.write(bat, arcname="Run_Mathiya_GameLoop_Panel.bat")

        # Add onedir folder
        if os.path.exists(ONEDIR_FOLDER):
            for root, dirs, files in os.walk(ONEDIR_FOLDER):
                for f in files:
                    fp = os.path.join(root, f)
                    rel = os.path.relpath(fp, DIST_DIR)
                    zf.write(fp, arcname=rel)
            print(f"[+] Added to ZIP: MathiyaGameLoopPanel/ directory")

    size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    sha256 = hashlib.sha256()
    with open(ZIP_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    hash_hex = sha256.hexdigest()

    print(f"[+] SUCCESS! Release ZIP created: {ZIP_PATH} ({size_mb:.2f} MB)")
    print(f"[+] SHA-256: {hash_hex}")

    # Also record hash file
    with open(ZIP_PATH + ".sha256", "w") as f:
        f.write(f"{hash_hex}  Mathiya_GameLoop_Panel_v4.0_Setup.zip\n")

    return ZIP_PATH

if __name__ == "__main__":
    make_zip()
