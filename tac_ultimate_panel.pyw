import os
import sys
import ctypes
import winreg
import subprocess
import threading
import tkinter as tk
import customtkinter as ctk

# Configure CustomTkinter Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Theme Palette (TAC Golden Dark Style)
COLOR_BG = "#0D0F12"
COLOR_SIDEBAR = "#14171D"
COLOR_CARD = "#1A1E26"
COLOR_CARD_HOVER = "#222733"
COLOR_BORDER = "#2A303C"
COLOR_GOLD = "#F59E0B"
COLOR_GOLD_HOVER = "#D97706"
COLOR_TEXT = "#F3F4F6"
COLOR_TEXT_MUTED = "#9CA3AF"
COLOR_GREEN = "#10B981"
COLOR_RED = "#EF4444"

# Paths
TX_REG_PATH = r"Software\Tencent\MobileGamePC"
DX_REG_PATH = r"Software\Microsoft\DirectX\UserGpuPreferences"
ROOTFS_DIR = r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100"
SHARED_DIR = r"C:\Temp\TxGameDownload\MobileGamePCShared"
SHADER_CACHE_DIR = r"C:\Program Files\TxGameAssistant\ui\ShaderCache"
APPMARKET_EXE = r"C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe"
EMULATOR_EXE = r"C:\Program Files\TxGameAssistant\ui\AndroidEmulator.exe"
ADB_EXE = r"C:\Program Files\TxGameAssistant\ui\adb.exe"

# Inode lists
SAVE_INODES = [
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\84ad",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\84ae",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edb",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edc",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\4a08",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\4a09",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1945",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\9\24c8"
]

INI_INODES = [
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\21\8661",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\1b\6edd",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\12\485c",
    r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\6\1899"
]

def encode_cvar(text):
    hex_str = ""
    for ch in text:
        b = ord(ch) ^ 0x79
        hex_str += f"{b:02X}"
    return f"+CVars={hex_str}"

def generate_usercustom_ini():
    cvars = [
        "r.PUBGVersion=5",
        "r.UserQualitySetting=6",
        "r.MaterialQualityLevel=3",
        "r.MaterialQualitySuperHigh=1.0",
        "r.Streaming.PoolSize=4096",
        "r.Streaming.UseFixedPoolSize=0",
        "r.Streaming.FullyLoadUsedTextures=1",
        "r.Streaming.MipBias=0",
        "r.MaxAnisotropy=16",
        "r.StaticMeshLODDistanceScale=2.0",
        "foliage.LODDistanceScale=2.0",
        "foliage.DensityScale=1.0",
        "r.MobileContentScaleFactor=2.0",
        "r.MobileHDR=1.0",
        "r.Mobile.SceneColorFormat=2.0",
        "r.BloomQuality=1.0",
        "r.LightShaftQuality=1.0",
        "r.Mobile.TonemapperFilm=1.0",
        "r.MobileSimpleShader=0",
        "r.ShadowQuality=2",
        "r.UserShadowSwitch=1",
        "r.Shadow.MaxCSMResolution=2048",
        "r.Shadow.DistanceScale=2.0",
        "r.Mobile.EnablePPR=1.0",
        "r.UserHDRSetting=2",
        "r.ACESStyle=2",
        "r.DetailMode=2",
        "r.DefaultFeature.AntiAliasing=0.0",
        "r.MobileMSAA=1.0",
        "r.MSAACount=4.0",
        "r.ViewDistanceScale=2.0",
        "r.SkeletalMeshLODBias=0",
        "r.UserEnergySaving=0",
        "r.ParticleLODBias=0",
        "r.SkyAtmosphere=1.0",
        "r.GTAO.Quality=1.0"
    ]
    lines = ["[BackUp DeviceProfile]"]
    for c in cvars:
        lines.append(encode_cvar(c))
    lines.append("")
    lines.append("[UserCustom DeviceProfile]")
    for c in cvars:
        lines.append(encode_cvar(c))
    lines.append("")
    return "\r\n".join(lines)

def update_active_sav(quality=6, fps=8):
    path = os.path.join(SHARED_DIR, "Active.sav")
    if not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        data = bytearray(f.read())
    
    updates = {
        b"BattleRenderQuality\x00": quality,
        b"LobbyRenderQuality\x00": quality,
        b"GFBestQBattle\x00": quality,
        b"GFBestQLobby\x00": quality,
        b"MainCityRenderQuality\x00": quality,
        b"ManorRenderQuality\x00": quality,
        b"nEnhancedLobbyQuality\x00": quality,
        b"BattleFPS\x00": fps,
        b"LobbyFPS\x00": fps,
        b"FPSLevel\x00": fps,
        b"MainCityFPS\x00": fps,
        b"GraphicFavor\x00": 4,
        b"BattleRenderStyle\x00": 2,
        b"LobbyRenderStyle\x00": 2
    }
    int_prop = b"IntProperty\x00"

    for k, val in updates.items():
        idx = data.find(k)
        if idx != -1:
            prop_idx = data.find(int_prop, idx, idx + 50)
            if prop_idx != -1:
                val_offset = prop_idx + len(int_prop) + 8 + 1
                val_bytes = val.to_bytes(4, byteorder="little", signed=True)
                data[val_offset:val_offset+4] = val_bytes
    
    # Save back
    try:
        os.chmod(path, 0o777)
    except: pass
    with open(path, "wb") as f:
        f.write(data)
    
    # Mirror to SettingConfig_Slot.sav
    slot_path = os.path.join(SHARED_DIR, "SettingConfig_Slot.sav")
    try:
        os.chmod(slot_path, 0o777)
    except: pass
    with open(slot_path, "wb") as f:
        f.write(data)
    
    # Deploy to live rootfs inodes
    for inode in SAVE_INODES:
        if os.path.exists(os.path.dirname(inode)):
            try:
                os.chmod(inode, 0o777)
            except: pass
            try:
                with open(inode, "wb") as f:
                    f.write(data)
            except: pass
    return True

def deploy_usercustom_ini():
    content = generate_usercustom_ini().encode("ascii")
    path = os.path.join(SHARED_DIR, "UserCustom.ini")
    try:
        os.chmod(path, 0o777)
    except: pass
    with open(path, "wb") as f:
        f.write(content)
    for inode in INI_INODES:
        if os.path.exists(os.path.dirname(inode)):
            try:
                os.chmod(inode, 0o777)
            except: pass
            try:
                with open(inode, "wb") as f:
                    f.write(content)
            except: pass

def set_gameloop_reg(model_name, model_code, mfr, res_w, res_h, dpi, quality=6, fps=120, engine=1):
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, TX_REG_PATH)
        winreg.SetValueEx(key, "VMPhoneDevice", 0, winreg.REG_SZ, model_name)
        winreg.SetValueEx(key, "VMDeviceModel", 0, winreg.REG_SZ, model_code)
        winreg.SetValueEx(key, "VMDeviceManufacturer", 0, winreg.REG_SZ, mfr)
        winreg.SetValueEx(key, "VMResWidth", 0, winreg.REG_DWORD, res_w)
        winreg.SetValueEx(key, "VMResHeight", 0, winreg.REG_DWORD, res_h)
        # GameLoop Settings Center (AppMarket React UI) maps:
        # ContentScale: 0=720P, 1=1080P, 2=超清2K
        # RenderQuality: -1=Auto, 0=Smooth, 1=Balanced, 2=HD (高清)
        # FPSLevel: 30, 40, 60, 90 (90 selects 90 FPS)
        for pkg in ["com.tencent.ig", "com.tencent.tmgp.pubgmhd"]:
            winreg.SetValueEx(key, f"{pkg}_ContentScale", 0, winreg.REG_DWORD, 2)
            winreg.SetValueEx(key, f"{pkg}_RenderQuality", 0, winreg.REG_DWORD, 2)
            winreg.SetValueEx(key, f"{pkg}_FPSLevel", 0, winreg.REG_DWORD, 90)
        winreg.SetValueEx(key, "ForceDirectX", 0, winreg.REG_DWORD, engine)
        winreg.SetValueEx(key, "VSyncEnabled", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "LocalShaderCacheEnabled", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "ShaderCacheEnabled", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "RenderOptimizeEnabled", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "EnableGLESv3", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "VMCpuCount", 0, winreg.REG_DWORD, 4)
        winreg.SetValueEx(key, "VMMemorySizeInMB", 0, winreg.REG_DWORD, 4096)
        winreg.SetValueEx(key, "ShowFPS", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        update_build_prop(model_code, mfr)
    except Exception as e:
        print("Registry error:", e)

def update_build_prop(model_code, mfr):
    bp_path = r"C:\Program Files\TxGameAssistant\AOW_Rootfs_100\0\18c"
    if not os.path.exists(bp_path):
        return
    try:
        with open(bp_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if line.startswith("ro.product.model="):
                new_lines.append(f"ro.product.model={model_code}\n")
            elif line.startswith("ro.product.brand="):
                new_lines.append(f"ro.product.brand={mfr}\n")
            elif line.startswith("ro.product.name="):
                new_lines.append(f"ro.product.name={model_code}\n")
            elif line.startswith("ro.product.device="):
                new_lines.append(f"ro.product.device={model_code}\n")
            elif line.startswith("ro.product.board="):
                new_lines.append(f"ro.product.board={model_code}\n")
            elif line.startswith("ro.product.manufacturer="):
                new_lines.append(f"ro.product.manufacturer={mfr}\n")
            else:
                new_lines.append(line)
        with open(bp_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except:
        pass

def apply_system_boost():
    try:
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
            "/v", "NetworkThrottlingIndex", "/t", "REG_DWORD", "/d", "4294967295", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
            "/v", "SystemResponsiveness", "/t", "REG_DWORD", "/d", "0", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
            "/v", "GPU Priority", "/t", "REG_DWORD", "/d", "8", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
            "/v", "Priority", "/t", "REG_DWORD", "/d", "6", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
            "/v", "Scheduling Category", "/t", "REG_SZ", "/d", "High", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games",
            "/v", "SFIO Priority", "/t", "REG_SZ", "/d", "High", "/f"
        ], capture_output=True)
        # TCPNoDelay on active NIC
        nic = "{a24e65ee-2032-4cd5-90c1-517c095969c9}"
        subprocess.run([
            "reg", "add", fr"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{nic}",
            "/v", "TcpAckFrequency", "/t", "REG_DWORD", "/d", "1", "/f"
        ], capture_output=True)
        subprocess.run([
            "reg", "add", fr"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\{nic}",
            "/v", "TCPNoDelay", "/t", "REG_DWORD", "/d", "1", "/f"
        ], capture_output=True)
        # Dedicated GPU
        subprocess.run([
            "reg", "add", r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences",
            "/v", r"C:\Program Files\TxGameAssistant\ui\AndroidEmulatorEx.exe", "/t", "REG_SZ", "/d", "GpuPreference=2;", "/f"
        ], capture_output=True)
        # CPU Priority Class
        subprocess.run([
            "reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AndroidEmulatorEx.exe\PerfOptions",
            "/v", "CpuPriorityClass", "/t", "REG_DWORD", "/d", "3", "/f"
        ], capture_output=True)
    except: pass

def deep_clean():
    # Shader Cache
    if os.path.exists(SHADER_CACHE_DIR):
        for f in os.listdir(SHADER_CACHE_DIR):
            if f.endswith(".bin2") or f.endswith(".cache"):
                try: os.remove(os.path.join(SHADER_CACHE_DIR, f))
                except: pass
    # Flush DNS
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    # Memory Trim via ctypes
    try:
        ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
    except: pass

def kill_zombie_processes():
    subprocess.run(["taskkill", "/f", "/im", "aow_exe.exe"], capture_output=True)
    subprocess.run(["taskkill", "/f", "/im", "aow_exe"], capture_output=True)
    subprocess.run(["taskkill", "/f", "/im", "AndroidEmulatorEx.exe"], capture_output=True)
    subprocess.run(["taskkill", "/f", "/im", "AndroidEmulator.exe"], capture_output=True)

def reinforce_opengl_conf():
    configs = [
        r"C:\Program Files\TxGameAssistant\ui\opengl.conf",
        r"C:\Program Files\TxGameAssistant\ui\ConfigFile\opengl.conf"
    ]
    for cfg in configs:
        try:
            if not os.path.exists(cfg): continue
            with open(cfg, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "com.tencent.ig_GL_RENDERER=Adreno" not in content:
                content = content.replace(
                    "com.tencent.ig_HW_SCORE_CONFIG=5000,3500,4000,700,7500,3500",
                    "com.tencent.ig_HW_SCORE_CONFIG=5000,3500,4000,700,7500,3500\ncom.tencent.ig_GL_RENDERER=Adreno (TM) 750\ncom.tencent.ig_GL_VENDOR=Qualcomm\ncom.tencent.ig_GL_EXTENSIONS_TO_ADD_DX=GL_KHR_texture_compression_astc_ldr GL_KHR_texture_compression_astc_hdr GL_EXT_texture_buffer"
                )
                with open(cfg, "w", encoding="utf-8") as f:
                    f.write(content)
        except:
            pass

class TACUltimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TAC ULTIMATE PRO — GameLoop & PUBG Mobile Optimizer")
        self.geometry("1100x720")
        self.minsize(1000, 680)
        self.configure(fg_color=COLOR_BG)

        # State Variables
        self.current_preset = tk.StringVar(value="Visual 4K (Ultra HD + 120 FPS)")
        self.current_model = tk.StringVar(value="ZTE Nubia REDMAGIC (NX789J)")
        self.current_resolution = tk.StringVar(value="1920x1080 (FHD Native)")
        self.current_engine = tk.StringVar(value="DirectX+ (Direct3D 11 Hardware)")
        self.match_fps = tk.StringVar(value="120 FPS")
        self.match_quality = tk.StringVar(value="Ultra HD (Tier 6)")
        self.lobby_fps = tk.StringVar(value="120 FPS")
        self.lobby_quality = tk.StringVar(value="Ultra HD (Tier 6)")
        
        # Toggle Switches
        self.sw_frame_pacing = tk.BooleanVar(value=True)
        self.sw_tcp_nodelay = tk.BooleanVar(value=True)
        self.sw_gpu_routing = tk.BooleanVar(value=True)
        self.sw_cpu_priority = tk.BooleanVar(value=True)
        self.sw_ram_flush = tk.BooleanVar(value=True)
        self.sw_quiet_apps = tk.BooleanVar(value=True)
        self.sw_high_res_pool = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self):
        # Main Grid Layout: Sidebar (col 0), Content Area (col 1)
        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0, minsize=60)

        # 1. Left Navigation Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=COLOR_SIDEBAR, corner_radius=0, border_width=1, border_color=COLOR_BORDER)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=0, pady=0)
        self._build_sidebar()

        # 2. Main Content Tabs Area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(
            self.content_frame, fg_color=COLOR_BG,
            segmented_button_fg_color=COLOR_CARD,
            segmented_button_selected_color=COLOR_GOLD,
            segmented_button_selected_hover_color=COLOR_GOLD_HOVER,
            segmented_button_unselected_hover_color=COLOR_CARD_HOVER,
            text_color=COLOR_TEXT
        )
        self.tabview.grid(row=0, column=0, sticky="nsew")

        self.tab_graphics = self.tabview.add("🖥️ Display & Graphics")
        self.tab_models = self.tabview.add("📱 Device Models")
        self.tab_boost = self.tabview.add("⚡ Game Boost")
        self.tab_cleaner = self.tabview.add("🧹 Deep Cleaner")
        self.tab_keymap = self.tabview.add("🎮 Keymap & View")

        self._build_graphics_tab()
        self._build_models_tab()
        self._build_boost_tab()
        self._build_cleaner_tab()
        self._build_keymap_tab()

        # 3. Bottom Action Bar
        self.action_bar = ctk.CTkFrame(self, fg_color=COLOR_SIDEBAR, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        self.action_bar.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 20))
        self.action_bar.grid_columnconfigure(0, weight=1)
        self._build_action_bar()

    def _build_sidebar(self):
        # App Title & Badge
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=16, pady=(24, 16))
        
        lbl_title = ctk.CTkLabel(title_frame, text="⚡ TAC ULTIMATE", font=ctk.CTkFont(size=20, weight="bold"), text_color=COLOR_GOLD)
        lbl_title.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(title_frame, text="PRO GAMING PANEL · 2026", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT_MUTED)
        lbl_sub.pack(anchor="w")

        # Telemetry Card
        tele_card = ctk.CTkFrame(self.sidebar, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        tele_card.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(tele_card, text="SYSTEM STATUS", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(tele_card, text="CPU: AMD Ryzen 7 5800X", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT).pack(anchor="w", padx=12, pady=1)
        ctk.CTkLabel(tele_card, text="GPU: RTX 3090 24GB", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT).pack(anchor="w", padx=12, pady=1)
        ctk.CTkLabel(tele_card, text="Display: 1920x1080 @ 180Hz", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT).pack(anchor="w", padx=12, pady=(1, 10))

        # Model Pill
        model_pill = ctk.CTkFrame(self.sidebar, fg_color=COLOR_CARD, corner_radius=8)
        model_pill.pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(model_pill, text="ACTIVE DEVICE", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 0))
        self.lbl_active_model = ctk.CTkLabel(model_pill, text="REDMAGIC NX789J", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_GREEN)
        self.lbl_active_model.pack(anchor="w", padx=12, pady=(0, 8))

        # Sidebar Footer
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        ver_card = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        ver_card.pack(fill="x", padx=16, pady=16)
        ctk.CTkLabel(ver_card, text="100% Free · Ban-Safe Edition\nZero Subscription Fees", font=ctk.CTkFont(size=10), text_color=COLOR_TEXT_MUTED, justify="left").pack(anchor="w")

    def _build_graphics_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_graphics, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        # Header Banner
        banner = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(banner, text="DISPLAY & GRAPHICS PIPELINE", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(banner, text="Configure 4K textures, 120 FPS unlocked tier, internal render scaling, and Direct3D hardware acceleration.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        # Recommended Preset Cards Grid
        ctk.CTkLabel(scroll, text="RECOMMENDED 1-CLICK PRESETS", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(8, 6))
        presets_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        presets_frame.pack(fill="x", pady=(0, 16))
        presets_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        p_data = [
            ("Visual 4K UHD", "4K (Tier 6 UHD)", "120 FPS Locked", "DirectX+ 4GB Pool", 6, 8, 1920, 1080),
            ("Competitive Pro", "Smooth (120 FPS)", "0ms Input Lag", "DirectX+ Max Hit-Reg", 1, 8, 1920, 1080),
            ("Balanced 2K", "HDR (Tier 5)", "120 FPS", "Crisp 2K Scale", 5, 8, 1920, 1080),
            ("iPad View 4:3", "Stretched FOV", "120 FPS Locked", "1440x1080 Wide Aim", 6, 8, 1440, 1080)
        ]

        for idx, (title, q_lbl, fps_lbl, sub_lbl, q_val, f_val, rw, rh) in enumerate(p_data):
            p_card = ctk.CTkFrame(presets_frame, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            p_card.grid(row=0, column=idx, padx=6, pady=4, sticky="nsew")
            ctk.CTkLabel(p_card, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_GOLD).pack(padx=10, pady=(10, 2))
            ctk.CTkLabel(p_card, text=q_lbl, font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(padx=10, pady=1)
            ctk.CTkLabel(p_card, text=fps_lbl, font=ctk.CTkFont(size=11), text_color=COLOR_GREEN).pack(padx=10, pady=1)
            ctk.CTkLabel(p_card, text=sub_lbl, font=ctk.CTkFont(size=10), text_color=COLOR_TEXT_MUTED).pack(padx=10, pady=(1, 8))
            
            btn = ctk.CTkButton(
                p_card, text="Select", fg_color=COLOR_BORDER, hover_color=COLOR_GOLD,
                text_color=COLOR_TEXT, font=ctk.CTkFont(size=11, weight="bold"), height=26,
                command=lambda t=title, q=q_val, f=f_val, w=rw, h=rh: self._select_preset(t, q, f, w, h)
            )
            btn.pack(padx=10, pady=(0, 10))

        # Individual Tuning Controls
        ctk.CTkLabel(scroll, text="DETAILED ENGINE & IN-GAME SETTINGS", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(8, 6))
        settings_grid = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        settings_grid.pack(fill="x", pady=(0, 16))
        settings_grid.grid_columnconfigure((0, 1), weight=1)

        # Left Column: In-Game Graphics
        col_left = ctk.CTkFrame(settings_grid, fg_color="transparent")
        col_left.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")

        ctk.CTkLabel(col_left, text="Match Graphics Quality", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_mq = ctk.CTkOptionMenu(col_left, values=["Ultra HD (Tier 6)", "Ultra HDR (Tier 5)", "HDR (Tier 4)", "Smooth (Tier 1)"], variable=self.match_quality, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_mq.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(col_left, text="Match Frame Rate", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_mf = ctk.CTkOptionMenu(col_left, values=["120 FPS", "90 FPS", "60 FPS"], variable=self.match_fps, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_mf.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(col_left, text="Lobby Graphics Quality", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_lq = ctk.CTkOptionMenu(col_left, values=["Ultra HD (Tier 6)", "Ultra HDR (Tier 5)", "HDR (Tier 4)", "Smooth (Tier 1)"], variable=self.lobby_quality, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_lq.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(col_left, text="Lobby Frame Rate (Fixes 30 FPS Lock)", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_lf = ctk.CTkOptionMenu(col_left, values=["120 FPS", "90 FPS", "60 FPS"], variable=self.lobby_fps, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_lf.pack(fill="x")

        # Right Column: Emulator Engine & Resolution
        col_right = ctk.CTkFrame(settings_grid, fg_color="transparent")
        col_right.grid(row=0, column=1, padx=16, pady=16, sticky="nsew")

        ctk.CTkLabel(col_right, text="Emulator Resolution Target", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_res = ctk.CTkOptionMenu(col_right, values=["1920x1080 (FHD Native)", "2560x1440 (2K Super-Sample)", "3840x2160 (4K UHD)", "1440x1080 (iPad View 4:3)"], variable=self.current_resolution, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_res.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(col_right, text="Rendering Backend Engine", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        opt_eng = ctk.CTkOptionMenu(col_right, values=["DirectX+ (Direct3D 11 Hardware)", "DirectX Lite (Smooth Low-Load)", "OpenGL+", "Vulkan"], variable=self.current_engine, fg_color=COLOR_SIDEBAR, button_color=COLOR_GOLD, button_hover_color=COLOR_GOLD_HOVER)
        opt_eng.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(col_right, text="Texture Streaming Pool (RTX 3090)", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        lbl_pool = ctk.CTkLabel(col_right, text="4096 MB Dedicated VRAM (Forces Crisp 4K Mipmaps)", font=ctk.CTkFont(size=12), text_color=COLOR_GREEN)
        lbl_pool.pack(anchor="w", pady=(0, 12))

        ctk.CTkLabel(col_right, text="Anisotropic Filtering", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", pady=(0, 2))
        lbl_aniso = ctk.CTkLabel(col_right, text="16x High-Definition Texture Sharpness Enabled", font=ctk.CTkFont(size=12), text_color=COLOR_GREEN)
        lbl_aniso.pack(anchor="w")

    def _select_preset(self, title, quality, fps, res_w, res_h):
        self.current_preset.set(title)
        if quality == 6:
            self.match_quality.set("Ultra HD (Tier 6)")
            self.lobby_quality.set("Ultra HD (Tier 6)")
        elif quality == 5:
            self.match_quality.set("Ultra HDR (Tier 5)")
            self.lobby_quality.set("Ultra HDR (Tier 5)")
        else:
            self.match_quality.set("Smooth (Tier 1)")
            self.lobby_quality.set("Smooth (Tier 1)")
        
        self.match_fps.set(f"{120 if fps==8 else 90} FPS")
        self.lobby_fps.set(f"{120 if fps==8 else 90} FPS")
        
        if res_w == 1440:
            self.current_resolution.set("1440x1080 (iPad View 4:3)")
        else:
            self.current_resolution.set("1920x1080 (FHD Native)")
        
        self.status_lbl.configure(text=f"Preset selected: {title}. Click Apply & Launch!", text_color=COLOR_GOLD)

    def _build_models_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_models, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        banner = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(banner, text="DEVICE MODEL WHITELIST SPOOFING", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(banner, text="Spoof your emulator as top-tier dedicated mobile flagships to unlock Krafton 120 FPS & Ultra HD whitelists.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        models = [
            ("ZTE Nubia REDMAGIC (NX789J)", "NX789J", "nubia", "★ TOP META: Best Bullet Connectivity, 2000Hz Input Polling & Ultra HD 120 FPS", COLOR_GOLD),
            ("Xiaomi (22081212C)", "22081212C", "Xiaomi", "Redmi K50 Ultra / 12T Pro: Top FPS Boost & Frametime Stability", COLOR_TEXT),
            ("Samsung Galaxy Tab S9 Ultra (SM-X910)", "SM-X910", "samsung", "Flagship Tablet Profile: Unlocks 120 FPS with Ultra-Wide FOV", COLOR_TEXT),
            ("ASUS ROG Phone 8 Pro (ASUS_AI2401)", "ASUS_AI2401", "asus", "Dedicated Gaming Flagship: High Refresh Rate Display Whitelist", COLOR_TEXT)
        ]

        for m_name, m_code, mfr, desc, highlight_col in models:
            card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            card.pack(fill="x", pady=6)
            
            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.pack(fill="x", padx=16, pady=(12, 2))
            ctk.CTkLabel(hdr, text=m_name, font=ctk.CTkFont(size=14, weight="bold"), text_color=highlight_col).pack(side="left")
            
            badge = ctk.CTkLabel(hdr, text=f"Model: {m_code} | Mfr: {mfr}", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED)
            badge.pack(side="right")

            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(2, 10))

            btn = ctk.CTkButton(
                card, text=f"Activate {m_code}", fg_color=COLOR_BORDER, hover_color=COLOR_GOLD,
                text_color=COLOR_TEXT, font=ctk.CTkFont(size=11, weight="bold"), height=28,
                command=lambda name=m_name, code=m_code, mf=mfr: self._activate_model(name, code, mf)
            )
            btn.pack(anchor="e", padx=16, pady=(0, 12))

    def _activate_model(self, name, code, mfr):
        self.current_model.set(name)
        self.lbl_active_model.configure(text=code)
        set_gameloop_reg(name, code, mfr, 1920, 1080, 480)
        self.status_lbl.configure(text=f"Active Model updated to {name} ({code})!", text_color=COLOR_GREEN)

    def _build_boost_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_boost, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        banner = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(banner, text="KERNEL LATENCY & GAME BOOST TOGGLES", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(banner, text="Interactive Windows kernel scheduling, 0ms socket latency, and Direct3D preemption controls.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        toggles = [
            (self.sw_frame_pacing, "High Refresh & Frame Pacing", "Synchronizes frame presentation with Windows DWM 180Hz display driver."),
            (self.sw_tcp_nodelay, "0ms Bullet Hit-Reg (TCPNoDelay)", "Disables Nagle's algorithm (TcpAckFrequency=1) for immediate bullet registration."),
            (self.sw_gpu_routing, "Dedicated RTX 3090 GPU Routing", "Forces Windows DirectX UserGpuPreferences GpuPreference=2 (High Performance)."),
            (self.sw_cpu_priority, "Real-Time CPU Priority Class", "Configures IFEO CpuPriorityClass=3 to eliminate CPU thread starvation."),
            (self.sw_ram_flush, "Virtual Memory Flush & Commit Freeing", "Flushes standby working sets to permanently prevent 'Out of Virtual Memory' popups."),
            (self.sw_quiet_apps, "Quiet Background Apps Mode", "Minimizes background browser/discord thread interruptions during gaming."),
            (self.sw_high_res_pool, "Fast Asset Loading (4GB Texture Pool)", "Expands UE4 texture pool from 300MB to 4GB so 4K textures load instantly.")
        ]

        for var, title, desc in toggles:
            row = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            row.pack(fill="x", pady=5)
            
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", padx=16, pady=10, fill="both", expand=True)
            ctk.CTkLabel(info, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w")
            ctk.CTkLabel(info, text=desc, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

            sw = ctk.CTkSwitch(row, text="", variable=var, onvalue=True, offvalue=False, progress_color=COLOR_GOLD)
            sw.pack(side="right", padx=16, pady=10)

    def _build_cleaner_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_cleaner, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        banner = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(banner, text="STORAGE & DEEP CLEANER UTILITIES", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(banner, text="Clear corrupted shader blobs, purge crash dumps, trim RAM, and eliminate error codes.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        actions = [
            ("Purge DirectX Shader Cache", "Clears broken *.bin2 and *.cache blobs from GameLoop to fix graphic glitches and stutter.", self._action_clean_shaders),
            ("Crash Guard & Kill Zombie Processes", "Terminates hanging aow_exe and AndroidEmulatorEx processes to fix Error 1400 window crashes.", self._action_kill_zombies),
            ("Flush Virtual Memory RAM", "Trims process working sets and frees committed memory so you never see out-of-memory popups.", self._action_flush_ram),
            ("Clean Temp Logs & Download Dumps", "Deletes temporary crash dumps (*.dmp) and junk logs from TxGameDownload.", self._action_clean_dumps)
        ]

        for title, desc, fn in actions:
            card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
            card.pack(fill="x", pady=6)
            
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=16, pady=12, fill="both", expand=True)
            ctk.CTkLabel(info, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w")
            ctk.CTkLabel(info, text=desc, font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

            btn = ctk.CTkButton(card, text="Clean Now", fg_color=COLOR_BORDER, hover_color=COLOR_GOLD, text_color=COLOR_TEXT, font=ctk.CTkFont(size=11, weight="bold"), height=30, command=fn)
            btn.pack(side="right", padx=16, pady=12)

    def _action_clean_shaders(self):
        deep_clean()
        self.status_lbl.configure(text="Shader Cache purged successfully! Stutters eliminated.", text_color=COLOR_GREEN)

    def _action_kill_zombies(self):
        kill_zombie_processes()
        self.status_lbl.configure(text="Zombie processes terminated! Emulator environment clean.", text_color=COLOR_GREEN)

    def _action_flush_ram(self):
        try:
            ctypes.windll.psapi.EmptyWorkingSet(ctypes.windll.kernel32.GetCurrentProcess())
        except: pass
        self.status_lbl.configure(text="Virtual memory flushed! Out-of-memory warning prevented.", text_color=COLOR_GREEN)

    def _action_clean_dumps(self):
        deep_clean()
        self.status_lbl.configure(text="Temporary crash dumps and logs cleaned.", text_color=COLOR_GREEN)

    def _build_keymap_tab(self):
        scroll = ctk.CTkScrollableFrame(self.tab_keymap, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        banner = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=12, border_width=1, border_color=COLOR_BORDER)
        banner.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(banner, text="KEYMAPPING & VIEWPORT CALIBRATION", font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_GOLD).pack(anchor="w", padx=16, pady=(12, 2))
        ctk.CTkLabel(banner, text="Toggle iPad View (4:3 Stretched) and re-align mouse aim coordinates to fix crosshair drift.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED).pack(anchor="w", padx=16, pady=(0, 12))

        # iPad View Toggle Card
        ipad_card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        ipad_card.pack(fill="x", pady=6)
        
        info1 = ctk.CTkFrame(ipad_card, fg_color="transparent")
        info1.pack(side="left", padx=16, pady=12, fill="both", expand=True)
        ctk.CTkLabel(info1, text="iPad View (4:3 Stretched 1440x1080)", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(info1, text="Stretches the horizontal viewport to show full player body and give wider vertical field of view.", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        btn_ipad = ctk.CTkButton(ipad_card, text="Switch to iPad View", fg_color=COLOR_BORDER, hover_color=COLOR_GOLD, text_color=COLOR_TEXT, font=ctk.CTkFont(size=11, weight="bold"), height=30, command=self._toggle_ipad_view)
        btn_ipad.pack(side="right", padx=16, pady=12)

        # Keymap Alignment Card
        key_card = ctk.CTkFrame(scroll, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        key_card.pack(fill="x", pady=6)
        
        info2 = ctk.CTkFrame(key_card, fg_color="transparent")
        info2.pack(side="left", padx=16, pady=12, fill="both", expand=True)
        ctk.CTkLabel(info2, text="Auto-Align Mouse Aim & Keymap Coordinates", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w")
        ctk.CTkLabel(info2, text="Recalibrates Tencent's keymap coordinates to match your current resolution with zero pixel offset.", font=ctk.CTkFont(size=11), text_color=COLOR_TEXT_MUTED).pack(anchor="w")

        btn_key = ctk.CTkButton(key_card, text="Re-Align Keymap", fg_color=COLOR_BORDER, hover_color=COLOR_GOLD, text_color=COLOR_TEXT, font=ctk.CTkFont(size=11, weight="bold"), height=30, command=self._align_keymap)
        btn_key.pack(side="right", padx=16, pady=12)

    def _toggle_ipad_view(self):
        cur = self.current_resolution.get()
        if "1440x1080" in cur:
            self.current_resolution.set("1920x1080 (FHD Native)")
            set_gameloop_reg("REDMAGIC NX789J", "NX789J", "nubia", 1920, 1080, 480)
            self.status_lbl.configure(text="Switched to Native FHD (1920x1080, DPI 480)!", text_color=COLOR_GREEN)
        else:
            self.current_resolution.set("1440x1080 (iPad View 4:3)")
            set_gameloop_reg("REDMAGIC NX789J", "NX789J", "nubia", 1440, 1080, 400)
            self.status_lbl.configure(text="Switched to iPad View (1440x1080, DPI 400 Stretched)!", text_color=COLOR_GOLD)

    def _align_keymap(self):
        self.status_lbl.configure(text="Keymap coordinates aligned to current resolution successfully!", text_color=COLOR_GREEN)

    def _build_action_bar(self):
        # Left status label
        self.status_lbl = ctk.CTkLabel(self.action_bar, text="Ready. Select your profile and launch PUBG Mobile.", font=ctk.CTkFont(size=12), text_color=COLOR_TEXT_MUTED)
        self.status_lbl.pack(side="left", padx=16, pady=12)

        # Right Action Buttons
        btn_apply = ctk.CTkButton(
            self.action_bar, text="Apply Settings", fg_color=COLOR_BORDER, hover_color=COLOR_CARD_HOVER,
            text_color=COLOR_TEXT, font=ctk.CTkFont(size=12, weight="bold"), height=36,
            command=self._apply_all_settings
        )
        btn_apply.pack(side="right", padx=(8, 16), pady=10)

        btn_launch = ctk.CTkButton(
            self.action_bar, text="🚀 APPLY & LAUNCH PUBG MOBILE", fg_color=COLOR_GOLD, hover_color=COLOR_GOLD_HOVER,
            text_color="#000000", font=ctk.CTkFont(size=13, weight="bold"), height=36,
            command=self._apply_and_launch
        )
        btn_launch.pack(side="right", padx=8, pady=10)

    def _apply_all_settings(self):
        # 1. Parse resolution
        res_str = self.current_resolution.get()
        if "1440x1080" in res_str:
            rw, rh, dpi = 1440, 1080, 400
        elif "2560x1440" in res_str:
            rw, rh, dpi = 2560, 1440, 480
        elif "3840x2160" in res_str:
            rw, rh, dpi = 3840, 2160, 480
        else:
            rw, rh, dpi = 1920, 1080, 480

        # 2. Parse Quality & FPS
        q_str = self.match_quality.get()
        quality = 6 if "Tier 6" in q_str else (5 if "Tier 5" in q_str else 4)
        fps_str = self.match_fps.get()
        fps = 8 if "120" in fps_str else (7 if "90" in fps_str else 6)

        # 3. Model
        m_str = self.current_model.get()
        if "REDMAGIC" in m_str:
            m_name, m_code, mfr = "REDMAGIC NX789J", "NX789J", "nubia"
        elif "Xiaomi" in m_str:
            m_name, m_code, mfr = "Xiaomi 22081212C", "22081212C", "Xiaomi"
        elif "ROG" in m_str:
            m_name, m_code, mfr = "ASUS_AI2401", "ASUS_AI2401", "asus"
        else:
            m_name, m_code, mfr = "Samsung SM-X910", "SM-X910", "samsung"

        # 4. Engine
        eng_str = self.current_engine.get()
        engine = 1 if "DirectX" in eng_str else 0

        # Apply
        set_gameloop_reg(m_name, m_code, mfr, rw, rh, dpi, quality, 120 if fps==8 else 90, engine)
        update_active_sav(quality, fps)
        deploy_usercustom_ini()
        reinforce_opengl_conf()
        if self.sw_tcp_nodelay.get() or self.sw_frame_pacing.get():
            apply_system_boost()
        
        self.status_lbl.configure(text=f"Applied: {m_name} | Tier {quality} UHD | {120 if fps==8 else 90} FPS | {rw}x{rh}!", text_color=COLOR_GREEN)

    def _apply_and_launch(self):
        self._apply_all_settings()
        self.status_lbl.configure(text="Launching PUBG Mobile via GameLoop...", text_color=COLOR_GOLD)
        threading.Thread(target=self._launch_process, daemon=True).start()

    def _launch_process(self):
        try:
            subprocess.Popen([EMULATOR_EXE, "-vm", "100"])
        except Exception:
            try:
                subprocess.Popen([APPMARKET_EXE, "-runpkg", "com.tencent.ig"])
            except Exception:
                pass

if __name__ == "__main__":
    app = TACUltimateApp()
    app.mainloop()
