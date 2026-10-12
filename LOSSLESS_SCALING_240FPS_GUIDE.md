# PUBG Mobile GameLoop: 200–240 FPS Lossless Scaling (LSFG) Master Guide

## 1. Overview: How High-FPS Streamers Achieve 240 FPS
In PUBG Mobile on GameLoop, Tencent's native engine (`libUE4.so`) caps physics simulation at **120 FPS** (`BattleFPS=8`).
To achieve **180Hz, 200 FPS, or 240 FPS motion fluidity**, professional streamers and competitive players use **Lossless Scaling (LSFG)**—an external AI Frame Generation utility running on the GPU (NVIDIA RTX 3090).

* **Input**: Rock-solid 120 FPS base output from GameLoop.
* **Output**: **240 FPS** via AI frame generation (`LSFG X2`) or **180 FPS** locked 1:1 to your 180Hz monitor!
* **Input Latency**: Zero additional queue delay; on the RTX 3090, intermediate frame synthesis takes **< 1.2 milliseconds**.
* **Safety**: **100% Ban-Safe**. It operates purely on the Windows desktop presentation layer without hooking into game memory, DLLs, or Tencent's anti-cheat.

---

## 2. Recommended Settings for NVIDIA GeForce RTX 3090 & 180Hz Monitor

Open **Lossless Scaling** (available on Steam) and configure the profile as follows:

### A. Frame Generation (The Core Engine)
| Setting | Recommended Value | Why |
| :--- | :--- | :--- |
| **Frame Generation** | **LSFG 3.1** (or LSFG 2.3) | State-of-the-art optical flow frame synthesis |
| **Mode** | **X2** (or Fixed Target) | Multiplies 120 native FPS into **240 FPS** |
| **Performance Mode** | **ON** | Drastically cuts GPU processing overhead to ~1.1ms |
| **Capture API** | **WGC** (Windows Graphics Capture) | Lowest latency capture API for GameLoop window |
| **Max Frame Latency** | **1** | Eliminates buffering latency |

### B. Scaling Type (Preserving 1080p Visual Clarity)
| Setting | Recommended Value | Why |
| :--- | :--- | :--- |
| **Scaling Type** | **Off** | Keep native 1080p UHD rendering sharp without extra upscaling blur |
| **Scaling Mode** | **Aspect Ratio** | Maintains exact 16:9 1920x1080 proportions |
| **Sharpness** | **0** (or 1 if you want extra crispness) | In-game textures are already high-res 3GB dynamic pool |

### C. Rendering & GPU
| Setting | Recommended Value | Why |
| :--- | :--- | :--- |
| **Preferred GPU** | **NVIDIA GeForce RTX 3090** | Utilizes the 24GB VRAM and dedicated Tensor cores |
| **Clip Cursor** | **ON** | Prevents mouse from slipping outside during rapid flicks |
| **Draw FPS** | **ON** (top-left or top-right) | Displays real-time base FPS and generated FPS (e.g. `120 / 240`) |

---

## 3. Step-by-Step Launch Workflow

1. **Step 1: Apply TAC Engine 180Hz / 240 FPS Optimization**:
   - Open `panel_loop_ultimate.bat` and select **Option [21]** (or click `⚡ 180Hz Monitor Sync` in GUI).
   - This sets `VMRefreshRate=180` (or `240`), uncaps UE4 to `t.MaxFPS=240`, removes thread lag (`r.OneFrameThreadLag=0`), and sets 240Hz mouse polling.

2. **Step 2: Launch GameLoop & PUBG Mobile**:
   - Launch PUBG Mobile.
   - Enter Cheer Park or Training Grounds to confirm your base framerate is pinned at **120 FPS**.

3. **Step 3: Activate Lossless Scaling**:
   - Open Lossless Scaling.
   - Click the **Scale** button (or press hotkey `Ctrl + Alt + S`).
   - You have **5 seconds** to click onto the GameLoop window.
   - Once hooked:
     - The top-corner counter will display: **`120 / 240` FPS**!
     - Motion becomes ultra-fluid, matching or exceeding 180Hz–240Hz monitor panels with zero stutter.

---

## 4. Pro Tips for 180Hz Monitor Owners
* If your physical panel is **180Hz**, you can either:
  1. Let LSFG output **240 FPS** with **G-Sync/FreeSync VRR** active (the monitor smoothly presents the fastest available scans with minimum tear).
  2. Set a frame rate limit of **180 FPS** in NVIDIA Control Panel (`Max Frame Rate = 180`) for perfect 1:1 hardware synchronization with zero frame drops.
* Keep **VSync OFF** in GameLoop to prevent compositor wait cycles.
* Run in **True Fullscreen (F11)** or **Streamer Mode (Option 11)** for zero DWM desktop compositing delay.
