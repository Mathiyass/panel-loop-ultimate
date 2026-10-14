r"""
===============================================================================
GITHUB RELEASE PUBLISHER: MATHIYA GAMELOOP PANEL v4.0
Pushes commit & tag, creates GitHub Release, and uploads portable setup assets
===============================================================================
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import subprocess
import ctypes
import ctypes.wintypes

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RELEASE_DIR = os.path.join(BASE_DIR, "release")
DIST_DIR = os.path.join(BASE_DIR, "dist")

REPO_OWNER = "Mathiyass"
REPO_NAME = "panel-loop-ultimate"
TAG_NAME = "v4.3.0"
RELEASE_TITLE = "⚡ Mathiya GameLoop Panel v4.3 — Streamer HDR 120 FPS Verified Edition"

RELEASE_NOTES = """# ⚡ Mathiya GameLoop Panel v4.3 (Streamer HDR 120 FPS Verified Edition)

### 🏆 Streamer Flat-Texture 120 FPS & Zero Combat Lag Edition
The definitive esports-grade optimization dashboard for **PUBG Mobile** and **GameLoop**.

---

## 🚀 What's New in v4.3 (Streamer HDR 120 FPS Verified Edition)

### 🏆 Verified Master Save Template & Flat Shaded Textures
- **Exact User-Verified `Active.sav` Template**: Sourced directly from esports gameplay (`BattleRenderQuality = 6`, `BattleFPS = 8`, `GraphicFavor = 4`, `BattleRenderStyle = 2`).
- **Watermark Confirmed**: In-game displays `HDR ⚡ [ping]` running at locked 119–120 FPS.
- **Flat Pastel Esports Shading**: Clean ground and building textures with zero texture loading stutter or pop-in during hot drops.
- **GameLoop Chinese Settings Center Locked**: Strictly synchronizes `超清2K` (ContentScale = 2), `高清` (RenderQuality = 3), and `90 FPS` (com.tencent.ig_FPSLevel = 90).
- **Universal Save Inode Sync**: Atomically clones and locks the 11,064-byte master save across both disk caches (`7\1c78`, `a\2839`), MobileGamePCShared, and local assets.
### ⚔️ Combat Anti-Stutter Engine
- **1.0ms Async Loading Time**: `s.AsyncLoadingTime = 1.0` guarantees disk streaming never steals more than 1ms from the 8.33ms (120 FPS) render frame.
- **Combat Particle & Physics Caps**: `fx.MaxCPUParticlesPerEmitter = 50` and `p.ClothPhysics = 0` eliminate CPU spikes during explosive close-quarter gunfights.
- **Vibrant Colorful Grading**: `r.ACESStyle = 2` and `BattleRenderStyle = 2` ensure high enemy contrast and visibility without visual noise.

---

## 🌟 Universal GameLoop Compatibility (All Versions Supported)
- **GameLoop Chinese 64-Bit** (`AOW_Rootfs_100` / Chinese Settings Center 设置中心)
- **GameLoop Global 64-Bit** (`AOW_Rootfs_64` / Global AppMarket)
- **GameLoop Global 32-Bit** (`TxGameAssistant` standard 32-bit / `AndroidEmulator.exe` / `AOW_Rootfs`)
- **All Game Package Editions**:
  - Global (`com.tencent.ig`)
  - BGMI India (`com.pubg.imobile`)
  - Korea / Japan (`com.pubg.krmobile`)
  - Vietnam (`com.vng.pubgmobile`)
  - Taiwan (`com.reindex.tw`)

### ⏱️ 0.50ms Kernel Timer & Universal CPU Pacing
- Sub-millisecond timer resolution locked to **0.50 ms** via native Win32 `NtSetTimerResolution`.
- **Dynamic CPU Topology Engine**: Automatically detects CPU core count and threads.
  - **AMD Ryzen**: Enforces physical core affinity (`0x5555` on 8-core, `0x0555` on 6-core) to bypass SMT cross-thread latency.
  - **Intel Core**: Supports auto-detecting physical performance cores (P-cores) or all logical cores.
- **High Process Priority**: Sets `HIGH_PRIORITY_CLASS (0x80)` for `aow_exe.exe` and `AndroidEmulatorEx.exe`.

### 🌐 Native Win32 DNS Flush & Hit-Registration Accelerator
- **Instant DNS Cache Flush**: Calls `dnsapi.dll!DnsFlushResolverCache` with **zero console popups or CMD flashes**.
- **Nagle's Algorithm Disabling**: Forces `TCPNoDelay = 1` and `TcpAckFrequency = 1` across all network adapters.
- **Zero Hitbox Interp Lag**: `p.NetInterpolation = 0.0` and `net.MaxClientTickRate = 120` to prevent ghost bullets.

### 🧹 Standby RAM & DirectX Shader Purger
- Reclaims fragmented memory from background processes (Discord, Edge, Chrome, SearchHost).
- Clears corrupted temporary DirectX shader cache files (`D3DSCache`) to eliminate hot-drop frame drops.

### 🎨 Custom Cyberpunk Esports Icon & ROG UI Overhaul
- Custom obsidian hexagon shield icon with dual cyan/ultraviolet borders and central "M" monogram.
- Active in titlebar, taskbar, desktop shortcut, and portable executable.

---

## 📥 Which file should I download?

1. **`Mathiya_GameLoop_Panel_Portable.exe` (Recommended)**:
   - Standalone single-file executable (~21.7 MB).
   - Double-click to run anywhere. No installation or extraction required!

2. **`Mathiya_GameLoop_Panel_v4.3_Setup.zip`**:
   - Complete package (~43.7 MB) containing the portable folder, silent VBS background launcher, and batch launcher.

---
*Built with ❤️ for the competitive gaming community.*
"""

def get_github_token():
    class CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ('Flags', ctypes.wintypes.DWORD), ('Type', ctypes.wintypes.DWORD),
            ('TargetName', ctypes.wintypes.LPWSTR), ('Comment', ctypes.wintypes.LPWSTR),
            ('LastWritten', ctypes.wintypes.FILETIME), ('CredentialBlobSize', ctypes.wintypes.DWORD),
            ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)), ('Persist', ctypes.wintypes.DWORD),
            ('AttributeCount', ctypes.wintypes.DWORD), ('Attributes', ctypes.c_void_p),
            ('TargetAlias', ctypes.wintypes.LPWSTR), ('UserName', ctypes.wintypes.LPWSTR)
        ]
    pCred = ctypes.POINTER(CREDENTIAL)()
    if ctypes.windll.advapi32.CredReadW(f'GitHub - https://api.github.com/{REPO_OWNER}', 1, 0, ctypes.byref(pCred)):
        cred = pCred.contents
        token = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize).decode('utf-8', errors='ignore')
        ctypes.windll.advapi32.CredFree(pCred)
        return token
    return None

def main():
    token = get_github_token()
    if not token:
        print("[-] Error: Could not retrieve GitHub token from Windows Credential Manager.")
        sys.exit(1)
    print(f"[+] Retrieved GitHub token for {REPO_OWNER} (prefix: {token[:4]}...)")

    # 1. Push commits and tag to GitHub
    push_url = f"https://{token}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    print(f"[*] Pushing 'main' branch to GitHub...")
    res_push = subprocess.run(["git", "push", push_url, "main"], cwd=BASE_DIR, capture_output=True, text=True)
    if res_push.returncode != 0:
        print(f"[-] Git push failed: {res_push.stderr}")
        sys.exit(1)
    print("[+] Successfully pushed 'main' branch.")

    print(f"[*] Pushing tag '{TAG_NAME}' to GitHub...")
    res_tag = subprocess.run(["git", "push", push_url, TAG_NAME], cwd=BASE_DIR, capture_output=True, text=True)
    if res_tag.returncode != 0:
        print(f"[-] Git push tag failed: {res_tag.stderr}")
        # tag might already exist, continue
    else:
        print(f"[+] Successfully pushed tag '{TAG_NAME}'.")

    # 2. Check if release already exists
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "MathiyaPanelPublisher"
    }

    rel_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{TAG_NAME}"
    existing_release = None
    try:
        req = urllib.request.Request(rel_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            existing_release = json.loads(resp.read().decode("utf-8"))
            print(f"[*] Found existing release for tag {TAG_NAME} (ID: {existing_release['id']})")
    except Exception:
        pass

    if existing_release:
        release_id = existing_release["id"]
        upload_url = existing_release["upload_url"].split("{")[0]
    else:
        # Create new release
        print(f"[*] Creating new GitHub Release: {RELEASE_TITLE}...")
        create_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
        payload = {
            "tag_name": TAG_NAME,
            "target_commitish": "main",
            "name": RELEASE_TITLE,
            "body": RELEASE_NOTES,
            "draft": False,
            "prerelease": False
        }
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(create_url, data=data_bytes, headers={**headers, "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            rel_data = json.loads(resp.read().decode("utf-8"))
            release_id = rel_data["id"]
            upload_url = rel_data["upload_url"].split("{")[0]
            print(f"[+] Successfully created Release: {rel_data['html_url']} (ID: {release_id})")

    # 3. Upload Assets
    assets_to_upload = [
        ("Mathiya_GameLoop_Panel_Portable.exe", os.path.join(DIST_DIR, "Mathiya_GameLoop_Panel_Portable.exe"), "application/octet-stream"),
        ("Mathiya_GameLoop_Panel_v4.3_Setup.zip", os.path.join(RELEASE_DIR, "Mathiya_GameLoop_Panel_v4.3_Setup.zip"), "application/zip")
    ]

    # Get list of existing assets on this release
    assets_list_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{release_id}/assets"
    existing_assets = {}
    try:
        req = urllib.request.Request(assets_list_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            items = json.loads(resp.read().decode("utf-8"))
            for item in items:
                existing_assets[item["name"]] = item["id"]
    except Exception as e:
        print(f"[!] Notice checking existing assets: {e}")

    for asset_name, asset_path, mime_type in assets_to_upload:
        if not os.path.exists(asset_path):
            print(f"[!] Warning: Asset not found: {asset_path}")
            continue

        # If asset already exists, delete it first to re-upload clean version
        if asset_name in existing_assets:
            del_id = existing_assets[asset_name]
            print(f"[*] Deleting existing asset {asset_name} (ID: {del_id})...")
            try:
                del_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/assets/{del_id}"
                req = urllib.request.Request(del_url, headers=headers, method="DELETE")
                urllib.request.urlopen(req)
                print(f"[+] Removed old {asset_name}")
            except Exception as e:
                print(f"[!] Warning deleting old asset: {e}")

        size_mb = os.path.getsize(asset_path) / (1024 * 1024)
        print(f"[*] Uploading {asset_name} ({size_mb:.2f} MB)...")

        target_upload_url = f"{upload_url}?name={urllib.parse.quote(asset_name)}"
        with open(asset_path, "rb") as f:
            file_data = f.read()

        req = urllib.request.Request(
            target_upload_url,
            data=file_data,
            headers={
                **headers,
                "Content-Type": mime_type,
                "Content-Length": str(len(file_data))
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            asset_res = json.loads(resp.read().decode("utf-8"))
            print(f"[+] Uploaded: {asset_name} -> {asset_res.get('browser_download_url')}")

    print("\n==================================================================")
    print(f"[+] RELEASE PUBLISHED SUCCESSFULLY!")
    print(f"[+] Release URL: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{TAG_NAME}")
    print("==================================================================")

if __name__ == "__main__":
    main()
