# PANEL LOOP ULTIMATE 🚀
### Esports-Grade GameLoop & PUBG Mobile Full-Stack Optimization Suite

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://microsoft.com/windows)
[![Architecture](https://img.shields.io/badge/GameLoop-Android%2013%2064--Bit%20%7C%20AOW%2032--Bit-success.svg)](https://gameloop.com)
[![Status](https://img.shields.io/badge/Ban--Safe-100%25%20Client--Side-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**PANEL LOOP ULTIMATE** is a comprehensive, low-level optimization and latency tuning suite engineered specifically for **GameLoop (Android 13 64-Bit Celadon & AOW 32-Bit)** and **PUBG Mobile (`com.tencent.ig`)**. 

It eliminates emulator micro-stutters, uncaps framerates, synchronizes 120 FPS Ultra HD in-game profiles, enforces sub-millisecond Windows kernel timer pacing, eliminates SMT thread scheduling thrashing on AMD Ryzen & Intel CPUs, and guarantees true 1:1 raw hardware mouse sensor tracking.

---

## ⚡ Core Features

### 1. 🎮 120 FPS & Ultra HD Sync (Active.sav & SettingConfig_Slot.sav)
- Direct ADB hot-push to `/sdcard/Android/data/com.tencent.ig/files/UE4Game/...`
- Patches in-game GVAS save states to `BattleFPS = 8` (120 FPS tier) and `BattleRenderQuality = 6` (Ultra HD).
- Synchronizes GameLoop Settings Center UI radio buttons to 90 FPS with active synchronization.

### 2. 🏎️ Uncapped UE4 Engine Pipeline (UserCustom.ini)
- **Uncapped Frame Rate**: `t.MaxFPS = 0` (Removes engine render loop clamps).
- **Zero Thread Lag**: `r.OneFrameThreadLag = 0` (Zero compositor frame queuing, enabling esports-grade 1:1 flick tracking).
- **2 GB Dynamic Texture Pool**: `r.Streaming.PoolSize = 2048` (Stops in-match LOD pop-in and texture streaming stutter).
- **Explosion & Smoke Stability**: Caps particles to 500 max per emitter with LOD bias 1 (`fx.MaxCPUParticlesPerEmitter = 500`).
- **Paced Garbage Collection**: Purges dead objects every 60 seconds (`gc.TimeBetweenPurgingPendingKillObjects = 60`).

### 3. 📱 Esports Device Profile Whitelisting
- Pre-configured profiles for **ASUS ROG Phone 8 Pro (`ASUS_AI2401_A`)**, **REDMAGIC 9 Pro (`NX769J`)**, and **Samsung Galaxy S24 Ultra**.
- Direct injection into `Androws.json` and guest Android 13 system properties (`ro.product.model`).
- Configures low-overhead hardware OpenGL transport (`useLocalOpengl = true`, `glTransport = "wormhole"`).

### 4. ⏱️ 0.50ms Kernel Timer & Host Pacing
- Locks Windows kernel timer resolution to **0.50 ms** via native `NtSetTimerResolution` & `timeBeginPeriod`.
- Sets scheduler quantum to `Win32PrioritySeparation = 0x26` (3:1 foreground priority boost).
- Elevates live emulator processes (`GameLoopEmulator.exe`, `GameLoopVm.exe`, `GameLoop.exe`, `adb.exe`) to **High Priority Class**.
- Enforces **Physical Core Affinity (`0x5555`)** for AMD Ryzen 7 5800X / 7000 / 9000 series, completely bypassing SMT thread scheduling latency.

### 5. 🎯 DirectX Direct Scanout (Independent Flip)
- Injects `~ DISABLEDXMAXIMIZEDWINDOWEDMODE HIGHDPIAWARE` into `AppCompatFlags\Layers`.
- Enables borderless DWM Direct Scanout for sub-millisecond display presentation.
- Direct GPU routing for NVIDIA RTX / AMD Radeon graphics cards via `UserGpuPreferences`.

### 6. 🌐 Multi-NIC 0ms Hit-Reg & Network Turbo
- Disables Nagle's algorithm (`TcpAckFrequency = 1`, `TCPNoDelay = 1`) across all physical and virtual network adapters.
- Elevates Windows Multimedia Class Scheduler Service (MMCSS) game and network priority to realtime.

### 7. 🧹 Multi-Tier Deep Clean & Forensic Uninstaller
- Multi-tier cache purge: shader caches, component dump files, installer residues, and DNS flushing.
- Automated forensic uninstaller script (`execute_full_gameloop_purge.py`) that terminates all emulator processes, unregisters services (`GameLoopService`), unloads virtualization drivers (`GLABoxSup`), and cleans registry trees.

---

## 🖥️ Graphical Dashboard & CLI Menu

The suite includes three flexible ways to run:

1. **Interactive Batch Launcher**:
   ```cmd
   panel_loop_ultimate.bat
   ```
2. **Modern Dark-Mode Python Dashboard**:
   ```cmd
   python tac_gui.py
   ```
3. **Command-Line Interface (Automation & Scripting)**:
   ```cmd
   python tac_engine.py --status
   python tac_engine.py --optimize
   python tac_engine.py --pacing
   python tac_engine.py --clean
   python tac_engine.py --turbo
   ```

---

## 📂 Repository Structure

```text
panel-loop-ultimate/
├── panel_loop_ultimate.bat             # Master Windows batch launcher & interactive menu
├── tac_engine.py                       # Core low-level optimization & diagnostic engine
├── tac_gui.py                          # Modern dark-mode graphical desktop dashboard
├── tac_ultimate_panel.pyw              # Standalone windowed GUI panel
├── apply_new_gameloop_optimizations.py # GameLoop 7.0/8.0 (Android 13 64-Bit) setup script
├── execute_full_gameloop_purge.py     # Forensic uninstaller and deep purge utility
├── patch_active_sav.py                 # Standalone UE4 Active.sav GVAS patcher
├── LOSSLESS_SCALING_240FPS_GUIDE.md    # 240 FPS frame generation & pacing guide
└── README.md                           # Documentation
```

---

## 🔒 Ban Safety & Integrity

- **100% Ban-Safe**: Panel Loop Ultimate operates strictly through official client configuration files (`UserCustom.ini`, `Active.sav`), standard Android system properties, and external Windows OS scheduling APIs.
- **No Memory Injections**: Never injects DLLs, never hooks game code, never modifies executable memory.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
