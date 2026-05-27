import tkinter as tk
from tkinter import ttk, messagebox
import threading, time, random, webbrowser, math
import sys
import traceback

# ── PALETTE ────────────────────────────────────────────────────────────────
BG        = "#080f0a"
BG_CARD   = "#0f1a12"
BG_CARD2  = "#162019"
PRIMARY   = "#16a34a"
PRIMARY_D = "#15803d"
PRIMARY_L = "#4ade80"
ACCENT    = "#22d3ee"
TEXT      = "#e2e8f0"
TEXT_M    = "#94a3b8"
BORDER    = "#1e2d22"
RED       = "#ef4444"
RED_D     = "#dc2626"
YELLOW    = "#f59e0b"
WHITE     = "#ffffff"

SERVERS = [
    {"name":"🇩🇪 Германия",       "city":"Франкфурт",  "ping":18,  "load":34},
    {"name":"🇺🇸 США",            "city":"Нью-Йорк",   "ping":92,  "load":61},
    {"name":"🇳🇱 Нидерланды",     "city":"Амстердам",  "ping":22,  "load":28},
    {"name":"🇬🇧 Великобритания", "city":"Лондон",     "ping":35,  "load":45},
    {"name":"🇯🇵 Япония",         "city":"Токио",      "ping":148, "load":52},
    {"name":"🇸🇬 Сингапур",       "city":"Сингапур",   "ping":130, "load":39},
    {"name":"🇫🇷 Франция",        "city":"Париж",      "ping":28,  "load":22},
    {"name":"🇨🇦 Канада",         "city":"Торонто",    "ping":105, "load":47},
    {"name":"🇦🇺 Австралия",      "city":"Сидней",     "ping":210, "load":31},
    {"name":"🇨🇭 Швейцария",      "city":"Цюрих",      "ping":25,  "load":19},
]

# ── CUSTOM ROUNDED BUTTON ──────────────────────────────────────────────────
class RoundBtn(tk.Canvas):
    """Canvas-based button with rounded corners and hover animation."""
    def __init__(self, parent, text, command=None,
                 bg=PRIMARY, fg=WHITE, hover=PRIMARY_D,
                 font_size=11, bold=True, radius=10,
                 padx=20, pady=10, width=0, **kw):
        self._text   = text
        self._bg     = bg
        self._fg     = fg
        self._hover  = hover
        self._cmd    = command
        self._radius = radius
        self._font   = ("Segoe UI", font_size, "bold" if bold else "normal")
        self._padx   = padx
        self._pady   = pady
        self._cur_bg = bg
        self._disabled = False

        # Measure text size
        tmp = tk.Label(parent, text=text, font=self._font)
        tw = tmp.winfo_reqwidth()
        th = tmp.winfo_reqheight()
        tmp.destroy()
        w = max(width, tw + padx * 2)
        h = th + pady * 2

        super().__init__(parent, width=w, height=h,
                         bg=parent["bg"], bd=0, highlightthickness=0, **kw)
        self._w = w
        self._h = h
        self._draw(bg)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _draw(self, color):
        self.delete("all")
        r = self._radius
        w, h = self._w, self._h
        # Rounded rect via polygon
        self.create_polygon(
            r, 0,  w-r, 0,
            w, 0,  w, r,
            w, h-r, w, h,
            w-r, h, r, h,
            0, h,  0, h-r,
            0, r,  0, 0,
            r, 0,
            smooth=True, fill=color, outline=color)
        self.create_text(w//2, h//2, text=self._text,
                         font=self._font, fill=self._fg)

    def _on_enter(self, e):
        if not self._disabled:
            self._draw(self._hover)

    def _on_leave(self, e):
        if not self._disabled:
            self._draw(self._bg)

    def _on_click(self, e):
        if not self._disabled:
            # Darken slightly
            self._draw(self._hover)

    def _on_release(self, e):
        if not self._disabled:
            self._draw(self._bg)
            if self._cmd:
                self._cmd()

    def configure_btn(self, text=None, bg=None, hover=None, fg=None, disabled=False):
        if text  is not None: self._text  = text
        if bg    is not None: self._bg    = bg
        if hover is not None: self._hover = hover
        if fg    is not None: self._fg    = fg
        self._disabled = disabled
        self._draw(self._bg)

# ── MAIN APP ───────────────────────────────────────────────────────────────
class SigmaVPN(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SigmaVPN")
        self.geometry("960x640")
        self.minsize(880, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        # State
        self.connected     = False
        self.connecting    = False
        self.selected_srv  = 0
        self.session_start = None
        self.dl_speed  = tk.StringVar(value="0.0")
        self.ul_speed  = tk.StringVar(value="0.0")
        self.timer_var = tk.StringVar(value="00:00:00")
        self.status_var= tk.StringVar(value="Отключено")
        self.ip_var    = tk.StringVar(value="—")
        self.proto_var = tk.StringVar(value="WireGuard")

        self._build_ui()
        self._tick()

    # ── HELPERS ─────────────────────────────────────────────────────────────
    def _card(self, parent, padx=0, pady=0):
        f = tk.Frame(parent, bg=BG_CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        return f

    def _label(self, parent, text, size=11, color=TEXT, bold=False, anchor="w"):
        return tk.Label(parent, text=text,
                        font=("Segoe UI", size, "bold" if bold else "normal"),
                        bg=parent["bg"], fg=color, anchor=anchor)

    def _sep(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

    # ── SIDEBAR ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.sidebar = tk.Frame(self, bg=BG_CARD, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self._build_home()

    def _build_sidebar(self):
        # Logo area
        logo = tk.Frame(self.sidebar, bg=BG_CARD, pady=22)
        logo.pack(fill="x")
        tk.Label(logo, text="🔒", font=("Segoe UI", 26),
                 bg=BG_CARD, fg=PRIMARY_L).pack()
        tk.Label(logo, text="SigmaVPN", font=("Segoe UI", 16, "bold"),
                 bg=BG_CARD, fg=WHITE).pack()
        tk.Label(logo, text="Защита · Свобода · Анонимность",
                 font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_M).pack()

        self._sep(self.sidebar)

        # Nav
        self.nav_btns = {}
        items = [("🏠   Главная","home"),("🌍   Серверы","servers"),
                 ("📊   Статистика","stats"),("⚙️   Настройки","settings")]
        nav = tk.Frame(self.sidebar, bg=BG_CARD, pady=10)
        nav.pack(fill="x")
        for label, key in items:
            btn = tk.Button(nav, text=label, font=("Segoe UI", 11),
                            bg=BG_CARD, fg=TEXT_M, bd=0, cursor="hand2",
                            activebackground=BG_CARD2, activeforeground=WHITE,
                            anchor="w", padx=22, pady=11, relief="flat",
                            command=lambda k=key: self._nav(k))
            btn.pack(fill="x")
            self.nav_btns[key] = btn
        self._highlight_nav("home")

        self._sep(self.sidebar)

        # Status badge
        self.badge_frame = tk.Frame(self.sidebar, bg=BG_CARD, pady=14)
        self.badge_frame.pack(fill="x")
        self.badge_dot = tk.Label(self.badge_frame, text="●",
                                  font=("Segoe UI", 14), bg=BG_CARD, fg=RED)
        self.badge_dot.pack(side="left", padx=(18,6))
        self.badge_lbl = tk.Label(self.badge_frame, textvariable=self.status_var,
                                  font=("Segoe UI", 11, "bold"),
                                  bg=BG_CARD, fg=TEXT)
        self.badge_lbl.pack(side="left")

        self._sep(self.sidebar)

        # Bottom buttons
        bot = tk.Frame(self.sidebar, bg=BG_CARD, pady=16)
        bot.pack(side="bottom", fill="x", padx=14)

        RoundBtn(bot, "💬  Поддержка Telegram",
                 bg="#1d6fa4", hover="#1a5f8c", fg=WHITE,
                 font_size=10, radius=8, padx=14, pady=9,
                 command=lambda: webbrowser.open("https://t.me/slogg12")
                 ).pack(fill="x", pady=3)

        RoundBtn(bot, "🌐  Открыть сайт",
                 bg=BG_CARD2, hover=BORDER, fg=TEXT_M,
                 font_size=10, radius=8, padx=14, pady=9,
                 command=lambda: webbrowser.open("https://sigmavpn.com")
                 ).pack(fill="x", pady=3)

    def _highlight_nav(self, key):
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.configure(bg=PRIMARY, fg=WHITE,
                              activebackground=PRIMARY_D)
            else:
                btn.configure(bg=BG_CARD, fg=TEXT_M,
                              activebackground=BG_CARD2)

    def _nav(self, key):
        self._highlight_nav(key)
        for w in self.main.winfo_children():
            w.destroy()
        {"home":self._build_home,"servers":self._build_servers,
         "stats":self._build_stats,"settings":self._build_settings}[key]()

    # ── HOME ────────────────────────────────────────────────────────────────
    def _build_home(self):
        pad = tk.Frame(self.main, bg=BG, padx=30, pady=22)
        pad.pack(fill="both", expand=True)

        self._label(pad,"Панель управления",18,TEXT,True).pack(anchor="w")
        self._label(pad,"Управляйте вашим VPN-соединением",10,TEXT_M).pack(anchor="w",pady=(2,18))

        # ── Top row ──
        top = tk.Frame(pad, bg=BG)
        top.pack(fill="x", pady=(0,14))
        top.columnconfigure(0, weight=3)
        top.columnconfigure(1, weight=2)

        # Connect card
        cc = self._card(top)
        cc.grid(row=0, column=0, sticky="nsew", padx=(0,12))
        self._connect_card(cc)

        # Info card
        ic = self._card(top)
        ic.grid(row=0, column=1, sticky="nsew")
        self._info_card(ic)

        # ── Bottom row: speed cards ──
        bot = tk.Frame(pad, bg=BG)
        bot.pack(fill="x")
        for i in range(3):
            bot.columnconfigure(i, weight=1)
        self._metric_card(bot,"⬇  Загрузка",  self.dl_speed,"МБ/с",PRIMARY_L,0)
        self._metric_card(bot,"⬆  Отдача",    self.ul_speed,"МБ/с",ACCENT,   1)
        self._ping_metric(bot, 2)

    def _connect_card(self, parent):
        f = tk.Frame(parent, bg=BG_CARD, padx=24, pady=20)
        f.pack(fill="both", expand=True)

        # Server row
        self._label(f,"Выбранный сервер",9,TEXT_M).pack(anchor="w")
        srv_row = tk.Frame(f, bg=BG_CARD)
        srv_row.pack(fill="x", pady=(4,16))

        self.srv_lbl = self._label(srv_row,
            SERVERS[self.selected_srv]["name"]+"  —  "+SERVERS[self.selected_srv]["city"],
            12, TEXT, True)
        self.srv_lbl.pack(side="left")

        RoundBtn(srv_row,"Сменить →",
                 bg=BG_CARD2, hover=BORDER, fg=PRIMARY_L,
                 font_size=9, radius=6, padx=12, pady=6,
                 command=lambda: self._nav("servers")).pack(side="right")

        # Big connect button
        self.conn_btn = RoundBtn(f,
            "⏻   ПОДКЛЮЧИТЬСЯ",
            bg=PRIMARY, hover=PRIMARY_D, fg=WHITE,
            font_size=14, radius=12, padx=0, pady=16,
            command=self._toggle_connect)
        self.conn_btn.pack(fill="x", pady=(0,16))

        # Status row
        sr = tk.Frame(f, bg=BG_CARD)
        sr.pack(fill="x")
        self._label(sr,"Статус:",10,TEXT_M).pack(side="left")
        self.dot_lbl = tk.Label(sr, text="●", font=("Segoe UI",14),
                                bg=BG_CARD, fg=RED)
        self.dot_lbl.pack(side="left", padx=(8,4))
        tk.Label(sr, textvariable=self.status_var,
                 font=("Segoe UI",11,"bold"), bg=BG_CARD, fg=TEXT).pack(side="left")

        # Timer
        tk.Label(f, textvariable=self.timer_var,
                 font=("Segoe UI",26,"bold"), bg=BG_CARD, fg=PRIMARY_L
                 ).pack(pady=(14,0))
        self._label(f,"Время сессии",9,TEXT_M,"normal","center").pack()

    def _info_card(self, parent):
        f = tk.Frame(parent, bg=BG_CARD, padx=20, pady=20)
        f.pack(fill="both", expand=True)
        self._label(f,"Информация",12,TEXT,True).pack(anchor="w",pady=(0,10))

        rows = [("IP-адрес",self.ip_var,TEXT),
                ("Протокол",self.proto_var,PRIMARY_L)]
        for lbl, var, vc in rows:
            row = tk.Frame(f, bg=BG_CARD2,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=3)
            self._label(row,lbl,10,TEXT_M).pack(side="left",padx=12,pady=9)
            tk.Label(row, textvariable=var, font=("Segoe UI",10,"bold"),
                     bg=BG_CARD2, fg=vc, padx=12).pack(side="right")

        for lbl, val, vc in [("Пинг","—",YELLOW),("Шифрование","AES-256",PRIMARY_L)]:
            row = tk.Frame(f, bg=BG_CARD2,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=3)
            self._label(row,lbl,10,TEXT_M).pack(side="left",padx=12,pady=9)
            lbl_w = tk.Label(row, text=val, font=("Segoe UI",10,"bold"),
                             bg=BG_CARD2, fg=vc, padx=12)
            lbl_w.pack(side="right")
            if lbl == "Пинг":
                self.ping_lbl = lbl_w

    def _metric_card(self, parent, title, var, unit, color, col):
        card = self._card(parent)
        card.grid(row=0, column=col, sticky="ew",
                  padx=(0,12) if col<2 else 0)
        f = tk.Frame(card, bg=BG_CARD, padx=20, pady=16)
        f.pack(fill="both")
        self._label(f,title,10,TEXT_M).pack(anchor="w")
        row = tk.Frame(f, bg=BG_CARD)
        row.pack(anchor="w", pady=(4,0))
        tk.Label(row, textvariable=var, font=("Segoe UI",22,"bold"),
                 bg=BG_CARD, fg=color).pack(side="left")
        self._label(row," "+unit,11,TEXT_M).pack(side="left",pady=(5,0))

    def _ping_metric(self, parent, col):
        card = self._card(parent)
        card.grid(row=0, column=col, sticky="ew")
        f = tk.Frame(card, bg=BG_CARD, padx=20, pady=16)
        f.pack(fill="both")
        self._label(f,"📡  Пинг",10,TEXT_M).pack(anchor="w")
        self.ping_big = tk.Label(f, text="—",
                                 font=("Segoe UI",22,"bold"),
                                 bg=BG_CARD, fg=YELLOW)
        self.ping_big.pack(anchor="w", pady=(4,0))
        self._label(f,"мс",10,TEXT_M).pack(anchor="w")

    # ── SERVERS ─────────────────────────────────────────────────────────────
    def _build_servers(self):
        pad = tk.Frame(self.main, bg=BG, padx=30, pady=22)
        pad.pack(fill="both", expand=True)
        self._label(pad,"Серверы",18,TEXT,True).pack(anchor="w")
        self._label(pad,f"Доступно {len(SERVERS)} серверов в 10 странах",
                    10,TEXT_M).pack(anchor="w",pady=(2,14))

        # Header
        hdr = tk.Frame(pad, bg=BG_CARD2)
        hdr.pack(fill="x")
        for txt, w in [("Страна",22),("Город",14),("Пинг",8),("Нагрузка",14),("",12)]:
            tk.Label(hdr, text=txt, font=("Segoe UI",10,"bold"),
                     bg=BG_CARD2, fg=TEXT_M, width=w,
                     padx=10, pady=8, anchor="w").pack(side="left")

        # Scrollable list
        canvas = tk.Canvas(pad, bg=BG, bd=0, highlightthickness=0)
        scroll = tk.Scrollbar(pad, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=BG)
        canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for i, srv in enumerate(SERVERS):
            bg = BG_CARD if i%2==0 else BG_CARD2
            row = tk.Frame(inner, bg=bg,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=1)

            pc = PRIMARY_L if srv["ping"]<50 else (YELLOW if srv["ping"]<120 else RED)
            lc = PRIMARY_L if srv["load"]<40 else (YELLOW if srv["load"]<70 else RED)

            tk.Label(row, text=srv["name"], font=("Segoe UI",11,"bold"),
                     bg=bg, fg=TEXT, width=22, padx=10, pady=10, anchor="w").pack(side="left")
            tk.Label(row, text=srv["city"], font=("Segoe UI",10),
                     bg=bg, fg=TEXT_M, width=14, padx=10, anchor="w").pack(side="left")
            tk.Label(row, text=f"{srv['ping']} мс", font=("Segoe UI",10,"bold"),
                     bg=bg, fg=pc, width=8, padx=10, anchor="w").pack(side="left")

            # Load bar
            lf = tk.Frame(row, bg=bg, padx=10, width=120)
            lf.pack(side="left")
            lf.pack_propagate(False)
            bar = tk.Frame(lf, bg=BORDER, width=90, height=6)
            bar.pack(pady=2)
            bar.pack_propagate(False)
            tk.Frame(bar, bg=lc, width=max(4,int(90*srv["load"]/100)),
                     height=6).place(x=0,y=0)
            tk.Label(lf, text=f"{srv['load']}%", font=("Segoe UI",9),
                     bg=bg, fg=TEXT_M).pack()

            is_sel = (i == self.selected_srv)
            RoundBtn(row,
                "✓ Выбран" if is_sel else "Выбрать",
                bg=PRIMARY if is_sel else BG_CARD2,
                hover=PRIMARY_D if is_sel else BORDER,
                fg=WHITE if is_sel else TEXT_M,
                font_size=9, radius=6, padx=14, pady=7,
                command=lambda idx=i: self._select_server(idx)
            ).pack(side="right", padx=12, pady=8)

    def _select_server(self, idx):
        self.selected_srv = idx
        if hasattr(self,"srv_lbl"):
            self.srv_lbl.configure(
                text=SERVERS[idx]["name"]+"  —  "+SERVERS[idx]["city"])
        self._nav("servers")

    # ── STATS ────────────────────────────────────────────────────────────────
    def _build_stats(self):
        pad = tk.Frame(self.main, bg=BG, padx=30, pady=22)
        pad.pack(fill="both", expand=True)
        self._label(pad,"Статистика",18,TEXT,True).pack(anchor="w")
        self._label(pad,"Данные о вашем использовании SigmaVPN",
                    10,TEXT_M).pack(anchor="w",pady=(2,18))

        grid = tk.Frame(pad, bg=BG)
        grid.pack(fill="x")
        for i in range(3): grid.columnconfigure(i, weight=1)

        for i,(lbl,val,col) in enumerate([
            ("📅  Дней активно","127",PRIMARY_L),
            ("🔒  Сессий всего","843",ACCENT),
            ("🌍  Стран посещено","12",YELLOW),
            ("⬇  Загружено","1.24 ТБ",PRIMARY_L),
            ("⬆  Отдано","312 ГБ",ACCENT),
            ("⏱  Часов онлайн","2 841",YELLOW),
        ]):
            c = self._card(grid)
            c.grid(row=i//3, column=i%3, sticky="ew",
                   padx=(0,12) if i%3<2 else 0, pady=(0,12))
            f = tk.Frame(c, bg=BG_CARD, padx=20, pady=18)
            f.pack(fill="both")
            self._label(f,lbl,10,TEXT_M).pack(anchor="w")
            tk.Label(f, text=val, font=("Segoe UI",24,"bold"),
                     bg=BG_CARD, fg=col).pack(anchor="w",pady=(6,0))

        self._label(pad,"Последние сессии",13,TEXT,True).pack(anchor="w",pady=(14,8))
        hdr = tk.Frame(pad, bg=BG_CARD2)
        hdr.pack(fill="x")
        for t in ["Сервер","Дата","Длительность","Трафик"]:
            tk.Label(hdr, text=t, font=("Segoe UI",10,"bold"),
                     bg=BG_CARD2, fg=TEXT_M, width=16,
                     padx=14, pady=8, anchor="w").pack(side="left")

        for i,(s,d,dur,tr) in enumerate([
            ("Германия 🇩🇪","Сегодня, 14:32","2ч 14м","1.2 ГБ"),
            ("Нидерланды 🇳🇱","Вчера, 20:11","45м","340 МБ"),
            ("Швейцария 🇨🇭","Вчера, 11:05","3ч 02м","2.1 ГБ"),
            ("США 🇺🇸","2 дня назад","1ч 30м","890 МБ"),
        ]):
            bg = BG_CARD if i%2==0 else BG_CARD2
            row = tk.Frame(pad, bg=bg,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", pady=1)
            for t in [s,d,dur,tr]:
                tk.Label(row, text=t, font=("Segoe UI",10),
                         bg=bg, fg=TEXT, width=16,
                         padx=14, pady=10, anchor="w").pack(side="left")

    # ── SETTINGS ─────────────────────────────────────────────────────────────
    def _build_settings(self):
        pad = tk.Frame(self.main, bg=BG, padx=30, pady=22)
        pad.pack(fill="both", expand=True)
        self._label(pad,"Настройки",18,TEXT,True).pack(anchor="w")
        self._label(pad,"Конфигурация SigmaVPN",10,TEXT_M).pack(anchor="w",pady=(2,18))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=BG_CARD2,
                        background=BG_CARD2, foreground=TEXT,
                        selectbackground=PRIMARY, selectforeground=WHITE,
                        bordercolor=BORDER, arrowcolor=TEXT_M)

        sections = [
            ("Протокол",[("Протокол подключения","protocol",["WireGuard","OpenVPN","IKEv2"])]),
            ("Безопасность",[
                ("Kill Switch","ks",["Включён","Выключен"]),
                ("DNS Leak Protection","dns",["Включена","Выключена"]),
                ("Обфускация трафика","obfs",["Включена","Выключена"]),
            ]),
            ("Автозапуск",[
                ("Запуск при старте Windows","auto",["Да","Нет"]),
                ("Автоподключение","autoconn",["Да","Нет"]),
            ]),
        ]
        defaults = {"protocol":"WireGuard","ks":"Включён","dns":"Включена",
                    "obfs":"Выключена","auto":"Нет","autoconn":"Нет"}

        for sec, opts in sections:
            self._label(pad,sec,12,PRIMARY_L,True).pack(anchor="w",pady=(8,4))
            card = self._card(pad)
            card.pack(fill="x", pady=(0,10))
            for lbl, key, choices in opts:
                row = tk.Frame(card, bg=BG_CARD)
                row.pack(fill="x", padx=20, pady=10)
                self._label(row,lbl,11,TEXT).pack(side="left")
                var = tk.StringVar(value=defaults.get(key,choices[0]))
                ttk.Combobox(row, textvariable=var, values=choices,
                             state="readonly", width=16,
                             font=("Segoe UI",10)).pack(side="right")

        RoundBtn(pad,"💾   Сохранить настройки",
                 bg=PRIMARY, hover=PRIMARY_D, fg=WHITE,
                 font_size=12, radius=10, padx=28, pady=13,
                 command=lambda: messagebox.showinfo("SigmaVPN","✅ Настройки сохранены!")
                 ).pack(anchor="w", pady=(10,0))

    # ── CONNECTION ──────────────────────────────────────────────────────────
    def _toggle_connect(self):
        if self.connecting:
            return
        if self.connected:
            self._disconnect()
        else:
            self._connect()

    def _connect(self):
        self.connecting = True
        self.conn_btn.configure_btn(disabled=True)
        threading.Thread(target=self._connect_thread, daemon=True).start()

    def _connect_thread(self):
        time.sleep(1.5)  # Simulate connection
        self.connected = True
        self.connecting = False
        self.session_start = time.time()
        self.status_var.set("Подключено")
        self.ip_var.set(f"192.168.{random.randint(1,255)}.{random.randint(1,255)}")
        self.conn_btn.configure_btn(text="⏻   ОТКЛЮЧИТЬСЯ", disabled=False)
        self.badge_dot.configure(fg=PRIMARY_L)
        self.dot_lbl.configure(fg=PRIMARY_L)

    def _disconnect(self):
        self.connecting = True
        self.conn_btn.configure_btn(disabled=True)
        threading.Thread(target=self._disconnect_thread, daemon=True).start()

    def _disconnect_thread(self):
        time.sleep(1)
        self.connected = False
        self.connecting = False
        self.session_start = None
        self.status_var.set("Отключено")
        self.ip_var.set("—")
        self.timer_var.set("00:00:00")
        self.dl_speed.set("0.0")
        self.ul_speed.set("0.0")
        self.ping_big.configure(text="—")
        self.ping_lbl.configure(text="—")
        self.conn_btn.configure_btn(text="⏻   ПОДКЛЮЧИТЬСЯ", disabled=False)
        self.badge_dot.configure(fg=RED)
        self.dot_lbl.configure(fg=RED)

    def _tick(self):
        if self.connected and self.session_start:
            elapsed = int(time.time() - self.session_start)
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            self.timer_var.set(f"{h:02d}:{m:02d}:{s:02d}")

            # Simulate speeds
            self.dl_speed.set(f"{random.uniform(5, 95):.1f}")
            self.ul_speed.set(f"{random.uniform(2, 45):.1f}")

            # Update ping
            srv = SERVERS[self.selected_srv]
            ping = srv["ping"] + random.randint(-5, 5)
            self.ping_big.configure(text=str(ping))
            self.ping_lbl.configure(text=str(ping))

        self.after(1000, self._tick)

if __name__ == "__main__":
    try:
        app = SigmaVPN()
        app.mainloop()
    except Exception as e:
        error_msg = f"Ошибка запуска приложения:\n\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("SigmaVPN - Ошибка", error_msg)
        except:
            pass
        sys.exit(1)
