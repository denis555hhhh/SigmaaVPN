#!/usr/bin/env python3
"""
SigmaVPN Desktop Application - Simplified Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import webbrowser

# Colors
BG = "#080f0a"
BG_CARD = "#0f1a12"
PRIMARY = "#16a34a"
PRIMARY_D = "#15803d"
PRIMARY_L = "#4ade80"
TEXT = "#e2e8f0"
TEXT_M = "#94a3b8"
WHITE = "#ffffff"
RED = "#ef4444"

class SigmaVPN(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SigmaVPN")
        self.geometry("800x600")
        self.configure(bg=BG)
        
        # State
        self.connected = False
        self.timer_seconds = 0
        
        self.build_ui()
        self.update_timer()
    
    def build_ui(self):
        # Main frame
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main, text="🔒 SigmaVPN", 
                        font=("Arial", 24, "bold"),
                        bg=BG, fg=PRIMARY_L)
        title.pack(pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Отключено")
        status = tk.Label(main, textvariable=self.status_var,
                         font=("Arial", 14),
                         bg=BG, fg=RED)
        status.pack(pady=5)
        
        # Connect button
        self.btn_connect = tk.Button(main, text="ПОДКЛЮЧИТЬСЯ",
                                     font=("Arial", 14, "bold"),
                                     bg=PRIMARY, fg=WHITE,
                                     padx=30, pady=15,
                                     command=self.toggle_connect,
                                     relief="flat", cursor="hand2")
        self.btn_connect.pack(pady=20)
        
        # Timer
        self.timer_var = tk.StringVar(value="00:00:00")
        timer = tk.Label(main, textvariable=self.timer_var,
                        font=("Arial", 20, "bold"),
                        bg=BG, fg=PRIMARY_L)
        timer.pack(pady=10)
        
        # Info frame
        info_frame = tk.Frame(main, bg=BG_CARD, relief="flat")
        info_frame.pack(fill="x", pady=20)
        
        tk.Label(info_frame, text="IP: —", font=("Arial", 11),
                bg=BG_CARD, fg=TEXT).pack(anchor="w", padx=15, pady=5)
        tk.Label(info_frame, text="Пинг: — мс", font=("Arial", 11),
                bg=BG_CARD, fg=TEXT).pack(anchor="w", padx=15, pady=5)
        tk.Label(info_frame, text="Скорость: 0.0 МБ/с", font=("Arial", 11),
                bg=BG_CARD, fg=TEXT).pack(anchor="w", padx=15, pady=5)
        
        # Support button
        support_btn = tk.Button(main, text="💬 Поддержка Telegram",
                               font=("Arial", 10),
                               bg="#1d6fa4", fg=WHITE,
                               padx=20, pady=10,
                               command=lambda: webbrowser.open("https://t.me/slogg12"),
                               relief="flat", cursor="hand2")
        support_btn.pack(pady=10)
        
        # Website button
        website_btn = tk.Button(main, text="🌐 Открыть сайт",
                               font=("Arial", 10),
                               bg=BG_CARD, fg=TEXT_M,
                               padx=20, pady=10,
                               command=lambda: webbrowser.open("https://sigmavpn.com"),
                               relief="flat", cursor="hand2")
        website_btn.pack(pady=5)
    
    def toggle_connect(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        self.connected = True
        self.timer_seconds = 0
        self.status_var.set("Подключено ✓")
        self.btn_connect.configure(text="ОТКЛЮЧИТЬСЯ", bg=RED)
        self.status_var.set("Подключено ✓")
    
    def disconnect(self):
        self.connected = False
        self.timer_seconds = 0
        self.status_var.set("Отключено")
        self.btn_connect.configure(text="ПОДКЛЮЧИТЬСЯ", bg=PRIMARY)
        self.timer_var.set("00:00:00")
    
    def update_timer(self):
        if self.connected:
            self.timer_seconds += 1
            h = self.timer_seconds // 3600
            m = (self.timer_seconds % 3600) // 60
            s = self.timer_seconds % 60
            self.timer_var.set(f"{h:02d}:{m:02d}:{s:02d}")
        
        self.after(1000, self.update_timer)

if __name__ == "__main__":
    app = SigmaVPN()
    app.mainloop()
