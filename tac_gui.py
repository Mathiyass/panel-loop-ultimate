"""
PANEL LOOP ULTIMATE - Graphical Desktop Application (GUI)
Modern Dark-Mode Dashboard for GameLoop & PUBG Mobile Optimization
"""

import sys
import os
import threading
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
import tac_engine

BG_DARK = "#121216"
BG_CARD = "#1c1c24"
BG_CARD_ACCENT = "#252532"
FG_TEXT = "#e0e0e6"
FG_MUTED = "#8e8e9e"
COLOR_PRIMARY = "#f53b57"      # Vibrant Esports Red
COLOR_ACCENT = "#3c40c6"       # Deep Indigo
COLOR_SUCCESS = "#05c46b"      # Neon Green
COLOR_WARNING = "#ffa801"      # Amber
COLOR_CONSOLE = "#0a0a0d"

class TacGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PANEL LOOP ULTIMATE - GameLoop & PUBG MOBILE Master Suite")
        self.root.geometry("860x780")
        self.root.minsize(800, 700)
        self.root.configure(bg=BG_DARK)

        self._build_styles()
        self._build_header()
        self._build_telemetry_cards()
        self._build_action_buttons()
        self._build_console()

        self.auto_guard_active = False

        # Initial telemetry load & background periodic refresh
        self.refresh_telemetry()
        self._auto_refresh()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=BG_DARK)
        style.configure("Card.TFrame", background=BG_CARD, relief="flat")
        style.configure("CardAccent.TFrame", background=BG_CARD_ACCENT, relief="flat")

    def _build_header(self):
        hdr_frame = tk.Frame(self.root, bg=BG_DARK, pady=10, padx=20)
        hdr_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            hdr_frame,
            text="PANEL LOOP ULTIMATE",
            font=("Segoe UI", 18, "bold"),
            fg=COLOR_PRIMARY,
            bg=BG_DARK
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            hdr_frame,
            text="Esports 120 FPS Lock  •  GameLoop UI 90 Sync  •  Dynamic RTX 3090 Cooling  •  AMD Ryzen 7 5800X",
            font=("Segoe UI", 9),
            fg=FG_MUTED,
            bg=BG_DARK
        )
        sub_lbl.pack(anchor="w")

    def _build_telemetry_cards(self):
        cards_frame = tk.Frame(self.root, bg=BG_DARK, padx=20, pady=5)
        cards_frame.pack(fill=tk.X)

        # 4 Telemetry metrics
        self.card_model_val = tk.StringVar(value="Loading...")
        self.card_res_val = tk.StringVar(value="Loading...")
        self.card_fps_val = tk.StringVar(value="Loading...")
        self.card_gpu_val = tk.StringVar(value="Loading...")

        cards_data = [
            ("DEVICE MODEL", self.card_model_val, COLOR_PRIMARY),
            ("DISPLAY RESOLUTION", self.card_res_val, COLOR_WARNING),
            ("IN-GAME / UI FPS", self.card_fps_val, COLOR_SUCCESS),
            ("THERMALS & NETWORK", self.card_gpu_val, "#00d2d3")
        ]

        for i, (title, var, accent_color) in enumerate(cards_data):
            card = tk.Frame(cards_frame, bg=BG_CARD, bd=0, padx=12, pady=10, highlightthickness=1, highlightbackground=BG_CARD_ACCENT)
            card.grid(row=0, column=i, sticky="nsew", padx=5)
            cards_frame.columnconfigure(i, weight=1)

            t_lbl = tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg=FG_MUTED, bg=BG_CARD)
            t_lbl.pack(anchor="w")

            v_lbl = tk.Label(card, textvariable=var, font=("Segoe UI", 11, "bold"), fg=accent_color, bg=BG_CARD)
            v_lbl.pack(anchor="w", pady=(4, 0))

    def _build_action_buttons(self):
        btn_frame = tk.Frame(self.root, bg=BG_DARK, padx=20, pady=10)
        btn_frame.pack(fill=tk.X)

        # Row 1: Primary actions
        row1 = tk.Frame(btn_frame, bg=BG_DARK)
        row1.pack(fill=tk.X, pady=4)

        b_opt = tk.Button(
            row1, text="🚀  1-Click Ultimate 120 FPS + UHD",
            font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=COLOR_PRIMARY,
            activebackground="#ff4d6d", activeforeground="#ffffff",
            bd=0, padx=15, pady=8, cursor="hand2",
            command=self.run_full_optimize
        )
        b_opt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        b_pacing = tk.Button(
            row1, text="⚡  120 FPS Pacing Lock",
            font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=COLOR_ACCENT,
            activebackground="#575fcf", activeforeground="#ffffff",
            bd=0, padx=15, pady=8, cursor="hand2",
            command=self.run_pacing
        )
        b_pacing.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        b_launch = tk.Button(
            row1, text="🎮  Launch PUBG Mobile",
            font=("Segoe UI", 10, "bold"), fg="#ffffff", bg=COLOR_SUCCESS,
            activebackground="#2ed573", activeforeground="#ffffff",
            bd=0, padx=15, pady=8, cursor="hand2",
            command=self.run_launch
        )
        b_launch.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        # Row 2: Model Switchers
        row2 = tk.Frame(btn_frame, bg=BG_DARK)
        row2.pack(fill=tk.X, pady=4)

        models = [
            ("📱 REDMAGIC 9 Pro", "redmagic"),
            ("📱 ROG 8 Pro", "rog"),
            ("📱 S24 Ultra", "samsung"),
            ("📱 Tab S9 Ultra", "tabs9"),
            ("📱 Xiaomi 13 Pro", "xiaomi")
        ]
        for name, key in models:
            b = tk.Button(
                row2, text=name, font=("Segoe UI", 9), fg=FG_TEXT, bg=BG_CARD,
                activebackground=BG_CARD_ACCENT, activeforeground="#ffffff",
                bd=0, pady=6, cursor="hand2",
                command=lambda k=key: self.run_model(k)
            )
            b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # Row 3: Resolution Switchers & Utilities
        row3 = tk.Frame(btn_frame, bg=BG_DARK)
        row3.pack(fill=tk.X, pady=4)

        res_actions = [
            ("🖥️ Fullscreen (F11)", self.run_fullscreen),
            ("🖥️ FHD (1920x1080)", lambda: self.run_res(1920, 1080, 480)),
            ("🖥️ 2K (2560x1440)", lambda: self.run_res(2560, 1440, 640)),
            ("🖥️ iPad (1440x1080)", lambda: self.run_res(1440, 1080, 400)),
            ("🧹 Deep Clean", self.run_clean),
            ("🛡️ Crash Guard", self.run_guard),
            ("🌐 0ms Network", self.run_turbo),
            ("🔄 Refresh", self.refresh_telemetry)
        ]
        for name, cmd in res_actions:
            b = tk.Button(
                row3, text=name, font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
                activebackground="#333342", activeforeground="#ffffff",
                bd=0, pady=6, cursor="hand2",
                command=cmd
            )
            b.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Row 4: Reverse-Engineered Upgrades (Auto-Guard, Backup, Restore, Watermark)
        row4 = tk.Frame(btn_frame, bg=BG_DARK)
        row4.pack(fill=tk.X, pady=4)

        self.guard_btn = tk.Button(
            row4, text="🛡️ Auto-Guard: OFF", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.toggle_auto_guard
        )
        self.guard_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_bk = tk.Button(
            row4, text="💾 Snapshot Backup", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_backup
        )
        b_bk.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_rst = tk.Button(
            row4, text="↩️ Factory Restore", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_restore
        )
        b_rst.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_wm = tk.Button(
            row4, text="👁️ Clean Screen", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_watermark_toggle
        )
        b_wm.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_stream = tk.Button(
            row4, text="📹 Streamer Mode", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_streamer_mode
        )
        b_stream.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Row 5: Pro Esports Systems (Mouse Keeper, Notice Tamer, Auto-Repair, Camera Tuning, Keymap Shield)
        row5 = tk.Frame(btn_frame, bg=BG_DARK)
        row5.pack(fill=tk.X, pady=4)

        b_mk = tk.Button(
            row5, text="🖱️ Mouse Keeper", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_mouse_keeper
        )
        b_mk.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_nt = tk.Button(
            row5, text="🔇 Notice Tamer", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_notice_tamer
        )
        b_nt.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_rep = tk.Button(
            row5, text="🩺 Auto-Repair", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_auto_repair
        )
        b_rep.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_cam = tk.Button(
            row5, text="🎯 Camera Tuning", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_camera_tuning
        )
        b_cam.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_km = tk.Button(
            row5, text="⌨️ Keymap Shield", font=("Segoe UI", 8, "bold"), fg=FG_TEXT, bg=BG_CARD_ACCENT,
            activebackground="#333342", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_keymap_protect
        )
        b_km.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Row 6: Ultra-Refresh 180Hz / 240 FPS & Lossless Scaling
        row6 = tk.Frame(btn_frame, bg=BG_DARK)
        row6.pack(fill=tk.X, pady=4)

        b_hr180 = tk.Button(
            row6, text="⚡ 180Hz Monitor Sync", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#8854d0",
            activebackground="#a55eea", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=lambda: self.run_high_refresh(180)
        )
        b_hr180.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_hr240 = tk.Button(
            row6, text="🚀 240 FPS Uncapped Pipeline", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#eb3b5a",
            activebackground="#fc5c65", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=lambda: self.run_high_refresh(240)
        )
        b_hr240.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        b_ls = tk.Button(
            row6, text="✨ Lossless Scaling 240 FPS Setup", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#20bf6b",
            activebackground="#26de81", activeforeground="#ffffff",
            bd=0, pady=6, cursor="hand2",
            command=self.run_lossless_guide
        )
        b_ls.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def _build_console(self):
        con_frame = tk.Frame(self.root, bg=BG_DARK, padx=20, pady=5)
        con_frame.pack(fill=tk.BOTH, expand=True)

        lbl = tk.Label(con_frame, text="ACTIVITY LOG & VERIFICATION OUTPUT", font=("Segoe UI", 8, "bold"), fg=FG_MUTED, bg=BG_DARK)
        lbl.pack(anchor="w")

        self.console = tk.Text(
            con_frame, bg=COLOR_CONSOLE, fg="#3ae374",
            insertbackground="#ffffff", font=("Consolas", 9),
            bd=0, padx=10, pady=10, wrap=tk.WORD
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(self.console, command=self.console.yview, bg=BG_CARD)
        self.console.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def log(self, text):
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)

    def _run_async(self, target_fn, name="Task"):
        def wrapper():
            self.log(f"\n--- [Starting {name}] ---")
            try:
                target_fn()
            except Exception as e:
                self.log(f"[Error in {name}]: {e}")
            finally:
                self.log(f"--- [Finished {name}] ---\n")
                self.root.after(500, self.refresh_telemetry)
        threading.Thread(target=wrapper, daemon=True).start()

    def refresh_telemetry(self):
        try:
            s = tac_engine.get_system_status()
            self.card_model_val.set(f"{s['model']}")
            self.card_res_val.set(f"{s['res_w']}x{s['res_h']} (Direct Flip)")
            in_game = "120 FPS Locked" if s['save_fps'] == 8 else f"{s['save_fps']} FPS"
            ui_fps = f"{s['ui_fps']} FPS"
            self.card_fps_val.set(f"{in_game} | UI {ui_fps}")
            timer_text = s.get('timer_res', '0.50 ms')
            nic_text = f"{s.get('nic_count', 0)} NICs"
            self.card_gpu_val.set(f"{s['gpu_temp']} | {nic_text} | {timer_text}")
        except Exception as e:
            self.log(f"[Telemetry error]: {e}")

    def _auto_refresh(self):
        self.refresh_telemetry()
        self.root.after(5000, self._auto_refresh)

    def toggle_auto_guard(self):
        self.auto_guard_active = not self.auto_guard_active
        if self.auto_guard_active:
            self.guard_btn.config(text="🛡️ Auto-Guard: ACTIVE", bg=COLOR_SUCCESS)
            self.log("[Auto-Guard] Background protection thread STARTED (monitoring drift every 30s)...")
            threading.Thread(target=self._guard_worker, daemon=True).start()
        else:
            self.guard_btn.config(text="🛡️ Auto-Guard: OFF", bg=BG_CARD_ACCENT)
            self.log("[Auto-Guard] Background protection thread STOPPED.")

    def _guard_worker(self):
        while self.auto_guard_active:
            try:
                s = tac_engine.get_system_status()
                if s["save_fps"] != 8 or s["ui_fps"] != 90:
                    self.log(f"[Auto-Guard] Drift detected (save_fps={s['save_fps']}, ui_fps={s['ui_fps']}). Re-locking 120 FPS...")
                    tac_engine.apply_full_optimization(1920, 1080, 480, 120)
                    self.refresh_telemetry()
            except Exception as e:
                self.log(f"[Auto-Guard error]: {e}")
            for _ in range(30):
                if not self.auto_guard_active:
                    break
                time.sleep(1)

    def run_backup(self):
        def task():
            self.log("[Action] Creating full environment backup snapshot...")
            bdir = tac_engine.backup_environment()
            self.log(f">> Snapshot successfully stored at:\n   {bdir}")
        self._run_async(task, "Backup Environment Snapshot")

    def run_restore(self):
        if messagebox.askyesno("Confirm Factory Restore", "Do you want to restore from the latest snapshot or revert to clean defaults?"):
            def task():
                self.log("[Action] Restoring environment...")
                tac_engine.restore_factory_defaults()
                self.log(">> Restoration complete!")
            self._run_async(task, "Factory Restore")

    def run_watermark_toggle(self):
        def task():
            s = tac_engine.get_system_status()
            new_state = not s.get("watermark_hidden", False)
            tac_engine.set_watermark_suppression(new_state)
            self.log(f">> Watermark Clean Screen: {'ENABLED (Clean Screen)' if new_state else 'DISABLED (Default Hints)'}")
        self._run_async(task, "Toggle Watermark Suppression")

    def run_pacing(self):
        def task():
            self.log("[Action] Enforcing 120 FPS Pacing & DirectX Direct Scanout...")
            tac_engine.lock_framerate_pacing()
            self.log(">> 0.50ms Kernel Timer Resolution Active!")
            self.log(">> Emulator Process Elevated to HIGH Priority!")
            self.log(">> DirectX Direct Scanout (Independent Flip) Registered!")
            self.log(">> PRO TIP: Press [F11] in GameLoop for 1080p True Fullscreen (0ms DWM Lag)!")
        self._run_async(task, "120 FPS Pacing Lock")

    def run_fullscreen(self):
        def task():
            self.log("[Action] Toggling GameLoop True 1080p Fullscreen (F11)...")
            ok = tac_engine.toggle_gameloop_fullscreen()
            if ok:
                self.log(">> Fullscreen [F11] Sent! Direct Hardware Scanout active.")
            else:
                self.log(">> Notice: You can also press [F11] on your keyboard in GameLoop.")
        self._run_async(task, "Toggle Fullscreen")

    def run_full_optimize(self):
        def task():
            tac_engine.apply_full_optimization(1920, 1080, 480, 120)
            self.log("[Success] 1-Click Ultimate 120 FPS + UHD applied cleanly!")
        self._run_async(task, "1-Click Ultimate Optimization")

    def run_launch(self):
        def task():
            try:
                subprocess.Popen([tac_engine.EMULATOR_EXE, "-vm", "100"])
                self.log("[Success] PUBG Mobile launched with flag -vm 100")
            except Exception:
                try:
                    subprocess.Popen([tac_engine.APPMARKET_EXE, "-runpkg", "com.tencent.ig"])
                    self.log("[Success] PUBG Mobile launched via AppMarket")
                except Exception as e:
                    self.log(f"[Launch Failed]: {e}")
        self._run_async(task, "Launch PUBG Mobile")

    def run_model(self, model_key):
        def task():
            tac_engine.switch_model(model_key)
            self.log(f"[Success] Switched device model to: {model_key}")
        self._run_async(task, f"Model Switch: {model_key}")

    def run_res(self, rw, rh, dpi):
        def task():
            tac_engine.set_resolution(rw, rh, dpi)
            self.log(f"[Success] Resolution switched to {rw}x{rh} DPI {dpi}")
        self._run_async(task, f"Set Resolution {rw}x{rh}")

    def run_clean(self):
        def task():
            tac_engine.deep_clean()
            self.log("[Success] Deep cleaner finished!")
        self._run_async(task, "Deep Cleaner")

    def run_guard(self):
        def task():
            tac_engine.crash_guard()
            self.log("[Success] Crash guard executed, memory trimmed!")
        self._run_async(task, "Crash Guard")

    def run_turbo(self):
        def task():
            tac_engine.network_turbo()
            self.log("[Success] 0ms Network Turbo active!")
        self._run_async(task, "Network Turbo")

    def run_mouse_keeper(self):
        def task():
            self.log("[Action] Activating Mouse Keeper & 1:1 Raw Mouse Sensor tracking...")
            tac_engine.apply_raw_mouse_1to1()
            tac_engine.fence_cursor_to_gameloop(True)
            self.log(">> 1:1 Raw Mouse Tracking Enforced (0 Accel)!")
            self.log(">> Cursor Fencing Active for GameLoop Viewport!")
        self._run_async(task, "Mouse Keeper")

    def run_notice_tamer(self):
        def task():
            self.log("[Action] Scanning and suppressing promotional & nag popups...")
            n = tac_engine.run_notice_tamer()
            self.log(f">> Notice Tamer finished ({n} intrusive dialogs suppressed)!")
        self._run_async(task, "Notice Tamer")

    def run_auto_repair(self):
        def task():
            self.log("[Action] Running PUBG Mobile & OpenGL Self-Healing Recovery...")
            tac_engine.repair_pubg_and_opengl()
            self.log(">> Self-Healing Recovery complete!")
        self._run_async(task, "Auto-Repair")

    def run_camera_tuning(self):
        def task():
            self.log("[Action] Applying Esports Flick-Turn & FOV Calibration...")
            tac_engine.apply_camera_tuning()
            self.log(">> Flick-Turn & Diagonal Sensitivity Curves Active!")
        self._run_async(task, "Camera Tuning")

    def run_streamer_mode(self):
        def task():
            self.log("[Action] Activating 1080p Borderless Streamer Mode...")
            ok = tac_engine.set_streamer_mode()
            if ok:
                self.log(">> Streamer Mode active! Borderless 1080p ready for OBS capture.")
            else:
                self.log(">> Ensure GameLoop is open first.")
        self._run_async(task, "Streamer Mode")

    def run_keymap_protect(self):
        def task():
            self.log("[Action] Backing up and locking custom keybindings...")
            tac_engine.protect_keymaps()
            self.log(">> Keymap Shield active! Custom keybindings secured against updates.")
        self._run_async(task, "Keymap Shield")

    def run_high_refresh(self, hz=180):
        def task():
            self.log(f"[Action] Enforcing {hz}Hz / 240 FPS Ultra-Fluidity Pipeline...")
            tac_engine.enable_high_refresh_mode(hz)
            self.log(f">> GameLoop Host VMRefreshRate locked to {hz}Hz!")
            self.log(">> UE4 Render Thread uncapped: t.MaxFPS=240, r.OneFrameThreadLag=0, r.GTSyncType=0!")
            self.log(">> Android SurfaceFlinger & Mouse Input locked to 240Hz events!")
            self.log(f">> {hz}Hz / 240 FPS Mode active and locked!")
        self._run_async(task, f"{hz}Hz / 240 FPS Mode")

    def run_lossless_guide(self):
        guide = os.path.join(os.getcwd(), 'LOSSLESS_SCALING_240FPS_GUIDE.md')
        if os.path.exists(guide):
            try:
                os.startfile(guide)
                self.log(">> Opened LOSSLESS_SCALING_240FPS_GUIDE.md")
            except Exception:
                pass
        self.log(">> Lossless Scaling Tip: Use LSFG 2x/3x with WGC capture API to turn 120 FPS into 240 FPS on RTX 3090!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TacGuiApp(root)
    root.mainloop()
