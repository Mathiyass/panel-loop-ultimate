# Implementation Plan: Fix PUBG Mobile In-Game Graphics Rendering & Low-LOD Textures

Fix the issue where in-game graphics and textures are not rendering properly (clay rocks, flat green ground without grass blades, low-poly vehicle models, blurry textures) despite the game displaying the **`Ultra HD`** watermark badge on an **AMD Ryzen 7 5800X + NVIDIA GeForce RTX 3090 (24GB)** system.

---

## 🔍 Root Cause Analysis (From Video & Screenshot Investigation)

After analyzing [`ui Screenshot 2026.10.09 - 19.09.38.80.png`](file:///C:/Users/MATHIYA/Videos/NVIDIA/ui/ui%20Screenshot%202026.10.09%20-%2019.09.38.80.png) and [`ui 2026.10.09 - 19.08.26.01.mp4`](file:///C:/Users/MATHIYA/Videos/NVIDIA/ui/ui%202026.10.09%20-%2019.08.26.01.mp4), alongside deep inspection of GameLoop's rendering logs, filesystem inodes, and config files, **4 distinct root causes** were discovered:

```mermaid
flowchart TD
    subgraph RootCauses ["Root Causes for Clay Rocks & Missing Textures"]
        RC1["1. opengl.conf Missing Entry<br/>GameLoop emulated ARM Mali-G76 instead of Adreno.<br/>UE4 throttles Mali GPUs to potato tier."]
        RC2["2. Unpatched Inode 21\\8661<br/>Actual mounted UserCustom.ini had r.UserEnergySaving=1<br/>and 0 Streaming Pool Size."]
        RC3["3. In-Game Ultra HD Pack Missing<br/>Rootfs only contains res_basetexmd (Medium).<br/>HD/UHD texture PAKs must be downloaded in-game."]
        RC4["4. Outdated Shader Cache<br/>Old shader blobs compiled for Mali-G76 in ShaderCache."]
    end

    subgraph Solutions ["Targeted Fix Architecture"]
        S1["Inject Adreno 750 + ASTC HDR into opengl.conf"]
        S2["Deploy Desktop CVar Profile to Inode 21\\8661"]
        S3["Purge ShaderCache for Clean Recompilation"]
        S4["Verify/Download UHD Resource Pack in PUBG Lobby"]
    end

    RC1 --> S1
    RC2 --> S2
    RC4 --> S3
    RC3 --> S4
```

### 1. GameLoop Emulating `ARM Mali-G76` Instead of Flagship Adreno
- In [`libOpenglRenderV3.log`](file:///C:/Program%20Files/TxGameAssistant/ui/libOpenglRenderV3.log):
  ```
  GL Vendor: ARM
  GL Renderer: Mali-G76
  GL Extensions: OpenGL ES 3.0.0 (ANGLE)
  testTextureCodecPerf: Could not create GLES 2.x Context! error=0x3004
  ```
- In [`opengl.conf`](file:///C:/Program%20Files/TxGameAssistant/ui/opengl.conf), GameLoop had **no renderer definition** for `com.tencent.ig` (PUBG Mobile Global), causing it to fall back to `ARM Mali-G76`.
- In Unreal Engine 4's `BaseDeviceProfiles.ini`, Mali GPUs are hard-coded to a restricted low-end rendering tier to avoid mobile driver crashes:
  - 3D foliage (grass blades) is completely disabled $\rightarrow$ produces flat green ground.
  - Texture streaming pool is throttled to 300MB $\rightarrow$ high-res mipmaps never stream in.
  - StaticMesh LOD distance is clamped $\rightarrow$ rocks and cars render at LOD 3/4 (clay blobs).

### 2. Active Rootfs Inode `21\8661` Had Not Received the Desktop CVars
- Directory inode `6\1895` maps `UserCustom.ini` directly to `21\8661`.
- Inspecting `21\8661` revealed it was still running old mobile power-saving parameters:
  - `r.UserEnergySaving=1` *(forces battery conservation and low texture resolution)*
  - `ParticleLODBias=2` *(lowest particle quality)*
  - `r.Streaming.PoolSize` was unset *(default 300MB)*
  - `r.MaterialQualityLevel` was unset
  - `foliage.LODDistanceScale` was unset
  - `r.StaticMeshLODDistanceScale` was unset

### 3. High-Definition Texture Packs (`res_basetexhd.pak`, `res_maptexhd.pak`)
- Inode `6\1957` (the active game `Paks` directory) contains `res_basetexmd` (Medium) and `res_maptexmd` (Medium).
- The base APK installation does not include 4K/HD assets out of the box. Even when `BattleRenderQuality: 6` (Ultra HD) is selected in `Active.sav`, if the **"Ultra HD Resource Pack"** or **"HD Graphics Pack"** is not downloaded in the in-game Download Center, the game has no high-res textures to load and must fall back to low-resolution base textures.

---

## 🛠️ Proposed Changes

### Component 1: GameLoop GPU Emulation (`opengl.conf`)

#### [MODIFY] [`C:\Program Files\TxGameAssistant\ui\opengl.conf`](file:///C:/Program%20Files/TxGameAssistant/ui/opengl.conf) & [`C:\Program Files\TxGameAssistant\ui\ConfigFile\opengl.conf`](file:///C:/Program%20Files/TxGameAssistant/ui/ConfigFile/opengl.conf)
Inject Qualcomm Adreno flagship profile and ASTC HDR texture compression extensions for `com.tencent.ig`:
```ini
com.tencent.ig_GL_RENDERER=Adreno (TM) 750
com.tencent.ig_GL_VENDOR=Qualcomm
com.tencent.ig_GL_EXTENSIONS_TO_ADD_DX=GL_KHR_texture_compression_astc_ldr GL_KHR_texture_compression_astc_hdr GL_EXT_texture_buffer
com.tencent.ig_HW_SCORE_CONFIG=5000,3500,4000,700,7500,3500
```
*Effect: GameLoop's ANGLE engine presents itself as a Qualcomm Adreno 750 (Snapdragon 8 Gen 3) with full ASTC HDR hardware texture decompression enabled directly on the RTX 3090.*

---

### Component 2: Active Rootfs Inode `21\8661` (`UserCustom.ini`)

#### [MODIFY] [`C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\8661`](file:///C:/Program%20Files/TxGameAssistant/AOW_Rootfs_100/21/8661)
Also ensure all candidate inodes (`1b\6edd`, `12\485c`, `6\1899`, `21\8661`, `MobileGamePCShared\UserCustom.ini`) are synchronized with:
- `r.PUBGVersion=5`
- `r.UserQualitySetting=6` (Tier 6 True Ultra HD)
- `r.MaterialQualityLevel=3` (Epic Materials)
- `r.MaterialQualitySuperHigh=1.0`
- `r.Streaming.PoolSize=4096` (4 GB dedicated texture pool)
- `r.Streaming.FullyLoadUsedTextures=1` (Forces full mipmaps)
- `r.Streaming.MipBias=0` (Zero blur mip bias)
- `r.MaxAnisotropy=16` (16x anisotropic filtering)
- `r.StaticMeshLODDistanceScale=2.0` (Forces maximum LOD on rocks and buildings)
- `foliage.LODDistanceScale=2.0` (Pushes grass blade rendering distance out)
- `foliage.DensityScale=1.0` (Full 3D grass density)
- `r.UserEnergySaving=0` (Disables power-saving throttling)
- `r.DetailMode=2` (High detail mode)
- `r.ShadowQuality=2`
- `r.Shadow.MaxCSMResolution=2048`

---

### Component 3: Purge Shader Cache for Fresh Compilation

#### [DELETE] [`C:\Program Files\TxGameAssistant\ui\ShaderCache\*`](file:///C:/Program%20Files/TxGameAssistant/ui/ShaderCache)
- Delete all `.bin2` files compiled under the previous `Mali-G76` profile.
- On next launch, GameLoop will recompile clean DirectX 11/12 shaders for the `Adreno 750` profile with zero legacy artifacts.

---

### Component 4: Update GUI Panel and Scripts

#### [MODIFY] [`tac_ultimate_panel.pyw`](file:///C:/Users/MATHIYA/Documents/saasassasa/tac_ultimate_panel.pyw) & [`Panel_Loop_Ultimate.bat`](file:///C:/Users/MATHIYA/Desktop/Panel_Loop_Ultimate.bat)
- Add inode `21\8661` to `INI_INODES`.
- Add automatic `opengl.conf` Adreno 750 reinforcement to the optimization routines.

---

## 🧪 Verification Plan

### Automated Verification
1. Verify `opengl.conf` contains `com.tencent.ig_GL_RENDERER=Adreno (TM) 750`.
2. Verify inode `21\8661` contains encoded CVars for `r.Streaming.PoolSize=4096`, `r.StaticMeshLODDistanceScale=2.0`, and `foliage.LODDistanceScale=2.0`.
3. Verify `libOpenglRenderV3.log` reflects the new Adreno GPU profile upon launch.

### Manual Verification
1. Launch PUBG Mobile via [**`TAC Ultimate Panel`**](file:///C:/Users/MATHIYA/Desktop/TAC%20Ultimate%20Panel.lnk) or [**`AndroidEmulator - Shortcut.lnk`**](file:///C:/Users/MATHIYA/Desktop/AndroidEmulator%20-%20Shortcut.lnk).
2. In the PUBG Mobile Lobby, click the **Download Center** icon (arrow/cloud icon).
3. Ensure the **"Ultra HD Resource Pack"** and **"Exciting / HD Resource Pack"** show **"Downloaded / 100%"**.
4. Enter Cheer Park / Training Ground:
   - Rocks should have visible stone crevices, normal maps, and realistic 3D textures.
   - Ground should have distinct 3D grass blades instead of a flat green smear.
   - Cars (Dacia, buggy) should render high-poly geometry and clear headlight/wheel textures.
   - Framerate remains locked at 120 FPS.
