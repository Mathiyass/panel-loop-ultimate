r"""
Capture & Lock Tool: In-Game Native HDR & 120 FPS Synchronization
Allows temporary unlock of save files so the in-game UI can write native HDR,
then captures the exact quality value, injects 120 FPS (BattleFPS=8), and locks all files.
"""

import os
import sys
import struct
import subprocess

ROOTFS_SAVES = [
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\7\1c78",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\a\2839"
]
SHARED_SAVES = [
    r"C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav",
    r"C:\Temp\TxGameDownload\MobileGamePCShared\SettingConfig_Slot.sav"
]
LOCAL_SAVES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "gl_optimized_files", "Active.sav"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "gl_optimized_files", "SettingConfig_Slot.sav")
]
ALL_SAVES = ROOTFS_SAVES + SHARED_SAVES + LOCAL_SAVES

def unlock_all():
    print("[*] Unlocking all save files for in-game editing...")
    for p in ALL_SAVES:
        if os.path.exists(p):
            subprocess.run(["attrib", "-r", "-s", p], capture_output=True)
            try:
                os.chmod(p, 0o777)
            except Exception:
                pass
            meta = p + ".ini"
            if os.path.exists(meta):
                subprocess.run(["attrib", "-r", "-s", meta], capture_output=True)
                with open(meta, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                new_lines = [l if not l.startswith("Mode=") else "Mode=0100777\n" for l in lines]
                with open(meta, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
    print("[+] All save files unlocked (writable). You can now change settings in PUBG Mobile.")

def lock_and_boost_120fps():
    print("[*] Inspecting save files to capture native quality and boost to 120 FPS...")
    target = ROOTFS_SAVES[0] if os.path.exists(ROOTFS_SAVES[0]) else SHARED_SAVES[0]
    if not os.path.exists(target):
        print("[-] Error: Save file not found!")
        return

    with open(target, "rb") as f:
        buf = bytearray(f.read())

    # Read captured quality
    int_prop = b"IntProperty\x00"
    def read_val(name):
        k = name.encode("latin1") + b"\x00"
        pos = buf.find(k)
        if pos != -1:
            idx = buf.find(int_prop, pos, pos + 80)
            if idx != -1:
                off = idx + len(int_prop) + 8 + 1
                return struct.unpack("<i", buf[off:off+4])[0]
        return None

    quality = read_val("BattleRenderQuality")
    print(f"[+] Detected current BattleRenderQuality: {quality}")

    # Inject 120 FPS and Colorful style
    updates = {
        "FPSLevel": 8,
        "BattleFPS": 8,
        "LobbyFPS": 8,
        "MainCityFPS": 8,
        "GraphicFavor": 4,
        "BattleRenderStyle": 2,
        "LobbyRenderStyle": 2
    }
    for name, val in updates.items():
        k = name.encode("latin1") + b"\x00"
        pos = buf.find(k)
        if pos != -1:
            idx = buf.find(int_prop, pos, pos + 80)
            if idx != -1:
                off = idx + len(int_prop) + 8 + 1
                buf[off:off+4] = struct.pack("<i", val)

    for p in ALL_SAVES:
        if os.path.exists(p):
            with open(p, "wb") as f:
                f.write(buf)
            subprocess.run(["attrib", "+r", p], capture_output=True)
            meta = p + ".ini"
            if os.path.exists(meta):
                with open(meta, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                new_lines = [l if not l.startswith("Mode=") else "Mode=0100444\n" for l in lines]
                with open(meta, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                subprocess.run(["attrib", "+r", meta], capture_output=True)
            print(f"[+] Locked: {p}")

    print("[+] Synchronization complete: Locked at 120 FPS with current quality setting!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--unlock":
        unlock_all()
    else:
        lock_and_boost_120fps()
