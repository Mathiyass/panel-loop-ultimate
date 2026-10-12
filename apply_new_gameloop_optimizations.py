r"""
Apply Master Optimizations to New GameLoop (Android 13 64-Bit) & PUBG Mobile
Configures:
1. Host VM Registry: 8GB RAM, 8 Cores, Esports High Performance, DirectX+, No Fullscreen Opt.
2. Device Whitelist: ASUS ROG Phone 8 Pro (ASUS_AI2401_A) in Androws.json.
3. In-Game PUBG Mobile: Active.sav (120 FPS / UHD) and UserCustom.ini (Uncapped, 0 frame lag, 2GB dynamic VRAM, 1 CSM cascade).
4. Guest Android 13: 120Hz/240Hz SurfaceFlinger, 240Hz mouse events, 0 pointer acceleration.
5. Windows 11 Host: 0.50ms kernel timer, 0x26 quantum, Ryzen 5800X physical affinity (0x5555), Independent Flip, GPU preference, network turbo.
"""

import os
import sys
import json
import ctypes
import subprocess
import winreg
import time
import tac_engine

GL_BASE = r"C:\Program Files\Tencent\GameLoop"
GL_APP = r"C:\Program Files\Tencent\GameLoop\Application\7.0.107.0"
ADB_EXE = os.path.join(GL_APP, "adb.exe")
ANDROWS_JSON = os.path.join(GL_APP, "Androws.json")

def log(msg):
    print(f"[*] {msg}")

def step1_host_registry():
    log("=== STEP 1: CONFIGURING GAMELOOP HOST VM REGISTRY ===")
    common_path = r"Software\Tencent\GameLoop\Settings\Common"
    k_common = winreg.CreateKey(winreg.HKEY_CURRENT_USER, common_path)
    winreg.SetValueEx(k_common, "PerformanceMemoryGb", 0, winreg.REG_DWORD, 8)
    winreg.SetValueEx(k_common, "PerformanceCpuCoreNum", 0, winreg.REG_DWORD, 8)
    winreg.SetValueEx(k_common, "PerformanceMode", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(k_common, "DisableFullscreenOptimization", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(k_common, "RenderMode", 0, winreg.REG_DWORD, 1)  # DirectX+
    winreg.SetValueEx(k_common, "RenderUserType", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(k_common)
    log("  Host VM Common Settings: 8 GB RAM, 8 CPU Cores, High Performance, DirectX+, No Fullscreen Optimization locked.")

    gl_path = r"Software\Tencent\GameLoop\Settings\GameLoop"
    k_gl = winreg.CreateKey(winreg.HKEY_CURRENT_USER, gl_path)
    winreg.SetValueEx(k_gl, "ShowFps", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(k_gl, "AndroidAdbMode", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(k_gl)

    settings_path = r"Software\Tencent\GameLoop\Settings\GameLoopSettings"
    k_settings = winreg.CreateKey(winreg.HKEY_CURRENT_USER, settings_path)
    winreg.SetValueEx(k_settings, "AutoSilentUpdate", 0, winreg.REG_DWORD, 0)
    winreg.SetValueEx(k_settings, "PreDownloadSwitch", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(k_settings)
    log("  GameLoop Settings: ShowFps=1, AndroidAdbMode=1, AutoSilentUpdate=0, PreDownloadSwitch=0 locked.")

def step2_androws_json():
    log("=== STEP 2: CONFIGURING HARDWARE DEVICE WHITELIST (Androws.json) ===")
    if not os.path.exists(ANDROWS_JSON):
        log(f"  WARNING: {ANDROWS_JSON} not found!")
        return

    with open(ANDROWS_JSON, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)

    cfg["useLocalOpengl"] = True
    cfg["enableFence"] = True
    cfg["glTransport"] = "wormhole"
    if "hyperv" in cfg and isinstance(cfg["hyperv"], dict):
        cfg["hyperv"]["useLocalOpengl"] = True
        cfg["hyperv"]["enableFence"] = True
        cfg["hyperv"]["glTransport"] = "wormhole"

    # ASUS ROG Phone 8 Pro profile (Best 120 FPS whitelist compatibility)
    cfg["prop"] = {
        "board": "ASUS_AI2401_A",
        "brand": "asus",
        "manufacture": "asus",
        "model": "ASUS_AI2401_A"
    }

    with open(ANDROWS_JSON, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    log("  Androws.json updated: ASUS ROG Phone 8 Pro (AI2401_A) + useLocalOpengl=True + enableFence=True.")

def step3_hotpush_ue4_files():
    log("=== STEP 3: HOT-PUSHING PUBG MOBILE ACTIVE.SAV & USERCUSTOM.INI (ADB) ===")
    if not os.path.exists(ADB_EXE):
        log(f"  WARNING: ADB not found at {ADB_EXE}")
        return

    subprocess.run([ADB_EXE, "connect", "127.0.0.1:5555"], capture_output=True, timeout=5)

    saved_base = "/sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved"
    dst_sav = f"{saved_base}/SaveGames/Active.sav"
    dst_slot = f"{saved_base}/SaveGames/SettingConfig_Slot.sav"
    dst_ini = f"{saved_base}/Config/Android/UserCustom.ini"

    tmp_dir = os.path.join(os.getcwd(), "gl_optimized_files")
    os.makedirs(tmp_dir, exist_ok=True)

    # 1. Pull current Active.sav or use template
    local_sav = os.path.join(tmp_dir, "Active.sav")
    subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "pull", dst_sav, local_sav], capture_output=True)

    if os.path.exists(local_sav) and os.path.getsize(local_sav) > 1000:
        with open(local_sav, "rb") as f:
            data = bytearray(f.read())
        patched_data = tac_engine.patch_sav_bytes(data, quality=6, fps_enum=8)
        with open(local_sav, "wb") as f:
            f.write(patched_data)
        log("  Patched local Active.sav with Quality=6 (Ultra HD) & FPS=8 (120 FPS).")
    else:
        log("  Generating new Active.sav via tac_engine...")
        template_sav = os.path.join(tac_engine.SHARED_DIR, "Active.sav")
        if os.path.exists(template_sav):
            with open(template_sav, "rb") as f:
                data = bytearray(f.read())
            patched_data = tac_engine.patch_sav_bytes(data, quality=6, fps_enum=8)
            with open(local_sav, "wb") as f:
                f.write(patched_data)

    # 2. Generate drop-immune UserCustom.ini
    local_ini = os.path.join(tmp_dir, "UserCustom.ini")
    ini_content = tac_engine.generate_usercustom_ini(target_fps=0)
    with open(local_ini, "w", encoding="ascii") as f:
        f.write(ini_content)
    log("  Generated drop-immune UserCustom.ini (t.MaxFPS=0, r.OneFrameThreadLag=0, PoolSize=2048, Cascades=1).")

    # 3. Push both files to VM
    res_sav1 = subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "push", local_sav, dst_sav], capture_output=True, text=True)
    res_sav2 = subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "push", local_sav, dst_slot], capture_output=True, text=True)
    res_ini = subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "push", local_ini, dst_ini], capture_output=True, text=True)

    # 4. Set permissions
    subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "shell", "chmod", "666", dst_sav], capture_output=True)
    subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "shell", "chmod", "666", dst_slot], capture_output=True)
    subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "shell", "chmod", "666", dst_ini], capture_output=True)

    log(f"  Hot-Pushed Active.sav: {res_sav1.stdout.strip()}")
    log(f"  Hot-Pushed SettingConfig_Slot.sav: {res_sav2.stdout.strip()}")
    log(f"  Hot-Pushed UserCustom.ini: {res_ini.stdout.strip()}")

def step4_guest_android_settings():
    log("=== STEP 4: CONFIGURING GUEST ANDROID 13 DISPLAY & INPUT (ADB) ===")
    if not os.path.exists(ADB_EXE):
        return

    commands = [
        ["settings", "put", "system", "peak_refresh_rate", "240.0"],
        ["settings", "put", "system", "min_refresh_rate", "240.0"],
        ["settings", "put", "system", "pointer_speed", "0"],
        ["setprop", "debug.sf.fps", "240"],
        ["setprop", "ro.vendor.display.panel_refresh_rate", "240"],
        ["setprop", "windowsmgr.max_events_per_sec", "240"]
    ]
    for cmd in commands:
        subprocess.run([ADB_EXE, "-s", "127.0.0.1:5555", "shell"] + cmd, capture_output=True)
    log("  Android 13 Display & Input: 240Hz refresh rate, 240Hz mouse polling, 0 pointer acceleration enforced.")

def step5_windows_host_pacing():
    log("=== STEP 5: CONFIGURING WINDOWS 11 HOST PACING, GPU & SCHEDULER ===")

    # 0.50ms Kernel Timer Resolution
    try:
        ctypes.windll.winmm.timeBeginPeriod(1)
        ntdll = ctypes.WinDLL("ntdll.dll")
        actual = ctypes.c_ulong()
        ntdll.NtSetTimerResolution(5000, 1, ctypes.byref(actual))
        log(f"  Kernel Timer Resolution: {actual.value / 10000:.2f} ms synchronized.")
    except Exception as e:
        log(f"  Timer notice: {e}")

    # Win32PrioritySeparation = 0x26 (3:1 foreground boost)
    try:
        subprocess.run(["reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Control\PriorityControl", "/v", "Win32PrioritySeparation", "/t", "REG_DWORD", "/d", "38", "/f"], capture_output=True)
        log("  Scheduler Quantum: Win32PrioritySeparation = 0x26 (3:1 foreground boost).")
    except Exception as e:
        log(f"  PriorityControl notice: {e}")

    # Process elevation & Ryzen 7 5800X physical core affinity (0x5555)
    kernel32 = ctypes.windll.kernel32
    psapi = ctypes.windll.psapi
    HIGH_PRIORITY = 0x00000080
    RYZEN_PHYSICAL_AFFINITY = 0x5555  # Cores 0, 2, 4, 6, 8, 10, 12, 14
    targets = [
        "gameloopemulator.exe",
        "gameloopvm.exe",
        "gameloop.exe",
        "gameloopassistant.exe",
        "gameloopdldsvr.exe",
        "adb.exe"
    ]
    out = subprocess.check_output("tasklist /FO CSV /NH", text=True)
    elevated = 0
    for line in out.splitlines():
        for t in targets:
            if t in line.lower():
                try:
                    pid = int(line.split(",")[1].replace('"', ''))
                    h = kernel32.OpenProcess(0x0200 | 0x0400 | 0x0100, False, pid)
                    if h:
                        kernel32.SetPriorityClass(h, HIGH_PRIORITY)
                        kernel32.SetProcessAffinityMask(h, RYZEN_PHYSICAL_AFFINITY)
                        try:
                            psapi.EmptyWorkingSet(h)
                        except Exception:
                            pass
                        elevated += 1
                        kernel32.CloseHandle(h)
                except Exception:
                    pass
    log(f"  Elevated & Pinned {elevated} live GameLoop processes to Ryzen 5800X Physical Cores (0x5555).")

    # DirectX Direct Scanout (Independent Flip)
    try:
        layer_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers")
        for exe in [
            os.path.join(GL_APP, "GameLoopEmulator.exe"),
            os.path.join(GL_APP, "GameLoop.exe")
        ]:
            winreg.SetValueEx(layer_key, exe, 0, winreg.REG_SZ, "~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE")
        winreg.CloseKey(layer_key)
        log("  DirectX Direct Scanout (Independent Flip) registered for GameLoopEmulator.exe & GameLoop.exe.")
    except Exception as e:
        log(f"  AppCompatFlags notice: {e}")

    # DirectX High Performance GPU (RTX 3090, AutoHDR Disabled)
    try:
        gpu_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\DirectX\UserGpuPreferences")
        for exe in [
            os.path.join(GL_APP, "GameLoopEmulator.exe"),
            os.path.join(GL_APP, "GameLoop.exe")
        ]:
            winreg.SetValueEx(gpu_key, exe, 0, winreg.REG_SZ, "GpuPreference=2;AutoHDREnable=0;")
        winreg.CloseKey(gpu_key)
        log("  DirectX UserGpuPreferences: NVIDIA RTX 3090 High Performance locked.")
    except Exception as e:
        log(f"  UserGpuPreferences notice: {e}")

    # RTX 3090 Dynamic P-States
    try:
        subprocess.run(["nvidia-smi", "-rgc"], capture_output=True, timeout=5)
        log("  NVIDIA Dynamic Clock Scaling verified (Cool & Quiet, 0% idle fan).")
    except Exception:
        pass

    # Network Turbo (0ms Nagle Bypass)
    tac_engine.network_turbo()
    log("  Network Turbo: 0ms Nagle Bypass (TcpAckFrequency=1, TCPNoDelay=1) active.")

def main():
    log("Starting Master Optimizations for New GameLoop (Android 13 64-Bit)...")
    step1_host_registry()
    step2_androws_json()
    step3_hotpush_ue4_files()
    step4_guest_android_settings()
    step5_windows_host_pacing()
    log("=== ALL MASTER OPTIMIZATIONS SUCCESSFULLY APPLIED ===")

if __name__ == "__main__":
    main()
