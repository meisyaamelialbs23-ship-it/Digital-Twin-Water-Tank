import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# ============================================================
# DIGITAL TWIN TANGKI AIR - INISIALISASI UI/UX
# Berdasarkan rancangan UX/UI:
# Login, Dashboard Real-Time, Grafik, Riwayat,
# Pengaturan Ambang Batas, dan Log Notifikasi.
# ============================================================

# ---------- Palet warna ----------
GREEN = "#28a745"       # Normal / Online
YELLOW = "#ffc107"      # Waspada
RED = "#dc3545"         # Bahaya / Offline
BLUE = "#0d6efd"        # Visual air
DARK = "#172033"
BG = "#f4f6f9"
WHITE = "#ffffff"
TEXT = "#222222"
GRAY = "#6c757d"


class DigitalTwinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Twin Tangki Air")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)

        # Data awal sesuai wireframe
        self.level = 120
        self.temperature = 27.5
        self.turbidity = 3.2
        self.tds = 320

        self.thresholds = {
            "level_min": 40,
            "level_max": 150,
            "temp_min": 15,
            "temp_max": 35,
            "turbidity_max": 5,
            "tds_max": 500
        }

        self.history = [
            ("10:32:05", 120, 27.5, 3.2, 320, "Normal"),
            ("10:31:55", 119, 27.5, 3.1, 318, "Normal"),
            ("10:31:45", 118, 27.4, 3.3, 355, "Waspada"),
        ]

        self.notifications = [
            ("10:15", "Tangki Utama", "Level air di bawah 80 cm", "Info"),
            ("09:40", "Tangki Utama", "TDS mendekati 500 ppm", "Waspada"),
            ("08:05", "Tangki Utama", "Level kembali normal", "Normal"),
        ]

        self.show_login()

    # ========================================================
    # LOGIN
    # ========================================================
    def show_login(self):
        self.clear_window()

        container = tk.Frame(self.root, bg=BG)
        container.pack(expand=True)

        card = tk.Frame(
            container, bg=WHITE, padx=45, pady=35,
            highlightbackground="#dddddd", highlightthickness=1
        )
        card.pack()

        tk.Label(
            card, text="DIGITAL TWIN TANGKI AIR",
            font=("Segoe UI", 22, "bold"), bg=WHITE, fg=DARK
        ).pack(pady=(0, 8))

        tk.Label(
            card, text="Monitoring Ketinggian & Kondisi Air",
            font=("Segoe UI", 10), bg=WHITE, fg=GRAY
        ).pack(pady=(0, 25))

        tk.Label(card, text="Username", anchor="w",
                 font=("Segoe UI", 10, "bold"), bg=WHITE).pack(fill="x")
        username = tk.Entry(card, width=38, font=("Segoe UI", 11))
        username.pack(ipady=8, pady=(5, 15))

        tk.Label(card, text="Password", anchor="w",
                 font=("Segoe UI", 10, "bold"), bg=WHITE).pack(fill="x")
        password = tk.Entry(card, width=38, show="*", font=("Segoe UI", 11))
        password.pack(ipady=8, pady=(5, 20))

        def login():
            if username.get() and password.get():
                self.show_dashboard()
            else:
                messagebox.showwarning(
                    "Login", "Username dan password harus diisi."
                )

        tk.Button(
            card, text="LOGIN", command=login,
            bg=BLUE, fg=WHITE, activebackground="#0b5ed7",
            activeforeground=WHITE, relief="flat",
            font=("Segoe UI", 11, "bold"), cursor="hand2"
        ).pack(fill="x", ipady=9)

        tk.Label(
            card, text="Demo: isi username dan password bebas",
            font=("Segoe UI", 9), bg=WHITE, fg=GRAY
        ).pack(pady=(15, 0))

    # ========================================================
    # DASHBOARD
    # ========================================================
    def show_dashboard(self):
        self.clear_window()

        # Header
        header = tk.Frame(self.root, bg=DARK, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="Digital Twin Tangki Air",
            font=("Segoe UI", 17, "bold"),
            bg=DARK, fg=WHITE
        ).pack(side="left", padx=25)

        nav = tk.Frame(header, bg=DARK)
        nav.pack(side="right", padx=15)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Grafik", self.show_chart),
            ("Riwayat", self.show_history),
            ("Atur", self.show_threshold),
            ("Log", self.show_notifications),
            ("Logout", self.show_login),
        ]

        for text, command in buttons:
            tk.Button(
                nav, text=text, command=command,
                bg=DARK, fg=WHITE, activebackground="#2d3b59",
                activeforeground=WHITE, relief="flat",
                font=("Segoe UI", 9, "bold"), cursor="hand2",
                padx=9
            ).pack(side="left")

        # Toolbar
        toolbar = tk.Frame(self.root, bg=WHITE, height=55)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        tk.Label(toolbar, text="Tangki:",
                 bg=WHITE, font=("Segoe UI", 10, "bold")).pack(
                     side="left", padx=(25, 5)
                 )

        tank = ttk.Combobox(
            toolbar, values=["Tangki Utama", "Tangki B", "Tangki C"],
            state="readonly", width=18
        )
        tank.set("Tangki Utama")
        tank.pack(side="left")

        tk.Label(
            toolbar, text="● Sensor Terhubung",
            bg=WHITE, fg=GREEN,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=30)

        self.update_label = tk.Label(
            toolbar, text="Update: --:--:--",
            bg=WHITE, fg=GRAY, font=("Segoe UI", 10)
        )
        self.update_label.pack(side="right", padx=25)

        # Konten
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=25, pady=20)

        # Kolom kiri: visual tangki
        tank_card = tk.Frame(content, bg=WHITE, padx=25, pady=20)
        tank_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 15))

        tk.Label(
            tank_card, text="VISUAL TANGKI",
            font=("Segoe UI", 12, "bold"), bg=WHITE, fg=DARK
        ).pack()

        self.canvas = tk.Canvas(
            tank_card, width=220, height=320,
            bg=WHITE, highlightthickness=0
        )
        self.canvas.pack(pady=10)

        self.draw_tank()

        self.level_label = tk.Label(
            tank_card, text="Level 75%",
            font=("Segoe UI", 14, "bold"),
            bg=WHITE, fg=BLUE
        )
        self.level_label.pack()

        # Parameter cards
        cards_frame = tk.Frame(content, bg=BG)
        cards_frame.grid(row=0, column=1, sticky="nsew")

        self.parameter_card(cards_frame, "KETINGGIAN",
                            f"{self.level} cm", "75%", GREEN, 0, 0)
        self.parameter_card(cards_frame, "SUHU",
                            f"{self.temperature} °C", "NORMAL", GREEN, 0, 1)
        self.parameter_card(cards_frame, "KEKERUHAN",
                            f"{self.turbidity} NTU", "NORMAL", GREEN, 0, 2)
        self.parameter_card(cards_frame, "TDS",
                            f"{self.tds} ppm", "NORMAL", GREEN, 1, 0)
        self.parameter_card(cards_frame, "STATUS UMUM",
                            "NORMAL", "Semua parameter aman", GREEN, 1, 1)

        # Notifikasi
        notif = tk.Frame(content, bg=WHITE, padx=20, pady=15)
        notif.grid(row=1, column=1, sticky="nsew", pady=(15, 0))

        tk.Label(
            notif, text="Notifikasi Terbaru",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE, fg=DARK
        ).pack(anchor="w", pady=(0, 10))

        for time, tank_name, msg, status in self.notifications:
            row = tk.Frame(notif, bg=WHITE)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=time, width=9, anchor="w",
                     bg=WHITE, fg=GRAY).pack(side="left")
            tk.Label(row, text=msg, anchor="w",
                     bg=WHITE, fg=TEXT).pack(side="left", fill="x", expand=True)
            tk.Label(row, text=status, width=12,
                     bg=WHITE, fg=self.status_color(status),
                     font=("Segoe UI", 9, "bold")).pack(side="right")

        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=2)
        content.rowconfigure(1, weight=1)

        self.update_dashboard()

    def parameter_card(self, parent, title, value, status, color, row, col):
        card = tk.Frame(parent, bg=WHITE, padx=18, pady=15,
                        highlightbackground="#dddddd", highlightthickness=1)
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=GRAY).pack(anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 18, "bold"),
                 bg=WHITE, fg=DARK).pack(anchor="w", pady=4)
        tk.Label(card, text=f"[ {status} ]", font=("Segoe UI", 9, "bold"),
                 bg=WHITE, fg=color).pack(anchor="w")

        parent.columnconfigure(col, weight=1)

    def draw_tank(self):
        self.canvas.delete("all")

        # Tangki
        x1, y1, x2, y2 = 60, 25, 160, 285
        self.canvas.create_rectangle(
            x1, y1, x2, y2, outline=DARK, width=4
        )

        # Level air
        max_height = y2 - y1
        percent = self.level / 160
        water_top = y2 - (max_height * percent)

        self.canvas.create_rectangle(
            x1 + 4, water_top, x2 - 4, y2 - 4,
            fill=BLUE, outline=BLUE
        )

        # Gelombang sederhana
        for i in range(3):
            self.canvas.create_line(
                x1 + 8, water_top + 8 + i * 5,
                x2 - 8, water_top + 8 + i * 5,
                fill=WHITE, width=2
            )

        self.canvas.create_text(
            110, 305, text=f"{self.level} cm",
            font=("Segoe UI", 11, "bold"), fill=DARK
        )

    def update_dashboard(self):
        if hasattr(self, "update_label"):
            now = datetime.now().strftime("%H:%M:%S")
            self.update_label.config(text=f"Update: {now}")

    # ========================================================
    # GRAFIK TREN
    # ========================================================
    def show_chart(self):
        self.clear_window()
        self.add_page_header("GRAFIK TREN")

        top = tk.Frame(self.root, bg=WHITE, padx=25, pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Parameter:",
                 bg=WHITE, font=("Segoe UI", 10, "bold")).pack(side="left")
        combo = ttk.Combobox(
            top, values=["Ketinggian", "Suhu", "Kekeruhan", "TDS"],
            state="readonly", width=15
        )
        combo.set("Ketinggian")
        combo.pack(side="left", padx=8)

        tk.Label(top, text="Rentang:",
                 bg=WHITE, font=("Segoe UI", 10, "bold")).pack(
                     side="left", padx=(30, 5)
                 )

        for label in ["1 Jam", "24 Jam", "7 Hari"]:
            tk.Button(top, text=label, relief="groove").pack(
                side="left", padx=2
            )

        frame = tk.Frame(self.root, bg=WHITE, padx=35, pady=25)
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        canvas = tk.Canvas(frame, bg=WHITE, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Grafik sederhana tanpa library tambahan
        width, height = 900, 400
        left, top_y = 70, 35
        right, bottom = 850, 330

        for y in [0, 40, 80, 120, 160]:
            yy = bottom - (y / 160) * (bottom - top_y)
            canvas.create_line(left, yy, right, yy, fill="#dddddd")
            canvas.create_text(left - 25, yy, text=str(y), fill=GRAY)

        points = [(0, 70), (1, 85), (2, 75), (3, 120),
                  (4, 105), (5, 135), (6, 120), (7, 148)]

        coords = []
        for i, val in points:
            x = left + i * ((right - left) / 7)
            y = bottom - (val / 160) * (bottom - top_y)
            coords.extend([x, y])

        canvas.create_line(*coords, fill=BLUE, width=3, smooth=True)

        # Garis ambang
        min_y = bottom - (40 / 160) * (bottom - top_y)
        max_y = bottom - (150 / 160) * (bottom - top_y)

        canvas.create_line(left, min_y, right, min_y,
                           fill=RED, dash=(5, 3), width=2)
        canvas.create_line(left, max_y, right, max_y,
                           fill=YELLOW, dash=(5, 3), width=2)

        canvas.create_text(750, min_y - 10,
                           text="Batas minimum (40 cm)", fill=RED)
        canvas.create_text(750, max_y - 10,
                           text="Batas maksimum (150 cm)", fill=YELLOW)

        for i, label in enumerate(
            ["06:00", "09:00", "12:00", "15:00", "18:00"]
        ):
            x = left + i * ((right - left) / 4)
            canvas.create_text(x, bottom + 25, text=label, fill=GRAY)

        tk.Label(
            frame, text="Min: 45 cm     Maks: 148 cm     Rata-rata: 102 cm",
            bg=WHITE, fg=DARK, font=("Segoe UI", 11, "bold")
        ).pack(pady=10)

    # ========================================================
    # RIWAYAT
    # ========================================================
    def show_history(self):
        self.clear_window()
        self.add_page_header("RIWAYAT DATA SENSOR")

        top = tk.Frame(self.root, bg=WHITE, padx=25, pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Tangki:", bg=WHITE).pack(side="left")
        ttk.Combobox(
            top, values=["Tangki Utama", "Tangki B", "Tangki C"],
            state="readonly", width=15
        ).pack(side="left", padx=5)

        tk.Label(top, text="Status:", bg=WHITE).pack(side="left", padx=(20, 5))
        ttk.Combobox(
            top, values=["Semua", "Normal", "Waspada", "Bahaya"],
            state="readonly", width=12
        ).pack(side="left")

        tk.Button(top, text="Ekspor CSV",
                  command=lambda: messagebox.showinfo(
                      "Ekspor", "Fitur ekspor CSV siap dikembangkan."
                  )).pack(side="right")

        frame = tk.Frame(self.root, bg=WHITE, padx=25, pady=15)
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        columns = ("Waktu", "Level (cm)", "Suhu (°C)",
                   "Keruh (NTU)", "TDS", "Status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor="center")

        for row in self.history:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)

    # ========================================================
    # AMBANG BATAS
    # ========================================================
    def show_threshold(self):
        self.clear_window()
        self.add_page_header("PENGATURAN AMBANG BATAS")

        frame = tk.Frame(self.root, bg=WHITE, padx=35, pady=25)
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        tk.Label(frame, text="Tangki:",
                 bg=WHITE, font=("Segoe UI", 10, "bold")).grid(
                     row=0, column=0, sticky="w", pady=10
                 )

        ttk.Combobox(
            frame, values=["Tangki Utama", "Tangki B", "Tangki C"],
            state="readonly", width=20
        ).grid(row=0, column=1, sticky="w")

        headers = ["Parameter", "Batas Bawah", "Batas Atas", "Satuan"]
        for c, h in enumerate(headers):
            tk.Label(frame, text=h, bg=WHITE,
                     font=("Segoe UI", 10, "bold")).grid(
                         row=2, column=c, padx=10, pady=10
                     )

        fields = [
            ("Ketinggian", self.thresholds["level_min"],
             self.thresholds["level_max"], "cm"),
            ("Suhu", self.thresholds["temp_min"],
             self.thresholds["temp_max"], "°C"),
            ("Kekeruhan", "-", self.thresholds["turbidity_max"], "NTU"),
            ("TDS", "-", self.thresholds["tds_max"], "ppm"),
        ]

        entries = []

        for r, (name, low, high, unit) in enumerate(fields, start=3):
            tk.Label(frame, text=name, bg=WHITE).grid(
                row=r, column=0, padx=10, pady=8, sticky="w"
            )

            low_entry = tk.Entry(frame, width=15)
            low_entry.insert(0, str(low))
            low_entry.grid(row=r, column=1, padx=10)

            high_entry = tk.Entry(frame, width=15)
            high_entry.insert(0, str(high))
            high_entry.grid(row=r, column=2, padx=10)

            tk.Label(frame, text=unit, bg=WHITE).grid(
                row=r, column=3
            )
            entries.append((low_entry, high_entry))

        tk.Label(
            frame, text="Kirim notifikasi via:",
            bg=WHITE, font=("Segoe UI", 10, "bold")
        ).grid(row=8, column=0, sticky="w", pady=20)

        for i, text in enumerate(["In-app", "Email", "Telegram"], start=1):
            tk.Checkbutton(frame, text=text, bg=WHITE).grid(
                row=8, column=i, sticky="w"
            )

        def save():
            messagebox.showinfo(
                "Berhasil", "Pengaturan ambang batas berhasil disimpan."
            )

        tk.Button(
            frame, text="BATAL", command=self.show_dashboard,
            relief="groove", padx=20
        ).grid(row=10, column=2, pady=25)

        tk.Button(
            frame, text="SIMPAN PENGATURAN", command=save,
            bg=BLUE, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), padx=20
        ).grid(row=10, column=3, pady=25)

    # ========================================================
    # LOG NOTIFIKASI
    # ========================================================
    def show_notifications(self):
        self.clear_window()
        self.add_page_header("LOG NOTIFIKASI")

        frame = tk.Frame(self.root, bg=WHITE, padx=25, pady=20)
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        columns = ("Waktu", "Tangki", "Pesan", "Tingkat")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        for row in self.notifications:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True)

    # ========================================================
    # HELPER
    # ========================================================
    def add_page_header(self, title):
        header = tk.Frame(self.root, bg=DARK, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(
            header, text="← Dashboard",
            command=self.show_dashboard,
            bg=DARK, fg=WHITE, relief="flat",
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        ).pack(side="left", padx=20)

        tk.Label(
            header, text=title,
            bg=DARK, fg=WHITE,
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=20)

    def status_color(self, status):
        if status.lower() == "normal":
            return GREEN
        if status.lower() == "waspada":
            return YELLOW
        if status.lower() == "bahaya":
            return RED
        return BLUE

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalTwinApp(root)
    root.mainloop()
