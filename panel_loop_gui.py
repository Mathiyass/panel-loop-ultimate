r"""
===============================================================================
MATHIYA GAMELOOP PANEL - ULTIMATE CYBER-ESPORTS DASHBOARD & MINI-HUD
Universal Compatibility: All GameLoop Versions (Global, BGMI, Chinese, KR, VN, TW)
Hardware Target: Any CPU (Auto-Topology AMD/Intel), Any GPU, Any Display (180Hz+)
100% Pure Win32 Ctypes API - ZERO Console/Terminal Popups Ever
===============================================================================
"""

import os
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
import winsound

import customtkinter as ctk
from PIL import Image

from gui_engine import (
    PanelLoopEngine,
    SUPPORTED_PACKAGES,
    USERCUSTOM_INODES,
    GVAS_SAVE_INODES,
    CPU_INFO,
    PATHS_INFO
)

# Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Futuristic Cyberpunk Color Palette
COLOR_BG = "#070A0F"
COLOR_SIDEBAR = "#0D111A"
COLOR_CARD = "#121824"
COLOR_CARD_HOVER = "#1A2234"
COLOR_BORDER = "#1E293B"
COLOR_BORDER_GLOW = "#00F0FF"
COLOR_CYAN = "#00F0FF"
COLOR_CYAN_HOVER = "#00D2E0"
COLOR_VIOLET = "#A855F7"
COLOR_VIOLET_HOVER = "#9333EA"
COLOR_GOLD = "#FEB700"
COLOR_GOLD_HOVER = "#E0A200"
COLOR_GREEN = "#00F985"
COLOR_RED = "#FF4444"
COLOR_TEXT = "#F8FAFC"
COLOR_MUTED = "#94A3B8"
COLOR_CONSOLE_BG = "#05070B"

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_ICO = os.path.join(ASSETS_DIR, "mathiya_icon.ico")
ICON_PNG = os.path.join(ASSETS_DIR, "mathiya_header_logo.png")

def play_cyber_chime(sound_type="boost"):
    try:
        if sound_type == "boost":
            threading.Thread(target=lambda: [winsound.Beep(1000, 50), winsound.Beep(1500, 80), winsound.Beep(2000, 120)], daemon=True).start()
        elif sound_type == "click":
            threading.Thread(target=lambda: winsound.Beep(1800, 40), daemon=True).start()
        elif sound_type == "purge":
            threading.Thread(target=lambda: [winsound.Beep(800, 60), winsound.Beep(1200, 90)], daemon=True).start()
    except Exception:
        pass

# -----------------------------------------------------------------------------
# IN-GAME FLOATING MINI-HUD (ALWAYS-ON-TOP DRAGGABLE OVERLAY)
# -----------------------------------------------------------------------------
class MiniHUDWindow(ctk.CTkToplevel):
    def __init__(self, master_app, engine):
        super().__init__(master_app)
        self.master_app = master_app
        self.engine = engine

        self.title("Mathiya GameLoop Mini-HUD")
        self.geometry("340x190+50+50")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.94)
        self.configure(fg_color="#070A0F")

        # Outer Border Frame with Cyan Glow
        self.border_frame = ctk.CTkFrame(self, fg_color="#0D111A", border_width=1, border_color=COLOR_CYAN, corner_radius=10)
        self.border_frame.pack(fill="both", expand=True, padx=1, pady=1)

        # Drag bar
        self.drag_bar = ctk.CTkFrame(self.border_frame, fg_color="#141A26", height=30, corner_radius=8)
        self.drag_bar.pack(fill="x", padx=4, pady=4)
        self.drag_bar.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            self.drag_bar,
            text="⚡ MATHIYA // TOURNAMENT HUD",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=COLOR_CYAN
        )
        title_lbl.pack(side="left", padx=8)

        btn_close = ctk.CTkButton(
            self.drag_bar, text="✕", width=22, height=22,
            fg_color="transparent", hover_color=COLOR_RED, text_color=COLOR_TEXT,
            command=self.hide_hud, font=ctk.CTkFont(size=10, weight="bold")
        )
        btn_close.pack(side="right", padx=4)

        # Mouse Drag Handlers
        self.drag_bar.bind("<ButtonPress-1>", self._start_drag)
        self.drag_bar.bind("<B1-Motion>", self._on_drag)
        title_lbl.bind("<ButtonPress-1>", self._start_drag)
        title_lbl.bind("<B1-Motion>", self._on_drag)

        # Stats Container
        stats_box = ctk.CTkFrame(self.border_frame, fg_color="transparent")
        stats_box.pack(fill="both", expand=True, padx=12, pady=(2, 6))

        # Row 1: Kernel Timer
        r1 = ctk.CTkFrame(stats_box, fg_color="transparent")
        r1.pack(fill="x", pady=2)
        ctk.CTkLabel(r1, text="Kernel Timer:", font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(side="left")
        self.hud_timer_lbl = ctk.CTkLabel(r1, text="0.50 ms", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=COLOR_GREEN)
        self.hud_timer_lbl.pack(side="right")

        # Row 2: Profile Status
        r2 = ctk.CTkFrame(stats_box, fg_color="transparent")
        r2.pack(fill="x", pady=2)
        ctk.CTkLabel(r2, text="Profile / Quality:", font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(side="left")
        self.hud_prof_lbl = ctk.CTkLabel(r2, text="HDR 120 FPS Locked", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_CYAN)
        self.hud_prof_lbl.pack(side="right")

        # Row 3: Available RAM
        r3 = ctk.CTkFrame(stats_box, fg_color="transparent")
        r3.pack(fill="x", pady=2)
        ctk.CTkLabel(r3, text="Available RAM:", font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(side="left")
        self.hud_mem_lbl = ctk.CTkLabel(r3, text="-- GB Free", font=ctk.CTkFont(family="Consolas", size=10), text_color=COLOR_GOLD)
        self.hud_mem_lbl.pack(side="right")

        # Action Button Row (Boost + Purge)
        btn_row = ctk.CTkFrame(self.border_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 8))

        self.btn_hud_boost = ctk.CTkButton(
            btn_row,
            text="⚡ QUICK BOOST",
            command=self._quick_boost,
            height=28,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=COLOR_CYAN,
            text_color="#002022",
            hover_color=COLOR_CYAN_HOVER
        )
        self.btn_hud_boost.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.btn_hud_purge = ctk.CTkButton(
            btn_row,
            text="🧹 PURGE RAM",
            command=self._quick_purge,
            height=28,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=COLOR_CARD_HOVER,
            text_color=COLOR_GOLD,
            hover_color="#243048"
        )
        self.btn_hud_purge.pack(side="left", fill="x", expand=True, padx=(4, 0))

        self.start_x = 0
        self.start_y = 0

    def _start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def _on_drag(self, event):
        deltax = event.x - self.start_x
        deltay = event.y - self.start_y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def hide_hud(self):
        self.withdraw()

    def show_hud(self):
        self.deiconify()
        self.lift()

    def _quick_boost(self):
        self.btn_hud_boost.configure(text="BOOSTING...", state="disabled")
        def worker():
            self.engine.apply_master_esports_optimization()
            if self.master_app.sound_enabled:
                play_cyber_chime("boost")
            self.master_app.after(500, self.update_stats)
            self.btn_hud_boost.configure(text="⚡ BOOSTED!", state="normal")
            self.master_app.after(2000, lambda: self.btn_hud_boost.configure(text="⚡ QUICK BOOST"))
        threading.Thread(target=worker, daemon=True).start()

    def _quick_purge(self):
        def worker():
            self.engine.purge_standby_and_shader_cache()
            if self.master_app.sound_enabled:
                play_cyber_chime("purge")
            self.master_app.after(500, self.update_stats)
        threading.Thread(target=worker, daemon=True).start()

    def update_stats(self):
        diag = self.engine.get_live_diagnostics()
        res = diag.get("timer_resolution_ms", 15.6)
        self.hud_timer_lbl.configure(text=f"{res:.2f} ms", text_color=COLOR_GREEN if res <= 1.0 else COLOR_GOLD)
        self.hud_prof_lbl.configure(text="HDR 120 Locked" if diag.get("fps_locked") else "90 FPS Default")
        self.hud_mem_lbl.configure(text=f"{diag.get('virtual_avail_gb', 0.0)} GB Free")

# -----------------------------------------------------------------------------
# MAIN DASHBOARD APPLICATION
# -----------------------------------------------------------------------------
class PanelLoopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MATHIYA GAMELOOP PANEL // Mathiya Tournament Setup (120 FPS Locked)")
        self.geometry("1160x780")
        self.minsize(1020, 720)
        self.configure(fg_color=COLOR_BG)

        # Apply Custom Esports Windows Icon
        if os.path.exists(ICON_ICO):
            try:
                self.iconbitmap(ICON_ICO)
            except Exception:
                pass

        # Initialize Backend Engine (Zero-Subprocess Win32 API)
        self.engine = PanelLoopEngine(log_callback=self.log_to_terminal)
        self.current_tab = "dashboard"
        self.sound_enabled = True
        self.selected_pkg = "com.tencent.ig"

        # Floating Mini-HUD
        self.mini_hud = MiniHUDWindow(self, self.engine)
        self.mini_hud.withdraw()

        # Build UI Architecture
        self._create_header()
        self._create_body()

        # Shutdown Protocol
        self._is_closing = False
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start periodic telemetry polling (100% PURE WIN32 - ZERO POPUPS)
        self.after(500, self.update_telemetry)
        self.after(3000, self._periodic_status_checker)

        # Initial Log Message
        self.log_to_terminal("[+] MATHIYA GAMELOOP PANEL: MATHIYA TOURNAMENT SETUP INITIALIZED", "SUCCESS")
        self.log_to_terminal(f"[*] CPU Detected: {self.engine.cpu['name']} ({self.engine.cpu['threads']} Threads)", "INFO")
        self.log_to_terminal(f"[*] GameLoop Path: {self.engine.paths['install_dir']} (Rootfs: {os.path.basename(self.engine.paths['rootfs_dir'])})", "INFO")
        self.log_to_terminal("[*] Device Target: REDMAGIC 9 Pro (NX769J) [nubia]", "INFO")

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COLOR_SIDEBAR, height=72, corner_radius=0, border_width=1, border_color=COLOR_BORDER)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        # Left: Logo Emblem & Title
        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.pack(side="left", padx=16, pady=10)

        # Load Header Logo Image
        if os.path.exists(ICON_PNG):
            try:
                pil_img = Image.open(ICON_PNG)
                self.header_logo = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(44, 44))
                lbl_icon = ctk.CTkLabel(title_box, image=self.header_logo, text="")
                lbl_icon.pack(side="left", padx=(0, 12))
            except Exception:
                pass

        text_subbox = ctk.CTkFrame(title_box, fg_color="transparent")
        text_subbox.pack(side="left")

        title_lbl = ctk.CTkLabel(
            text_subbox,
            text="⚡ MATHIYA GAMELOOP PANEL // ESPORTS",
            font=ctk.CTkFont(family="Segoe UI Variable", size=17, weight="bold"),
            text_color=COLOR_CYAN
        )
        title_lbl.pack(anchor="w")

        sub_lbl = ctk.CTkLabel(
            text_subbox,
            text="UNIVERSAL ENGINE // 0.50ms KERNEL TIMER // 1:1 RAW MOUSE // LOCKED 120 FPS",
            font=ctk.CTkFont(family="Segoe UI Variable", size=10, weight="bold"),
            text_color=COLOR_MUTED
        )
        sub_lbl.pack(anchor="w")

        # Right: Profile Selector, Status Badge, HUD Toggle
        right_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_box.pack(side="right", padx=16, pady=12)

        # Profile Quick Switcher Dropdown
        self.hdr_profile_opt = ctk.CTkOptionMenu(
            right_box,
            values=[
                "🏆 Streamer HDR 120 (Verified)",
                "⚡ Tournament HDR 120",
                "🚀 Streamer Flat 120"
            ],
            command=self._on_header_profile_change,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#141A26",
            button_color=COLOR_CYAN,
            button_hover_color=COLOR_CYAN_HOVER,
            width=215,
            height=32
        )
        self.hdr_profile_opt.set("🏆 Streamer HDR 120 (Verified)")
        self.hdr_profile_opt.pack(side="left", padx=(0, 8))

        # Sound FX Toggle
        self.btn_sound = ctk.CTkButton(
            right_box,
            text="🔊 SFX",
            command=self._toggle_sound,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#141A26",
            text_color=COLOR_GREEN,
            border_width=1,
            border_color=COLOR_BORDER,
            hover_color=COLOR_CARD_HOVER,
            width=65,
            height=32
        )
        self.btn_sound.pack(side="left", padx=(0, 8))

        # HUD Toggle Button
        btn_hud_toggle = ctk.CTkButton(
            right_box,
            text="📌 MINI-HUD",
            command=self.toggle_mini_hud,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#18202D",
            text_color=COLOR_CYAN,
            border_width=1,
            border_color=COLOR_BORDER,
            hover_color=COLOR_CARD_HOVER,
            width=100,
            height=32
        )
        btn_hud_toggle.pack(side="left", padx=(0, 8))

        # Live Status Badges
        self.badge_timer = self._create_badge(right_box, "TIMER", "0.50 ms", COLOR_GREEN)
        self.badge_fps = self._create_badge(right_box, "TARGET", "120 FPS", COLOR_CYAN)

    def _create_badge(self, parent, label, value, val_color):
        frame = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=6, border_width=1, border_color=COLOR_BORDER)
        frame.pack(side="left", padx=3)

        lbl = ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=9, weight="bold"), text_color=COLOR_MUTED)
        lbl.pack(side="left", padx=(6, 3), pady=4)

        val_lbl = ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(family="Consolas", size=10, weight="bold"), text_color=val_color)
        val_lbl.pack(side="left", padx=(0, 6), pady=4)
        return val_lbl

    def _toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.btn_sound.configure(text="🔊 SFX", text_color=COLOR_GREEN)
            play_cyber_chime("click")
        else:
            self.btn_sound.configure(text="🔇 MUTE", text_color=COLOR_MUTED)

    def _on_header_profile_change(self, val):
        if "Verified" in val or "Streamer HDR" in val or "MrBro" in val:
            self._apply_preset_direct(quality_tier=6, target_fps=0, pool_mb=2048, shadow_scale=1.0, shadow_res=1024)
        elif "Tournament" in val or "HDR" in val:
            self._apply_preset_direct(quality_tier=5, target_fps=0, pool_mb=2048, shadow_scale=0.5, shadow_res=512)
        elif "Flat" in val or "Streamer" in val:
            self._apply_preset_direct(quality_tier=1, target_fps=0, pool_mb=100, shadow_scale=0.0, shadow_res=0)

    def _apply_preset_direct(self, quality_tier, target_fps, pool_mb, shadow_scale, shadow_res):
        def worker():
            self.engine.verify_aengine_integrity()
            self.engine.sync_usercustom_inodes(quality_tier=quality_tier, target_fps=target_fps, pool_mb=pool_mb, shadow_scale=shadow_scale, shadow_res=shadow_res, style=2)
            self.engine.sync_gvas_saves(quality_tier=quality_tier, fps_enum=8, style=2)
            self.engine.lock_all_inodes()
            if self.sound_enabled:
                play_cyber_chime("boost")
            self.after(500, self.update_telemetry)
        threading.Thread(target=worker, daemon=True).start()

    def _create_body(self):
        self.body_frame = ctk.CTkFrame(self, fg_color=COLOR_BG, corner_radius=0)
        self.body_frame.pack(side="top", fill="both", expand=True)

        # 1. Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self.body_frame, fg_color=COLOR_SIDEBAR, width=230, corner_radius=0, border_width=1, border_color=COLOR_BORDER)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        nav_title = ctk.CTkLabel(self.sidebar, text="COMMAND CENTER", font=ctk.CTkFont(size=11, weight="bold"), text_color=COLOR_MUTED)
        nav_title.pack(anchor="w", padx=20, pady=(16, 8))

        self.nav_buttons = {}
        tabs = [
            ("dashboard", "⚡ Dashboard", self.show_dashboard),
            ("graphics", "🎮 Graphics & HDR", self.show_graphics),
            ("network", "🌐 Network & DNS Flush", self.show_network),
            ("aim", "🎯 Mouse Aim & Hitbox", self.show_aim_and_mouse),
            ("system", "💻 CPU Pacing & RAM", self.show_system),
            ("engine_suite", "⚙️ GameLoop Engine", self.show_engine_suite),
            ("inodes", "🛡️ Inodes & Backup", self.show_inodes)
        ]

        for tab_id, text, cmd in tabs:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                font=ctk.CTkFont(family="Segoe UI Variable", size=13, weight="bold"),
                fg_color="transparent",
                text_color=COLOR_TEXT,
                hover_color=COLOR_CARD_HOVER,
                anchor="w",
                height=38,
                corner_radius=8
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[tab_id] = btn

        # Sidebar Bottom: Game Package Selector & Watchdog
        bot_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bot_frame.pack(side="bottom", fill="x", padx=14, pady=12)

        # Package Selector
        ctk.CTkLabel(bot_frame, text="GAME VERSION / REGION:", font=ctk.CTkFont(size=9, weight="bold"), text_color=COLOR_MUTED).pack(anchor="w", pady=(0, 2))
        self.pkg_opt = ctk.CTkOptionMenu(
            bot_frame,
            values=[
                "Global (com.tencent.ig)",
                "BGMI India (com.pubg.imobile)",
                "Korea (com.pubg.krmobile)",
                "Vietnam (com.vng.pubgmobile)",
                "Taiwan (com.reindex.tw)"
            ],
            command=self._on_pkg_change,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#141A26",
            button_color=COLOR_VIOLET,
            button_hover_color=COLOR_VIOLET_HOVER,
            height=28
        )
        self.pkg_opt.set("Global (com.tencent.ig)")
        self.pkg_opt.pack(fill="x", pady=(0, 8))

        # Watchdog Toggle Switch
        self.sw_watchdog = ctk.CTkSwitch(
            bot_frame,
            text="Auto-Pacing Watchdog",
            command=self._toggle_watchdog,
            font=ctk.CTkFont(size=11, weight="bold"),
            progress_color=COLOR_GREEN
        )
        self.sw_watchdog.pack(anchor="w", pady=(0, 8))

        admin_badge = ctk.CTkFrame(bot_frame, fg_color="#132019", border_width=1, border_color=COLOR_GREEN, corner_radius=6)
        admin_badge.pack(fill="x", pady=2)
        admin_lbl = ctk.CTkLabel(admin_badge, text="● UNIVERSAL ENGINE // NATIVE WIN32", font=ctk.CTkFont(size=9, weight="bold"), text_color=COLOR_GREEN)
        admin_lbl.pack(pady=3)

        ver_lbl = ctk.CTkLabel(bot_frame, text="Mathiya Tournament Setup v4.0", font=ctk.CTkFont(size=9), text_color=COLOR_MUTED)
        ver_lbl.pack(pady=(2, 0))

        # 2. Dynamic Content Area
        self.content_area = ctk.CTkFrame(self.body_frame, fg_color=COLOR_BG, corner_radius=0)
        self.content_area.pack(side="left", fill="both", expand=True, padx=18, pady=16)

        self.show_dashboard()

    def _on_pkg_change(self, val):
        if "Global" in val:
            self.selected_pkg = "com.tencent.ig"
        elif "BGMI" in val:
            self.selected_pkg = "com.pubg.imobile"
        elif "Korea" in val:
            self.selected_pkg = "com.pubg.krmobile"
        elif "Vietnam" in val:
            self.selected_pkg = "com.vng.pubgmobile"
        elif "Taiwan" in val:
            self.selected_pkg = "com.reindex.tw"
        self.log_to_terminal(f"[*] Active Game Package set to: {self.selected_pkg}", "INFO")

    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def _set_active_tab(self, active_id):
        self.current_tab = active_id
        for tid, btn in self.nav_buttons.items():
            if tid == active_id:
                btn.configure(fg_color=COLOR_CARD, text_color=COLOR_CYAN, border_width=1, border_color=COLOR_BORDER)
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_TEXT, border_width=0)

    def toggle_mini_hud(self):
        if self.mini_hud.winfo_viewable():
            self.mini_hud.hide_hud()
        else:
            self.mini_hud.show_hud()
            self.mini_hud.update_stats()

    def _toggle_watchdog(self):
        if self.sw_watchdog.get():
            self.engine.start_watchdog(on_detect_callback=lambda: [play_cyber_chime("boost"), self.update_telemetry()])
            self.log_to_terminal("[+] Background Auto-Pacing Watchdog: ENABLED", "SUCCESS")
        else:
            self.engine.stop_watchdog()
            self.log_to_terminal("[*] Background Auto-Pacing Watchdog: DISABLED", "INFO")

    # -------------------------------------------------------------------------
    # TAB 1: DASHBOARD & 1-CLICK MASTER BOOST
    # -------------------------------------------------------------------------
    def show_dashboard(self):
        self._clear_content()
        self._set_active_tab("dashboard")

        # Top Status Grid (6 Telemetry Cards)
        grid_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        grid_frame.pack(fill="x", pady=(0, 12))

        self.card_device = self._create_status_card(grid_frame, 0, 0, "📱 DEVICE PROFILE", "REDMAGIC 9 Pro", "NX769J [nubia] Spoof Locked", COLOR_CYAN)
        self.card_hdr = self._create_status_card(grid_frame, 0, 1, "🎨 GRAPHICS PIPELINE", "Streamer Flat 120", "Zero Texture Stutter + 120 FPS Locked", COLOR_GREEN)
        self.card_dvr = self._create_status_card(grid_frame, 0, 2, "🚀 STUTTER ELIMINATION", "DVR Disabled", "Replays OFF & Async 1.0ms Locked", COLOR_GREEN)
        self.card_net = self._create_status_card(grid_frame, 1, 0, "🎯 HIT REGISTRATION", "Nagle Disabled", "Zero Ghost Bullets | 120Hz Tick", COLOR_GREEN)
        self.card_timer = self._create_status_card(grid_frame, 1, 1, "⏱️ KERNEL TIMER", "0.50 ms Pacing", "NtSetTimerResolution Sub-ms Locked", COLOR_CYAN)
        self.card_mem = self._create_status_card(grid_frame, 1, 2, "🧠 COMMIT HEADROOM", "-- GB Free", "Standby & Working Set Trim Ready", COLOR_GOLD)

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(2, weight=1)

        # Hero Action Ribbon (Master Boost + Quick Actions)
        action_bar = ctk.CTkFrame(self.content_area, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        action_bar.pack(fill="x", pady=(0, 12), ipady=6)

        btn_master = ctk.CTkButton(
            action_bar,
            text="⚡ APPLY VERIFIED STREAMER HDR 120 FPS (ZERO COMBAT LAG)",
            command=self.run_master_boost,
            font=ctk.CTkFont(family="Segoe UI Variable", size=13, weight="bold"),
            fg_color=COLOR_CYAN,
            text_color="#002022",
            hover_color=COLOR_CYAN_HOVER,
            height=44,
            corner_radius=8
        )
        btn_master.pack(side="left", padx=12, fill="x", expand=True)

        btn_dns = ctk.CTkButton(
            action_bar,
            text="🌐 FLUSH DNS",
            command=self._quick_dns_flush,
            font=ctk.CTkFont(family="Segoe UI Variable", size=11, weight="bold"),
            fg_color=COLOR_CARD_HOVER,
            text_color=COLOR_CYAN,
            border_width=1,
            border_color=COLOR_BORDER,
            hover_color="#243048",
            height=44,
            corner_radius=8
        )
        btn_dns.pack(side="left", padx=(0, 8))

        btn_purge = ctk.CTkButton(
            action_bar,
            text="🧹 PURGE RAM",
            command=self._quick_ram_purge,
            font=ctk.CTkFont(family="Segoe UI Variable", size=11, weight="bold"),
            fg_color=COLOR_CARD_HOVER,
            text_color=COLOR_GOLD,
            border_width=1,
            border_color=COLOR_BORDER,
            hover_color="#2A2F3D",
            height=44,
            corner_radius=8
        )
        btn_purge.pack(side="left", padx=(0, 8))

        btn_launch = ctk.CTkButton(
            action_bar,
            text="🎮 LAUNCH",
            command=lambda: self.engine.launch_gameloop(self.selected_pkg),
            font=ctk.CTkFont(family="Segoe UI Variable", size=11, weight="bold"),
            fg_color=COLOR_VIOLET,
            text_color=COLOR_TEXT,
            border_width=1,
            border_color=COLOR_BORDER,
            hover_color=COLOR_VIOLET_HOVER,
            height=44,
            corner_radius=8
        )
        btn_launch.pack(side="left", padx=(0, 8))

        btn_unlock = ctk.CTkButton(
            action_bar,
            text="🔓 UNLOCK",
            command=self.engine.unlock_all_inodes,
            font=ctk.CTkFont(family="Segoe UI Variable", size=11, weight="bold"),
            fg_color="transparent",
            text_color=COLOR_GOLD,
            border_width=1,
            border_color=COLOR_GOLD,
            hover_color="#332B14",
            height=44,
            corner_radius=8
        )
        btn_unlock.pack(side="left", padx=(0, 12))

        # Real-time Terminal Log Console
        console_container = ctk.CTkFrame(self.content_area, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        console_container.pack(fill="both", expand=True)

        cheader = ctk.CTkFrame(console_container, fg_color="transparent")
        cheader.pack(fill="x", padx=14, pady=(8, 4))

        clbl = ctk.CTkLabel(cheader, text="SYSTEM OPTIMIZATION LOG // ZERO-POPUP CONSOLE", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=COLOR_MUTED)
        clbl.pack(side="left")

        btn_clear = ctk.CTkButton(
            cheader, text="Clear", command=self.clear_terminal,
            width=50, height=22, font=ctk.CTkFont(size=10),
            fg_color="transparent", text_color=COLOR_MUTED, hover_color=COLOR_CARD_HOVER
        )
        btn_clear.pack(side="right")

        self.terminal_text = ctk.CTkTextbox(
            console_container,
            fg_color=COLOR_CONSOLE_BG,
            text_color="#A7B5C6",
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=6,
            border_width=1,
            border_color="#18202E"
        )
        self.terminal_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _quick_dns_flush(self):
        def worker():
            res = self.engine.flush_dns_cache()
            if self.sound_enabled:
                play_cyber_chime("click")
        threading.Thread(target=worker, daemon=True).start()

    def _quick_ram_purge(self):
        def worker():
            res = self.engine.purge_standby_and_shader_cache()
            if self.sound_enabled:
                play_cyber_chime("purge")
            self.after(500, self.update_telemetry)
        threading.Thread(target=worker, daemon=True).start()

    def _create_status_card(self, parent, row, col, title, value, detail, color):
        card = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=8, border_width=1, border_color=COLOR_BORDER)
        card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_MUTED)
        lbl_t.pack(anchor="w", padx=12, pady=(8, 1))

        lbl_v = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family="Segoe UI Variable", size=15, weight="bold"), text_color=color)
        lbl_v.pack(anchor="w", padx=12, pady=0)

        lbl_d = ctk.CTkLabel(card, text=detail, font=ctk.CTkFont(size=10), text_color=COLOR_MUTED)
        lbl_d.pack(anchor="w", padx=12, pady=(1, 8))
        return (lbl_v, lbl_d)

    def log_to_terminal(self, text, level="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        entry = f"[{now}] {text}\n"
        if hasattr(self, "terminal_text") and self.terminal_text.winfo_exists():
            self.terminal_text.insert("end", entry)
            self.terminal_text.see("end")

    def clear_terminal(self):
        if hasattr(self, "terminal_text") and self.terminal_text.winfo_exists():
            self.terminal_text.delete("1.0", "end")

    def run_master_boost(self):
        threading.Thread(target=self._run_master_boost_thread, daemon=True).start()

    def _run_master_boost_thread(self):
        self.engine.apply_master_esports_optimization()
        if self.sound_enabled:
            play_cyber_chime("boost")
        self.after(500, self.update_telemetry)
        if self.mini_hud.winfo_viewable():
            self.mini_hud.update_stats()

    # -------------------------------------------------------------------------
    # TAB 2: GRAPHICS & HDR ENGINE
    # -------------------------------------------------------------------------
    def show_graphics(self):
        self._clear_content()
        self._set_active_tab("graphics")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="🎮 GRAPHICS PRESETS & HDR COLOR PIPELINE", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        pcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        pcard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)

        ctk.CTkLabel(pcard, text="GRAPHICS PROFILE PRESET", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        self.preset_var = tk.StringVar(value="streamer120")
        presets = [
            ("streamer120", "🏆 Streamer Zero-Lag (Flat Pastel Buildings & 120 FPS Combat) [RECOMMENDED]", "Zero Texture Streaming (PoolSize=0), Zero Dynamic Shadows, 1.0ms Async Cap, Combat Particle Cap, Locked 120 FPS"),
            ("hdr120", "⚡ Cinematic True HDR 120 FPS (Full PBR Building Textures)", "Tier 5 HDR, GraphicFavor=4 (Customize Mode), 2GB Texture Pool, Colorful Style, High Details"),
            ("uncapped180", "🚀 Maximum Uncapped FPS (180Hz Monitor Synchronized)", "Flat Textures, t.MaxFPS=0 (Zero Limiter), 0ms Thread Lag, 180Hz+ Scanout"),
            ("balanced120", "🎬 Balanced 2K 90 FPS HDR", "Tier 2 Balanced Shading, 2K Resolution, Maximum visual clarity")
        ]

        for val, title, desc in presets:
            rb = ctk.CTkRadioButton(
                pcard, text=title, value=val, variable=self.preset_var,
                font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_TEXT,
                fg_color=COLOR_CYAN, hover_color=COLOR_CYAN_HOVER
            )
            rb.pack(anchor="w", padx=18, pady=(4, 1))
            ctk.CTkLabel(pcard, text=f"    {desc}", font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(anchor="w", padx=18, pady=(0, 4))

        tcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        tcard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)

        ctk.CTkLabel(tcard, text="TEXTURE STREAMING & SHADOW CONFIGURATION", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        s_frame = ctk.CTkFrame(tcard, fg_color="transparent")
        s_frame.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(s_frame, text="Texture Streaming Pool Size (MB):", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", pady=6)
        self.pool_slider = ctk.CTkSlider(s_frame, from_=512, to=3072, number_of_steps=10, width=280, fg_color="#232B3B", progress_color=COLOR_CYAN)
        self.pool_slider.set(2048)
        self.pool_slider.grid(row=0, column=1, padx=15, pady=6)
        self.pool_val_lbl = ctk.CTkLabel(s_frame, text="2048 MB (Full Textures)", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=COLOR_CYAN)
        self.pool_val_lbl.grid(row=0, column=2, sticky="w")
        self.pool_slider.configure(command=lambda v: self.pool_val_lbl.configure(text=f"{int(v)} MB"))

        ctk.CTkLabel(s_frame, text="Max CSM Shadow Resolution:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, sticky="w", pady=6)
        self.shadow_res_opt = ctk.CTkOptionMenu(s_frame, values=["512 (Esports High FPS)", "1024 (Cinematic)", "256 (Minimal)"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_CYAN, button_hover_color=COLOR_CYAN_HOVER)
        self.shadow_res_opt.set("512 (Esports High FPS)")
        self.shadow_res_opt.grid(row=1, column=1, sticky="w", padx=15, pady=6)

        btn_apply_gfx = ctk.CTkButton(
            container, text="APPLY GRAPHICS PROFILE & LOCK INODES",
            command=self._apply_custom_gfx,
            font=ctk.CTkFont(family="Segoe UI Variable", size=13, weight="bold"),
            fg_color=COLOR_CYAN, text_color="#002022", hover_color=COLOR_CYAN_HOVER,
            height=42, corner_radius=8
        )
        btn_apply_gfx.pack(fill="x", padx=4, pady=8)

    def _apply_custom_gfx(self):
        choice = self.preset_var.get()
        pool = int(self.pool_slider.get())
        shadow_res = 512 if "512" in self.shadow_res_opt.get() else 1024
        if choice in ("streamer120", "uncapped180"):
            q_tier = 1
            target_fps = 0
            pool = 0
            shadow_scale = 0.0
            shadow_res = 0
        elif choice == "hdr120":
            q_tier = 5
            target_fps = 0
            shadow_scale = 0.5
            shadow_res = 512
        else:
            q_tier = 2
            target_fps = 90
            shadow_scale = 0.6
            shadow_res = 512

        def worker():
            self.engine.verify_aengine_integrity()
            self.engine.sync_usercustom_inodes(quality_tier=q_tier, target_fps=target_fps, pool_mb=pool, shadow_scale=shadow_scale, shadow_res=shadow_res, style=2)
            self.engine.sync_gvas_saves(quality_tier=q_tier, fps_enum=8, style=2)
            self.engine.lock_all_inodes()
            if self.sound_enabled:
                play_cyber_chime("boost")
            self.after(500, self.update_telemetry)

        threading.Thread(target=worker, daemon=True).start()

    # -------------------------------------------------------------------------
    # TAB 3: NETWORK & DNS FLUSH ACCELERATOR
    # -------------------------------------------------------------------------
    def show_network(self):
        self._clear_content()
        self._set_active_tab("network")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="🌐 NETWORK, DNS ACCELERATOR & PACKET BENCHMARKER", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        # DNS Flush Card
        dns_card = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        dns_card.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(dns_card, text="NATIVE WIN32 DNS RESOLVER FLUSH (ZERO POPUPS)", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 6))

        ctk.CTkLabel(dns_card, text="Flushes corrupted DNS routing table directly in memory using dnsapi.dll without running cmd.exe.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=1)
        ctk.CTkLabel(dns_card, text="Prevents DNS resolution lag when matchmaking across PUBG Mobile match servers.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=1)

        btn_dns_action = ctk.CTkButton(
            dns_card,
            text="⚡ FLUSH DNS RESOLVER CACHE NOW",
            command=self._quick_dns_flush,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_CYAN,
            text_color="#002022",
            hover_color=COLOR_CYAN_HOVER,
            height=36
        )
        btn_dns_action.pack(anchor="w", padx=20, pady=(8, 4))

        # Ping Benchmarker Card
        bcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        bcard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(bcard, text="EDGE SERVER LATENCY TESTER", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        ping_box = ctk.CTkFrame(bcard, fg_color="transparent")
        ping_box.pack(fill="x", padx=20, pady=6)

        self.ping_res_lbl = ctk.CTkLabel(ping_box, text="-- ms", font=ctk.CTkFont(family="Consolas", size=26, weight="bold"), text_color=COLOR_GREEN)
        self.ping_res_lbl.pack(side="left", padx=(0, 20))

        btn_ping = ctk.CTkButton(
            ping_box,
            text="BENCHMARK EDGE PING",
            command=self._run_ping_test,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_CARD_HOVER,
            text_color=COLOR_TEXT,
            hover_color="#243048",
            border_width=1,
            border_color=COLOR_BORDER
        )
        btn_ping.pack(side="left")

        # Network Tuning Switches Card
        ncard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        ncard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(ncard, text="TCP/IP ESPORTS HITBOX PACKET TUNING", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        switches = [
            ("Disable Nagle's Algorithm (TCPNoDelay=1, TcpAckFrequency=1)", "Small bullet hit packets transmit immediately without 40-100ms buffering.", True),
            ("Disable Multimedia Network Throttling (Index=0xFFFFFFFF)", "Prevents Windows from throttling NIC packets while running 3D games.", True),
            ("Zero Hitbox Interpolation Lag (p.NetInterpolation=0.0)", "Renders enemy hitboxes at server real-time position with zero ghost bullets.", True),
            ("120Hz Network Tick Rate (net.MaxClientTickRate=120)", "Aligns network packet queue directly to 120 FPS frame pacing.", True)
        ]

        for title, desc, default_val in switches:
            s_frame = ctk.CTkFrame(ncard, fg_color="transparent")
            s_frame.pack(fill="x", padx=15, pady=4)
            sw = ctk.CTkSwitch(s_frame, text=title, font=ctk.CTkFont(size=12, weight="bold"), progress_color=COLOR_GREEN)
            if default_val:
                sw.select()
            sw.pack(anchor="w")
            ctk.CTkLabel(s_frame, text=f"    {desc}", font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(anchor="w")

    def _run_ping_test(self):
        self.ping_res_lbl.configure(text="Testing...", text_color=COLOR_MUTED)
        def worker():
            res = self.engine.measure_network_latency()
            if res["success"]:
                ms = res["latency_ms"]
                color = COLOR_GREEN if ms < 60 else (COLOR_GOLD if ms < 100 else COLOR_RED)
                self.ping_res_lbl.configure(text=f"{ms:.1f} ms", text_color=color)
                self.log_to_terminal(f"[+] Edge latency benchmark: {ms:.1f} ms (Host: {res['host']})", "SUCCESS")
            else:
                self.ping_res_lbl.configure(text="ERR", text_color=COLOR_RED)
        threading.Thread(target=worker, daemon=True).start()

    # -------------------------------------------------------------------------
    # TAB 4: MOUSE AIM & HITBOX SYNCHRONIZATION
    # -------------------------------------------------------------------------
    def show_aim_and_mouse(self):
        self._clear_content()
        self._set_active_tab("aim")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="🎯 1:1 RAW MOUSE AIM & HITBOX SYNCHRONIZATION", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        mcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        mcard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(mcard, text="ZERO POINTER ACCELERATION (1:1 LINEAR TRACKING)", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        ctk.CTkLabel(mcard, text="• Disables Windows 'Enhance Pointer Precision' curve (MouseSpeed=0, Threshold1=0, Threshold2=0).", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(mcard, text="• Removes non-linear mouse acceleration inside GameLoop for pixel-perfect spray control.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(mcard, text="• Synchronizes Windows cursor speed to true 1:1 raw hardware counts.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)

        btn_mouse = ctk.CTkButton(
            mcard,
            text="LOCK 1:1 RAW LINEAR MOUSE INPUT NOW",
            command=lambda: [self.engine.optimize_mouse_aim(), play_cyber_chime("click"), self.update_telemetry()],
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=COLOR_CYAN,
            text_color="#002022",
            hover_color=COLOR_CYAN_HOVER
        )
        btn_mouse.pack(anchor="w", padx=20, pady=(8, 4))

        acard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        acard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(acard, text="AIM ASSIST COLLISION CAPSULE FRICTION (120 HZ)", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        ctk.CTkLabel(acard, text="• At 40 FPS, collision checks tick every 25.0 ms, causing crosshair slip off enemies.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(acard, text="• At locked 120 FPS with 0.50ms kernel timer, collision friction runs 3x more frequently (every 8.33 ms).", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(acard, text="• p.NetInterpolation=0.0 eliminates client-side hitbox desync for true real-time target magnetism.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)

    # -------------------------------------------------------------------------
    # TAB 5: CPU PACING & RAM PURGE
    # -------------------------------------------------------------------------
    def show_system(self):
        self._clear_content()
        self._set_active_tab("system")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="💻 UNIVERSAL CPU PACING & STANDBY RAM PURGER", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        ccard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        ccard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(ccard, text="DYNAMIC CPU TOPOLOGY & AFFINITY ENFORCEMENT", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        cpu = self.engine.cpu
        ctk.CTkLabel(ccard, text=f"• Processor: {cpu['name']} ({cpu['threads']} Logical Threads)", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(ccard, text=f"• Detected Optimal Physical Mask: {hex(cpu['physical_mask'])} ({cpu['physical_cores']} Physical Cores)", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(ccard, text="• GameLoop Process Priority: HIGH (0x00000080) for aow_exe.exe & AndroidEmulatorEx.exe", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)

        aff_box = ctk.CTkFrame(ccard, fg_color="transparent")
        aff_box.pack(fill="x", padx=20, pady=(6, 4))

        ctk.CTkLabel(aff_box, text="Affinity Mode:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left", padx=(0, 10))
        self.aff_opt = ctk.CTkOptionMenu(
            aff_box,
            values=["Physical Cores Auto-Detect", "All Logical Cores", "Ryzen Physical (0x5555)"],
            font=ctk.CTkFont(size=11),
            fg_color=COLOR_CARD_HOVER,
            button_color=COLOR_CYAN,
            button_hover_color=COLOR_CYAN_HOVER
        )
        self.aff_opt.set("Physical Cores Auto-Detect")
        self.aff_opt.pack(side="left", padx=(0, 12))

        btn_proc = ctk.CTkButton(
            aff_box, text="APPLY AFFINITY & LOCK 0.50ms TIMER",
            command=self._apply_cpu_affinity,
            font=ctk.CTkFont(size=11, weight="bold"), fg_color=COLOR_CARD_HOVER, hover_color="#243048", border_width=1, border_color=COLOR_BORDER
        )
        btn_proc.pack(side="left")

        mcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        mcard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(mcard, text="HOST RAM & SHADER CACHE PURGER (NATIVE WIN32)", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        ctk.CTkLabel(mcard, text="Purges fragmented standby memory from background processes and clears stale DirectX / GameLoop shader cache files.", font=ctk.CTkFont(size=11), text_color=COLOR_MUTED).pack(anchor="w", padx=20, pady=2)

        btn_trim = ctk.CTkButton(
            mcard, text="🧹 PURGE STANDBY RAM & SHADERS NOW",
            command=self._quick_ram_purge,
            font=ctk.CTkFont(size=12, weight="bold"), fg_color=COLOR_GOLD, text_color="#000", hover_color=COLOR_GOLD_HOVER
        )
        btn_trim.pack(anchor="w", padx=20, pady=(8, 4))

    def _apply_cpu_affinity(self):
        val = self.aff_opt.get()
        mode = "all" if "All" in val else ("custom" if "Ryzen" in val else "physical")
        self.engine.lock_kernel_timer(5000)
        self.engine.enforce_process_pacing(mode=mode)
        if self.sound_enabled:
            play_cyber_chime("click")
        self.update_telemetry()

    # -------------------------------------------------------------------------
    # TAB 6: GAMELOOP ENGINE & RESOLUTION SUITE
    # -------------------------------------------------------------------------
    def show_engine_suite(self):
        self._clear_content()
        self._set_active_tab("engine_suite")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="⚙️ GAMELOOP ENGINE CONFIGURATION & RESOLUTION SUITE", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        ecard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        ecard.pack(fill="x", pady=(0, 14), padx=4, ipady=8)
        ctk.CTkLabel(ecard, text="RENDERER & DISPLAY RESOLUTION", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        grid = ctk.CTkFrame(ecard, fg_color="transparent")
        grid.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(grid, text="Display Resolution:", font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=0, sticky="w", pady=6)
        self.res_opt = ctk.CTkOptionMenu(grid, values=["1920x1080 (1080p Standard)", "2560x1440 (2K QHD)", "2560x1080 (21:9 Ultra-Wide)", "1600x900 (High FPS)"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_CYAN, button_hover_color=COLOR_CYAN_HOVER, width=220)
        self.res_opt.set("1920x1080 (1080p Standard)")
        self.res_opt.grid(row=0, column=1, sticky="w", padx=15, pady=6)

        ctk.CTkLabel(grid, text="Screen DPI:", font=ctk.CTkFont(size=11, weight="bold")).grid(row=1, column=0, sticky="w", pady=6)
        self.dpi_opt = ctk.CTkOptionMenu(grid, values=["480 DPI (High Precision)", "320 DPI (Balanced)", "240 DPI (Fast Crosshair)"], fg_color=COLOR_CARD_HOVER, button_color=COLOR_CYAN, button_hover_color=COLOR_CYAN_HOVER, width=220)
        self.dpi_opt.set("480 DPI (High Precision)")
        self.dpi_opt.grid(row=1, column=1, sticky="w", padx=15, pady=6)

        ctk.CTkLabel(grid, text="Rendering API:", font=ctk.CTkFont(size=11, weight="bold")).grid(row=2, column=0, sticky="w", pady=6)
        lbl_render = ctk.CTkLabel(grid, text="DirectX+ (RTX 3090 Dedicated GPU Locked)", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=COLOR_GREEN)
        lbl_render.grid(row=2, column=1, sticky="w", padx=15, pady=6)

        btn_save_engine = ctk.CTkButton(
            ecard, text="SYNCHRONIZE ENGINE REGISTRY NOW",
            command=self._apply_engine_settings,
            font=ctk.CTkFont(size=12, weight="bold"), fg_color=COLOR_CYAN, text_color="#002022", hover_color=COLOR_CYAN_HOVER, height=38
        )
        btn_save_engine.pack(anchor="w", padx=15, pady=(10, 4))

    def _apply_engine_settings(self):
        r_val = self.res_opt.get()
        if "2560x1440" in r_val:
            w, h = 2560, 1440
        elif "2560x1080" in r_val:
            w, h = 2560, 1080
        elif "1600x900" in r_val:
            w, h = 1600, 900
        else:
            w, h = 1920, 1080

        dpi = 480 if "480" in self.dpi_opt.get() else (320 if "320" in self.dpi_opt.get() else 240)

        def worker():
            self.engine.sync_gameloop_registry(res_width=w, res_height=h, dpi=dpi)
            if self.sound_enabled:
                play_cyber_chime("click")
            self.after(500, self.update_telemetry)
        threading.Thread(target=worker, daemon=True).start()

    # -------------------------------------------------------------------------
    # TAB 7: INODE & BACKUP MANAGER
    # -------------------------------------------------------------------------
    def show_inodes(self):
        self._clear_content()
        self._set_active_tab("inodes")

        container = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        container.pack(fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text="🛡️ ROOTFS INODES & SAFETY SNAPSHOTS", font=ctk.CTkFont(size=16, weight="bold"), text_color=COLOR_CYAN)
        lbl.pack(anchor="w", pady=(0, 14))

        abox = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        abox.pack(fill="x", pady=(0, 14), padx=4, ipady=6)

        ctk.CTkButton(
            abox, text="CREATE SNAPSHOT BACKUP",
            command=lambda: [self.engine.backup_all_configs(), play_cyber_chime("click")],
            font=ctk.CTkFont(size=11, weight="bold"), fg_color=COLOR_CYAN, text_color="#002022", hover_color=COLOR_CYAN_HOVER
        ).pack(side="left", padx=12)

        ctk.CTkButton(
            abox, text="LOCK ALL READ-ONLY",
            command=lambda: [self.engine.lock_all_inodes(), play_cyber_chime("click")],
            font=ctk.CTkFont(size=11, weight="bold"), fg_color=COLOR_CARD_HOVER, hover_color="#243048"
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            abox, text="UNLOCK ALL READ-WRITE",
            command=lambda: [self.engine.unlock_all_inodes(), play_cyber_chime("click")],
            font=ctk.CTkFont(size=11, weight="bold"), fg_color="transparent", text_color=COLOR_GOLD, border_width=1, border_color=COLOR_GOLD, hover_color="#332B14"
        ).pack(side="left", padx=4)

        lcard = ctk.CTkFrame(container, fg_color=COLOR_CARD, corner_radius=10, border_width=1, border_color=COLOR_BORDER)
        lcard.pack(fill="x", padx=4, ipady=8)
        ctk.CTkLabel(lcard, text="MANAGED GUEST INODES & DISK MIRRORS", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_TEXT).pack(anchor="w", padx=15, pady=(4, 8))

        all_inodes = self.engine.paths["usercustom_inodes"] + self.engine.paths["gvas_save_inodes"]
        for p in list(dict.fromkeys(all_inodes)):
            exists = os.path.exists(p)
            status_text = "● ON DISK" if exists else "○ MIRROR READY"
            status_color = COLOR_GREEN if exists else COLOR_MUTED

            row = ctk.CTkFrame(lcard, fg_color="#0D111A", corner_radius=6)
            row.pack(fill="x", padx=15, pady=3)

            base = os.path.basename(p)
            ctk.CTkLabel(row, text=base, font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=COLOR_CYAN).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row, text=p, font=ctk.CTkFont(size=10), text_color=COLOR_MUTED).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row, text=status_text, font=ctk.CTkFont(size=9, weight="bold"), text_color=status_color).pack(side="right", padx=10, pady=5)

    # -------------------------------------------------------------------------
    # PERIODIC TELEMETRY UPDATES (PURE WIN32 CTYPES - ZERO POPUPS)
    # -------------------------------------------------------------------------
    def update_telemetry(self):
        if getattr(self, "_is_closing", False):
            return
        diag = self.engine.get_live_diagnostics()

        if hasattr(self, "badge_timer"):
            res = diag.get("timer_resolution_ms", 15.6)
            self.badge_timer.configure(text=f"{res:.2f} ms", text_color=COLOR_GREEN if res <= 1.0 else COLOR_GOLD)

        if hasattr(self, "badge_fps"):
            locked = diag.get("fps_locked", False)
            self.badge_fps.configure(text="120 FPS" if locked else "90 FPS", text_color=COLOR_GREEN if locked else COLOR_GOLD)

        if self.current_tab == "dashboard" and hasattr(self, "card_device"):
            dev_val, dev_det = self.card_device
            dev_val.configure(text=diag.get("phone_device", "REDMAGIC 9 Pro"))
            dev_det.configure(text=f"{diag.get('device_model', 'NX769J')} [nubia] Locked")

            hdr_val, hdr_det = self.card_hdr
            if diag.get("fps_locked"):
                hdr_val.configure(text="Streamer HDR 120", text_color=COLOR_GREEN)
                hdr_det.configure(text="Verified Setup (BattleFPS=8 | Q=6) Locked")
            else:
                hdr_val.configure(text="Not Synchronized", text_color=COLOR_RED)
                hdr_det.configure(text="Click 1-Click Master Boost below")

            dvr_val, dvr_det = self.card_dvr
            if diag.get("dvr_disabled"):
                dvr_val.configure(text="DVR Stutter OFF", text_color=COLOR_GREEN)
                dvr_det.configure(text="Replays OFF & Async 5.0ms Locked")
            else:
                dvr_val.configure(text="DVR Active", text_color=COLOR_GOLD)
                dvr_det.configure(text="Potential micro-stutter detected")

            net_val, net_det = self.card_net
            if diag.get("network_optimized"):
                net_val.configure(text="Esports Tuned", text_color=COLOR_GREEN)
                net_det.configure(text="Nagle OFF | Throttling Disabled")
            else:
                net_val.configure(text="Default Stack", text_color=COLOR_GOLD)
                net_det.configure(text="Click 1-Click Master Boost to tune")

            tim_val, tim_det = self.card_timer
            res = diag.get("timer_resolution_ms", 15.6)
            tim_val.configure(text=f"{res:.2f} ms Pacing", text_color=COLOR_GREEN if res <= 1.0 else COLOR_GOLD)
            tim_det.configure(text="Sub-millisecond mouse polling active" if res <= 1.0 else "Click to lock 0.50ms")

            mem_val, mem_det = self.card_mem
            mem_val.configure(text=f"{diag.get('virtual_avail_gb', 0.0)} GB Free")
            mem_det.configure(text=f"Total Commit: {diag.get('virtual_commit_gb', 0.0)} GB")

        if hasattr(self, "mini_hud") and self.mini_hud and self.mini_hud.winfo_viewable():
            self.mini_hud.update_stats()

    def _periodic_status_checker(self):
        if getattr(self, "_is_closing", False):
            return
        self.update_telemetry()
        if not getattr(self, "_is_closing", False):
            self.after(3000, self._periodic_status_checker)

    def on_closing(self):
        self._is_closing = True
        try:
            if hasattr(self, "mini_hud") and self.mini_hud:
                self.mini_hud.destroy()
        except Exception:
            pass
        try:
            self.destroy()
        except Exception:
            pass
        import os
        os._exit(0)

if __name__ == "__main__":
    app = PanelLoopApp()
    app.mainloop()
