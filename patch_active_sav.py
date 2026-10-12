import struct
import os

source_file = r'C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav.bak'
target_file = r'C:\Temp\TxGameDownload\MobileGamePCShared\Active.sav'

with open(source_file, 'rb') as f:
    buf = bytearray(f.read())

print(f'Original file length: {len(buf)} bytes')

# Map of properties to modify: key -> new value (DWORD)
targets = {
    'FPSLevel': 8,              # 8 = 120 FPS
    'BattleFPS': 8,             # 8 = 120 FPS
    'LobbyFPS': 8,              # 8 = 120 FPS
    'MainCityFPS': 8,           # 8 = 120 FPS
    'BattleRenderQuality': 1,   # 1 = Smooth
    'LobbyRenderQuality': 1,    # 1 = Smooth
    'GFBestQLobby': 1,          # Smooth
    'GFBestQBattle': 1          # Smooth
}

modified_count = 0
for prop_name, new_val in targets.items():
    prefix = prop_name.encode('latin1') + b'\x00\x0c\x00\x00\x00IntProperty\x00'
    pos = buf.find(prefix)
    if pos != -1:
        # Offset calculation:
        # prefix length + 4 bytes (len of data = 4) + 4 bytes (array index = 0) + 1 byte (null separator) = 9 bytes
        val_offset = pos + len(prop_name) + 1 + 4 + 12 + 9
        old_val = struct.unpack('<I', buf[val_offset:val_offset+4])[0]
        buf[val_offset:val_offset+4] = struct.pack('<I', new_val)
        print(f'Successfully patched {prop_name}: {old_val} -> {new_val} at offset {val_offset}')
        modified_count += 1
    else:
        print(f'WARNING: Property {prop_name} not found!')

with open(target_file, 'wb') as f:
    f.write(buf)

print(f'Modified {modified_count} properties.')
print(f'Wrote patched file to {target_file} ({os.path.getsize(target_file)} bytes).')
