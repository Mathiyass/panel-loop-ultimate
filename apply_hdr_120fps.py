import struct
import shutil
import os
import subprocess

source_file = r'C:\Temp\TxGameDownload\MobileGamePCShared\Active_current.sav'
target_file = r'C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav'

with open(source_file, 'rb') as f:
    buf = bytearray(f.read())

print(f'Original file length: {len(buf)} bytes')

hdr_targets = {
    'FPSLevel': 8,              # 120 FPS
    'BattleFPS': 8,             # 120 FPS
    'LobbyFPS': 8,              # 120 FPS
    'MainCityFPS': 8,           # 120 FPS
    'BattleRenderQuality': 4,   # 4 = HDR
    'LobbyRenderQuality': 4,    # 4 = HDR
    'MainCityRenderQuality': 4, # 4 = HDR
    'ManorRenderQuality': 4,    # 4 = HDR
    'GFBestQBattle': 4,         # 4 = HDR
    'GFBestQLobby': 4,          # 4 = HDR
    'GraphicFavor': 4,          # 4 = HDR
    'nEnhancedLobbyQuality': 2  # 2 = Enhanced
}

patched = 0
for prop_name, new_val in hdr_targets.items():
    prefix = prop_name.encode('latin1') + b'\x00\x0c\x00\x00\x00IntProperty\x00'
    pos = buf.find(prefix)
    if pos != -1:
        val_offset = pos + len(prop_name) + 1 + 4 + 12 + 9
        old_val = struct.unpack('<I', buf[val_offset:val_offset+4])[0]
        buf[val_offset:val_offset+4] = struct.pack('<I', new_val)
        print(f'Patched {prop_name}: {old_val} -> {new_val} (offset {val_offset})')
        patched += 1
    else:
        print(f'WARNING: Property {prop_name} not found!')

with open(target_file, 'wb') as f:
    f.write(buf)

print(f'Wrote HDR 120 FPS Active.sav ({len(buf)} bytes).')

# Overwrite rootfs files directly
rootfs_destinations = [
    r'C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1945',
    r'C:\Program Files\TxGameAssistant\AOW_Rootfs_100\9\24c8'
]

for dest in rootfs_destinations:
    shutil.copy2(target_file, dest)
    print(f'Deployed to {dest} ({os.path.getsize(dest)} bytes)')

# Update UserCustom.ini with XOR 0x79 encrypted CVars
def encode_cvar(s):
    return ''.join([f'{ord(c) ^ 0x79:02X}' for c in s])

cvars_to_set = [
    'r.UserQualitySetting=4',
    'r.UserHDRSetting=2',
    'r.MobileHDR=1.0',
    'r.Mobile.SceneColorFormat=2.0',
    'r.Mobile.TonemapperFilm=1.0',
    'r.BloomQuality=1.0',
    'r.LightShaftQuality=1.0',
    'r.ShadowQuality=1',
    'r.MobileContentScaleFactor=2.0',
    'r.MaterialQualityLevel=2',
    'r.MobileSimpleShader=0'
]

ini_path = r'C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1899'
if os.path.exists(ini_path):
    with open(ini_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Prepend or append our custom CVars
    new_cvars = [f'+CVars={encode_cvar(c)}\n' for c in cvars_to_set]
    
    # Build updated UserCustom.ini
    out_lines = []
    in_user_custom = False
    added = False
    for line in lines:
        out_lines.append(line)
        if line.strip() == '[UserCustom DeviceProfile]':
            out_lines.extend(new_cvars)
            added = True
    
    if not added:
        out_lines.append('\n[UserCustom DeviceProfile]\n')
        out_lines.extend(new_cvars)
    
    with open(ini_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
    print(f'Updated UserCustom.ini with {len(cvars_to_set)} HDR CVars.')

# Try pushing via ADB if emulator is active
try:
    adb = r'C:\Program Files\TxGameAssistant\ui\adb.exe'
    subprocess.run([adb, 'connect', '127.0.0.1:5555'], capture_output=True, timeout=3)
    out = subprocess.run([adb, 'devices'], capture_output=True, text=True, timeout=3).stdout
    if '127.0.0.1:5555' in out:
        remote_base = '/sdcard/Android/data/com.tencent.ig/files/UE4Game/ShadowTrackerExtra/ShadowTrackerExtra/Saved'
        subprocess.run([adb, '-s', '127.0.0.1:5555', 'push', target_file, f'{remote_base}/SaveGames/Active.sav'], timeout=5)
        subprocess.run([adb, '-s', '127.0.0.1:5555', 'push', target_file, f'{remote_base}/SaveGames/SettingConfig_Slot.sav'], timeout=5)
        subprocess.run([adb, '-s', '127.0.0.1:5555', 'shell', f'chmod 777 {remote_base}/SaveGames/Active.sav'], timeout=5)
        print('ADB hot-push succeeded!')
    else:
        print('ADB not connected; rootfs files already synced on disk.')
except Exception as e:
    print('ADB push skipped:', e)
