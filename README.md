# ⚡ MATHIYA GAMELOOP PANEL v4.3
### Universal Esports-Grade GameLoop & PUBG Mobile Full-Stack Optimization Suite
#### *Streamer HDR 120 FPS Verified Edition (Mathiya Tournament Setup)*

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--Bit)-blue.svg)](https://microsoft.com/windows)
[![GameLoop](https://img.shields.io/badge/GameLoop-Chinese%2064--Bit%20%7C%20Global%2064--Bit%20%7C%20Global%2032--Bit-success.svg)](https://gameloop.com)
[![Status](https://img.shields.io/badge/Ban--Safe-100%25%20Client--Side-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v4.3.0%20Universal-cyan.svg)](https://github.com/Mathiyass/panel-loop-ultimate/releases)

---

## 🌟 What is Mathiya GameLoop Panel?

**Mathiya GameLoop Panel (Mathiya Tournament Setup)** is a professional, low-level optimization dashboard and kernel pacing engine designed for competitive PUBG Mobile and GameLoop players.

It eliminates combat micro-stutters, enables **Competitive Flat-Shaded Streamer Textures** (as used by top competitive streamers like MrBro to completely eliminate building pop-in and texture streaming hitching), locks framerates to **120 FPS**, synchronizes authentic **True HDR (Tier 5)** or **Flat-Streamer Smooth (Tier 1)**, enforces sub-millisecond (**0.50 ms**) Windows kernel timer pacing, optimizes network bullet hit-registration, and eliminates CPU core scheduling thrashing across **AMD Ryzen** and **Intel Core** processors.

---

## 🚀 Universal GameLoop Compatibility (All Versions Supported)

Mathiya GameLoop Panel dynamically detects and configures **all GameLoop versions and editions installed on any drive (`C:`, `D:`, `E:`, `F:`)**:

| GameLoop Edition | Rootfs Engine | Architecture | Package Support | Status |
| :--- | :--- | :--- | :--- | :--- |
| **GameLoop Chinese 64-Bit** | `AOW_Rootfs_100` | 64-Bit Celadon | All Packages | ✅ Fully Supported |
| **GameLoop Global 64-Bit** | `AOW_Rootfs_64` | 64-Bit Android 13 | All Packages | ✅ Fully Supported |
| **GameLoop Global 32-Bit** | `AOW_Rootfs` / Legacy | 32-Bit AOW | All Packages | ✅ Fully Supported |

### Supported Game Editions:
- 🌍 **Global**: `com.tencent.ig`
- 🇮🇳 **BGMI (Battlegrounds Mobile India)**: `com.pubg.imobile`
- 🇰🇷 **Korea / Japan**: `com.pubg.krmobile`
- 🇻🇳 **Vietnam**: `com.vng.pubgmobile`
- 🇹🇼 **Taiwan**: `com.reindex.tw`

---

## ⚡ Core Features

### 1. 🎨 True HDR + 120 FPS Master Synchronization
- **`GraphicFavor = 4` (Customize Mode)**: Strictly prevents the emulator fallback bug that forces the *Super Smooth* watermark when set incorrectly.
- **`BattleRenderQuality = 5`**: Activates true in-game HDR shading with full PBR building textures.
- **2048 MB Dynamic Texture Pool**: `r.Streaming.PoolSize = 2048` guarantees immediate LOD streaming without building pop-in or stutter.
- **Zero Unreal Engine 4 Limiter Clamps**: `t.MaxFPS = 0` and `r.OneFrameThreadLag = 0` for zero thread delay and 1:1 flick tracking.

### 2. ⏱️ 0.50ms Kernel Timer & Universal CPU Pacing
- Sub-millisecond timer resolution locked to **0.50 ms** via native Win32 `NtSetTimerResolution`.
- **Dynamic CPU Topology Engine**: Automatically detects CPU core count and threads.
  - **AMD Ryzen**: Enforces physical core affinity (`0x5555` on 8-core, `0x0555` on 6-core, `0x555555` on 12-core) to bypass SMT cross-thread latency penalties.
  - **Intel Core**: Supports auto-detecting physical performance cores (P-cores) or all logical cores.
- **High Process Priority**: Sets `HIGH_PRIORITY_CLASS (0x80)` for `aow_exe.exe` and `AndroidEmulatorEx.exe`.

### 3. 🌐 Native Win32 DNS Flush & Hit-Registration Accelerator
- **Instant DNS Cache Flush**: Calls `dnsapi.dll!DnsFlushResolverCache` directly in memory with **zero console popups or CMD flashes**.
- **Nagle's Algorithm Disabling**: Forces `TCPNoDelay = 1` and `TcpAckFrequency = 1` across all network adapters for immediate packet transmission.
- **Network Throttling Elimination**: `NetworkThrottlingIndex = 0xFFFFFFFF` and `SystemResponsiveness = 0`.
- **Zero Hitbox Interp Lag**: `p.NetInterpolation = 0.0` and `net.MaxClientTickRate = 120` to prevent ghost bullets.

### 4. 🧹 Standby RAM & DirectX Shader Purger
- One-click memory cleaner trimming background bloat (Discord, Edge, Chrome, SearchHost) via `psapi.dll!EmptyWorkingSet`.
- Cleans corrupted temporary DirectX shader cache files (`D3DSCache`) to eliminate hot-drop frame drops.

### 5. 🎯 1:1 Raw Linear Mouse Aim
- Disables Windows pointer acceleration curves (`MouseSpeed = 0`, `MouseThreshold = 0`).
- Synchronizes 120Hz collision capsule friction checks (running every 8.33 ms instead of 25.0 ms).

### 6. 📌 Draggable In-Game Floating Mini-HUD
- Translucent acrylic glass overlay displaying real-time Kernel Timer, locked profile, and free RAM.
- Contains one-click in-game `⚡ QUICK BOOST` and `🧹 PURGE RAM` recovery buttons.

### 7. 🛡️ Authentic Anti-Cheat Integrity
- Guaranteed authentic Tencent signed `AEngine.dll` binary verification (prevents TP Error 11102).

---

## 📥 Downloads & Installation

### Option 1: Standalone Portable Executable (Recommended)
> Download [`Mathiya_GameLoop_Panel_Portable.exe`](https://github.com/Mathiyass/panel-loop-ultimate/releases) from Releases, place it anywhere, and double-click to run. No installation or extraction required!

### Option 2: Setup ZIP Package
> Download [`Mathiya_GameLoop_Panel_v4.0_Setup.zip`](https://github.com/Mathiyass/panel-loop-ultimate/releases) from Releases. Extract anywhere and run `Run_Mathiya_GameLoop_Panel.vbs` for silent background execution with the custom desktop icon.

---

## 🎮 How to Use

1. Launch **Mathiya GameLoop Panel**.
2. Select your Game Version (Global, BGMI, KR, VN, TW) from the sidebar.
3. Select your Profile (e.g., `🏆 Tournament HDR 120` or `⚡ Streamer Smooth 120`).
4. Click **⚡ APPLY TRUE HDR 120 FPS (MATHIYA TOURNAMENT SETUP)**.
5. Click **🎮 LAUNCH GAMELOOP** and enjoy locked 120 FPS with zero lag!

---

## 🔒 Ban Safety & Integrity

- **100% Client-Side Safe**: Mathiya GameLoop Panel operates strictly through official client configuration files (`UserCustom.ini`, `Active.sav`), standard Android system properties, and external Windows OS scheduling APIs.
- **No Injections / No Memory Hooks**: Never modifies game executable code, never injects DLLs into the game process.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.
