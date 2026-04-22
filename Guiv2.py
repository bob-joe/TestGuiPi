import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
import os
import sys


class RecyclerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Filament Recycler Control Panel")
        self.root.geometry("700x520")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)
        self.root.attributes('-fullscreen', True)


        self.status_text = tk.StringVar(value="Idle")
        self.timer_text  = tk.StringVar(value="00:00")
        self.speed_mode  = tk.StringVar(value="Low Load")
        self.running     = False
        self.paused      = False
        self.elapsed_on_pause = 0
        self.start_time  = 0

        self.C = dict(
            BG="#1e1e2e", SURFACE="#2a2a3e", SRF2="#313150",
            ACCENT="#7c5cbf", ACCENT2="#a87dd6",
            TEXT="#e0e0f0", MUTED="#9090b0",
            SUCCESS="#3ddc84", WARNING="#f0a500", ERROR="#e05555",
            DIV="#3a3a5a",
        )
        C = self.C

        # ── TOP BAR ──────────────────────────────────────────────────
        top = tk.Frame(self.root, bg=C["SURFACE"], padx=12, pady=10)
        top.pack(fill="x")

        self.logo_lbl = tk.Label(top, bg=C["SURFACE"])
        self.logo_lbl.pack(side="left", padx=10)
        self._load_logo()

        title_col = tk.Frame(top, bg=C["SURFACE"])
        title_col.pack(side="left", padx=12)
        tk.Label(title_col, text="3D Filament Recycler",
                 font=("Segoe UI", 17, "bold"), fg=C["TEXT"], bg=C["SURFACE"]).pack(anchor="w")
        tk.Label(title_col, text="Raspberry Pi Control Panel",
                 font=("Segoe UI", 9), fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w")

        tk.Frame(root, height=2, bg=C["DIV"]).pack(fill="x")

        # ── BODY ─────────────────────────────────────────────────────
        body = tk.Frame(root, bg=C["BG"])
        body.pack(fill="both", expand=True, padx=20, pady=12)

        left = tk.Frame(body, bg=C["BG"])
        left.pack(side="left", fill="both", expand=True)

        # Timer card
        tc = tk.Frame(left, bg=C["SURFACE"], padx=16, pady=14)
        tc.pack(fill="x", pady=(0, 12))
        tk.Label(tc, text="SESSION TIMER", font=("Segoe UI", 8, "bold"),
                 fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w")
        tk.Label(tc, textvariable=self.timer_text,
                 font=("Courier New", 40, "bold"),
                 fg=C["ACCENT2"], bg=C["SURFACE"]).pack(pady=(2, 0))

        # Speed control card
        sc = tk.Frame(left, bg=C["SURFACE"], padx=16, pady=14)
        sc.pack(fill="x", pady=(0, 12))
        tk.Label(sc, text="MATERIAL / LOAD MODE", font=("Segoe UI", 8, "bold"),
                 fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w", pady=(0, 8))
        mode_row = tk.Frame(sc, bg=C["SURFACE"])
        mode_row.pack(fill="x")
        self.low_btn  = self._mode_btn(mode_row, "TPU  (Low Load)",  "Low Load")
        self.high_btn = self._mode_btn(mode_row, "PLA  (High Load)", "High Load")
        self.low_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.high_btn.pack(side="left", expand=True, fill="x")
        self.speed_mode.trace_add("write", self._update_mode_buttons)
        self._update_mode_buttons()

        # Controls card
        cc = tk.Frame(left, bg=C["SURFACE"], padx=16, pady=14)
        cc.pack(fill="x")
        tk.Label(cc, text="CONTROLS", font=("Segoe UI", 8, "bold"),
                 fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w", pady=(0, 8))
        ctrl_row = tk.Frame(cc, bg=C["SURFACE"])
        ctrl_row.pack(fill="x")
        self.start_btn = tk.Button(
            ctrl_row, text="START",
            font=("Segoe UI", 11, "bold"), fg="#fff", bg=C["SUCCESS"],
            activebackground="#2cb870", relief="flat", padx=14, pady=8,
            cursor="hand2", command=self.start_process)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.pause_btn = tk.Button(
            ctrl_row, text="PAUSE",
            font=("Segoe UI", 11, "bold"), fg="#fff", bg=C["WARNING"],
            activebackground="#cc8800", relief="flat", padx=14, pady=8,
            cursor="hand2", command=self.pause_process)
        self.pause_btn.pack(side="left", expand=True, fill="x")
        tk.Button(cc, text="STOP / RESET",
                  font=("Segoe UI", 10), fg="#fff", bg=C["ERROR"],
                  activebackground="#b83333", relief="flat", padx=14, pady=6,
                  cursor="hand2", command=self.stop_process).pack(fill="x", pady=(8, 0))

        # Right info panel
        right = tk.Frame(body, bg=C["SURFACE"], padx=14, pady=14, width=190)
        right.pack(side="right", fill="y", padx=(16, 0))
        right.pack_propagate(False)

        tk.Label(right, text="SYSTEM INFO", font=("Segoe UI", 8, "bold"),
                 fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w")
        tk.Frame(right, height=1, bg=C["DIV"]).pack(fill="x", pady=6)
        for label, var in [("Mode", self.speed_mode), ("Status", self.status_text)]:
            r = tk.Frame(right, bg=C["SURFACE"])
            r.pack(fill="x", pady=4)
            tk.Label(r, text=label, font=("Segoe UI", 9), fg=C["MUTED"],
                     bg=C["SURFACE"], anchor="w", width=8).pack(side="left")
            tk.Label(r, textvariable=var, font=("Segoe UI", 9, "bold"),
                     fg=C["TEXT"], bg=C["SURFACE"], anchor="w").pack(side="left")

        tk.Frame(right, height=1, bg=C["DIV"]).pack(fill="x", pady=10)
        tk.Label(right, text="GPIO PINS", font=("Segoe UI", 8, "bold"),
                 fg=C["MUTED"], bg=C["SURFACE"]).pack(anchor="w")
        for name, pin in [("Motor 1","GPIO 17"),("Motor 2","GPIO 27"),
                          ("Fan","GPIO 22"),("Heat","GPIO 18"),
                          ("Thermistor","GPIO 4"),("LCD","I2C 0x27")]:
            r = tk.Frame(right, bg=C["SURFACE"])
            r.pack(fill="x", pady=2)
            tk.Label(r, text=name, font=("Segoe UI", 8), fg=C["MUTED"],
                     bg=C["SURFACE"], anchor="w", width=10).pack(side="left")
            tk.Label(r, text=pin, font=("Courier New", 8, "bold"),
                     fg=C["ACCENT2"], bg=C["SURFACE"], anchor="w").pack(side="left")

        # ── STATUS BAR ────────────────────────────────────────────────
        self.status_bar = tk.Label(
            root, text="Status: Idle", font=("Segoe UI", 9),
            fg=C["MUTED"], bg=C["DIV"], anchor="w", padx=12, pady=4)
        self.status_bar.pack(side="bottom", fill="x")

    # ── HELPERS ──────────────────────────────────────────────────────

    def _mode_btn(self, parent, label, value):
        C = self.C
        return tk.Button(parent, text=label, font=("Segoe UI", 9, "bold"),
                         fg=C["TEXT"], bg=C["SRF2"],
                         activebackground=C["ACCENT"], activeforeground="#fff",
                         relief="flat", padx=8, pady=6, cursor="hand2",
                         command=lambda v=value: self.speed_mode.set(v))

    def _update_mode_buttons(self, *_):
        C = self.C
        mode = self.speed_mode.get()
        self.low_btn.config(bg=C["ACCENT"] if mode == "Low Load" else C["SRF2"],
                            fg="#fff" if mode == "Low Load" else C["TEXT"])
        self.high_btn.config(bg=C["ACCENT"] if mode == "High Load" else C["SRF2"],
                             fg="#fff" if mode == "High Load" else C["TEXT"])

    def _set_status(self, text, color):
        self.status_text.set(text)
        self.status_bar.config(text=f"Status: {text}", fg=color)

    # ── IMAGE UPLOAD ─────────────────────────────────────────────────

    def _load_logo(self):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        logo_path  = os.path.join(script_dir, "PCompanylogo.png")

        if os.path.exists(logo_path):
            try:
                img   = Image.open(logo_path).resize((54, 54), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.logo_lbl.config(image=photo)
                self.logo_lbl.image = photo
                self._logo_photo    = photo
            except Exception as exc:
                messagebox.showerror("Logo Error",
                                     f"Could not load PCompanylogo.png:\n{exc}")
                self._show_logo_fallback()
        else:
            self._show_logo_fallback()

    def _show_logo_fallback(self):
        self.logo_lbl.config(
            text="⬡", font=("Arial", 30),
            fg=self.C["ACCENT2"], bg=self.C["SURFACE"])

    # ── CONTROLS ─────────────────────────────────────────────────────

    def start_process(self):
        C = self.C
        if self.paused:
            self.paused = False
            self.running = True
            self.start_time = time.time() - self.elapsed_on_pause
            self._set_status("Running", C["SUCCESS"])
            self.start_btn.config(text="RUNNING", bg=C["SUCCESS"], state="disabled")
            self.pause_btn.config(state="normal")
            self.root.after(0, self._tick)
            print(f"[GPIO] Resumed – {self.speed_mode.get()}")
        elif not self.running:
            self.running = True
            self.paused = False
            self.elapsed_on_pause = 0
            self.start_time = time.time()
            self._set_status("Running", C["SUCCESS"])
            self.start_btn.config(state="disabled", text="RUNNING", bg=C["SUCCESS"])
            self.pause_btn.config(state="normal")
            self.root.after(0, self._tick)
            print(f"[GPIO] Started – {self.speed_mode.get()}")

    def pause_process(self):
        C = self.C
        if self.running:
            self.running = False
            self.paused = True
            self.elapsed_on_pause = int(time.time() - self.start_time)
            self._set_status("Paused", C["WARNING"])
            self.start_btn.config(state="normal", text="RESUME", bg="#5599cc")
            self.pause_btn.config(state="disabled")
            print("[GPIO] Paused")

    def stop_process(self):
        C = self.C
        self.running = False
        self.paused = False
        self.elapsed_on_pause = 0
        self.timer_text.set("00:00")
        self._set_status("Idle", C["MUTED"])
        self.start_btn.config(state="normal", text="START", bg=C["SUCCESS"])
        self.pause_btn.config(state="normal")
        print("[GPIO] Stopped")

    def _tick(self):
        if self.running:
            e = int(time.time() - self.start_time)
            self.timer_text.set(f"{e // 60:02}:{e % 60:02}")
            self.root.after(1000, self._tick)


if __name__ == "__main__":
    root = tk.Tk()
    app = RecyclerGUI(root)
    root.mainloop()
