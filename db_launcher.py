#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
from datetime import datetime
import hashlib

class DatabaseLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 SigmaVPN - Админ Панель БД")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0f172a")
        
        self.db_path = 'sigmavpn.db'
        self.current_user = None
        self.is_admin = False
        
        # Стили
        self.setup_styles()
        
        # Главное окно
        self.show_login_screen()
    
    def setup_styles(self):
        """Настройка стилей"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цвета
        bg_color = "#0f172a"
        fg_color = "#ffffff"
        accent_color = "#16a34a"
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=accent_color, foreground=fg_color)
        style.configure('Accent.TButton', background=accent_color, foreground=fg_color)
        style.configure('Danger.TButton', background="#dc2626", foreground=fg_color)
        style.configure('TEntry', fieldbackground="#1e293b", foreground=fg_color)
        style.configure('TCombobox', fieldbackground="#1e293b", foreground=fg_color)
        
        self.root.configure(bg=bg_color)
    
    def clear_window(self):
        """Очистить окно"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Экран входа"""
        self.clear_window()
        
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Заголовок
        title = tk.Label(frame, text="🔒 SigmaVPN Admin Panel", 
                        font=("Arial", 24, "bold"), fg="#16a34a", bg="#0f172a")
        title.pack(pady=20)
        
        # Форма входа
        login_frame = ttk.Frame(frame)
        login_frame.pack(pady=20)
        
        ttk.Label(login_frame, text="Пароль администратора:").pack(pady=10)
        password_entry = ttk.Entry(login_frame, show="*", width=30)
        password_entry.pack(pady=5)
        
        def login():
            password = password_entry.get()
            admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
            if hashlib.sha256(password.encode()).hexdigest() == admin_hash:
                self.is_admin = True
                self.show_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный пароль!")
        
        ttk.Button(login_frame, text="Вход", command=login).pack(pady=10)
        
        # Информация
        info = tk.Label(frame, text="Пароль по умолчанию: admin123", 
                       font=("Arial", 10), fg="#94a3b8", bg="#0f172a")
        info.pack(pady=20)
    
    def show_main_menu(self):
        """Главное меню"""
        self.clear_window()
        
        # Заголовок
        header = tk.Label(self.root, text="🔒 SigmaVPN - Админ Панель", 
                         font=("Arial", 20, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        # Меню кнопок
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        buttons = [
            ("👥 Управление пользователями", self.show_users),
            ("📊 Управление подписками", self.show_subscriptions),
            ("📝 Логи системы", self.show_logs),
            ("📈 Статистика", self.show_stats),
            ("⚙️ Настройки БД", self.show_settings),
            ("🚪 Выход", self.show_login_screen),
        ]
        
        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, command=command,
                          font=("Arial", 12), bg="#16a34a", fg="white",
                          padx=20, pady=15, relief="flat", cursor="hand2")
            btn.pack(fill='x', pady=10)
    
    def show_users(self):
        """Управление пользователями"""
        self.clear_window()
        
        # Заголовок
        header = tk.Label(self.root, text="👥 Управление пользователями", 
                         font=("Arial", 18, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        # Кнопки действий
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="➕ Добавить пользователя", 
                  command=self.add_user).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Обновить", 
                  command=self.show_users).pack(side='left', padx=5)
        ttk.Button(action_frame, text="⬅️ Назад", 
                  command=self.show_main_menu).pack(side='left', padx=5)
        
        # Таблица пользователей
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            conn.close()
            
            # Фрейм для таблицы
            table_frame = ttk.Frame(self.root)
            table_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Скролл
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side='right', fill='y')
            
            text = scrolledtext.ScrolledText(table_frame, height=20, width=100,
                                            yscrollcommand=scrollbar.set)
            text.pack(fill='both', expand=True)
            scrollbar.config(command=text.yview)
            
            # Заголовок таблицы
            header_text = f"{'ID':<5} {'Email':<25} {'Username':<20} {'Создан':<20} {'Действия':<20}\n"
            header_text += "=" * 100 + "\n"
            text.insert('end', header_text)
            
            # Данные
            for user in users:
                user_text = f"{user['id']:<5} {user['email']:<25} {user['username']:<20} {user['created_at']:<20}"
                text.insert('end', user_text + "\n")
                
                # Кнопки действий
                btn_frame = tk.Frame(text, bg="#1e293b")
                text.window_create('end', window=btn_frame)
                
                def delete_user(uid=user['id']):
                    if messagebox.askyesno("Подтверждение", f"Удалить пользователя {uid}?"):
                        self.delete_user_db(uid)
                        self.show_users()
                
                tk.Button(btn_frame, text="🗑️ Удалить", command=delete_user,
                         bg="#dc2626", fg="white", relief="flat").pack(side='left', padx=2)
                text.insert('end', "\n")
            
            text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки пользователей: {str(e)}")
    
    def add_user(self):
        """Добавить пользователя"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пользователя")
        dialog.geometry("400x300")
        dialog.configure(bg="#0f172a")
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=40)
        email_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(dialog, width=40)
        username_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Пароль:").pack(pady=5)
        password_entry = ttk.Entry(dialog, show="*", width=40)
        password_entry.pack(pady=5)
        
        def save():
            email = email_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            
            if not all([email, username, password]):
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("""
                    INSERT INTO users (email, username, password)
                    VALUES (?, ?, ?)
                """, (email, username, password_hash))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Успех", "Пользователь добавлен!")
                dialog.destroy()
                self.show_users()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {str(e)}")
        
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)
    
    def delete_user_db(self, user_id):
        """Удалить пользователя из БД"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Пользователь удален!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления: {str(e)}")
    
    def show_subscriptions(self):
        """Управление подписками"""
        self.clear_window()
        
        header = tk.Label(self.root, text="📊 Управление подписками", 
                         font=("Arial", 18, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="➕ Добавить подписку", 
                  command=self.add_subscription).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Обновить", 
                  command=self.show_subscriptions).pack(side='left', padx=5)
        ttk.Button(action_frame, text="⬅️ Назад", 
                  command=self.show_main_menu).pack(side='left', padx=5)
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.*, u.email FROM subscriptions s
                JOIN users u ON s.user_id = u.id
            """)
            subs = cursor.fetchall()
            conn.close()
            
            table_frame = ttk.Frame(self.root)
            table_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side='right', fill='y')
            
            text = scrolledtext.ScrolledText(table_frame, height=20, width=100,
                                            yscrollcommand=scrollbar.set)
            text.pack(fill='both', expand=True)
            scrollbar.config(command=text.yview)
            
            header_text = f"{'ID':<5} {'Email':<25} {'План':<15} {'Статус':<10} {'Начало':<20} {'Конец':<20}\n"
            header_text += "=" * 100 + "\n"
            text.insert('end', header_text)
            
            for sub in subs:
                sub_text = f"{sub['id']:<5} {sub['email']:<25} {sub['plan']:<15} {sub['status']:<10} {sub['start_date']:<20} {sub['end_date']:<20}\n"
                text.insert('end', sub_text)
            
            text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки подписок: {str(e)}")
    
    def add_subscription(self):
        """Добавить подписку"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить подписку")
        dialog.geometry("400x300")
        dialog.configure(bg="#0f172a")
        
        ttk.Label(dialog, text="ID пользователя:").pack(pady=5)
        user_id_entry = ttk.Entry(dialog, width=40)
        user_id_entry.pack(pady=5)
        
        ttk.Label(dialog, text="План:").pack(pady=5)
        plan_var = tk.StringVar()
        plan_combo = ttk.Combobox(dialog, textvariable=plan_var, 
                                 values=["Базовый", "Стандарт", "Премиум"], width=37)
        plan_combo.pack(pady=5)
        
        def save():
            user_id = user_id_entry.get()
            plan = plan_var.get()
            
            if not user_id or not plan:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO subscriptions (user_id, plan, status)
                    VALUES (?, ?, 'active')
                """, (int(user_id), plan))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Успех", "Подписка добавлена!")
                dialog.destroy()
                self.show_subscriptions()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {str(e)}")
        
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=20)
    
    def show_logs(self):
        """Логи системы"""
        self.clear_window()
        
        header = tk.Label(self.root, text="📝 Логи системы", 
                         font=("Arial", 18, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="🗑️ Очистить логи", 
                  command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Обновить", 
                  command=self.show_logs).pack(side='left', padx=5)
        ttk.Button(action_frame, text="⬅️ Назад", 
                  command=self.show_main_menu).pack(side='left', padx=5)
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 100")
            logs = cursor.fetchall()
            conn.close()
            
            table_frame = ttk.Frame(self.root)
            table_frame.pack(fill='both', expand=True, padx=20, pady=10)
            
            scrollbar = ttk.Scrollbar(table_frame)
            scrollbar.pack(side='right', fill='y')
            
            text = scrolledtext.ScrolledText(table_frame, height=20, width=100,
                                            yscrollcommand=scrollbar.set)
            text.pack(fill='both', expand=True)
            scrollbar.config(command=text.yview)
            
            header_text = f"{'ID':<5} {'User ID':<10} {'Action':<20} {'Details':<40} {'Время':<20}\n"
            header_text += "=" * 100 + "\n"
            text.insert('end', header_text)
            
            for log in logs:
                log_text = f"{log['id']:<5} {str(log['user_id']):<10} {log['action']:<20} {str(log['details'])[:40]:<40} {log['created_at']:<20}\n"
                text.insert('end', log_text)
            
            text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки логов: {str(e)}")
    
    def clear_logs(self):
        """Очистить логи"""
        if messagebox.askyesno("Подтверждение", "Вы уверены? Это действие необратимо!"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM logs")
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Логи очищены!")
                self.show_logs()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка очистки: {str(e)}")
    
    def show_stats(self):
        """Статистика"""
        self.clear_window()
        
        header = tk.Label(self.root, text="📈 Статистика", 
                         font=("Arial", 18, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM users")
            users_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as count FROM subscriptions WHERE status = 'active'")
            active_subs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as count FROM logs")
            logs_count = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT plan, COUNT(*) as count FROM subscriptions 
                GROUP BY plan
            """)
            plans = cursor.fetchall()
            
            conn.close()
            
            stats_frame = ttk.Frame(self.root)
            stats_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Статистика
            stat_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                    СТАТИСТИКА СИСТЕМЫ                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  👥 Всего пользователей:              {users_count:<30} ║
║  📊 Активных подписок:                {active_subs:<30} ║
║  📝 Записей в логах:                  {logs_count:<30} ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                    РАСПРЕДЕЛЕНИЕ ПО ПЛАНАМ                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
"""
            
            for plan, count in plans:
                stat_text += f"║  {plan:<40} {count:<20} ║\n"
            
            stat_text += """║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
            
            text_widget = tk.Label(stats_frame, text=stat_text, 
                                  font=("Courier", 11), fg="#16a34a", 
                                  bg="#0f172a", justify='left')
            text_widget.pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки статистики: {str(e)}")
        
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="⬅️ Назад", 
                  command=self.show_main_menu).pack(side='left', padx=5)
    
    def show_settings(self):
        """Настройки БД"""
        self.clear_window()
        
        header = tk.Label(self.root, text="⚙️ Настройки БД", 
                         font=("Arial", 18, "bold"), fg="#16a34a", bg="#0f172a")
        header.pack(pady=10)
        
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Информация о БД
        try:
            if os.path.exists(self.db_path):
                db_size = os.path.getsize(self.db_path) / 1024  # KB
                db_info = f"Размер БД: {db_size:.2f} KB"
            else:
                db_info = "БД не найдена"
            
            info_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                    ИНФОРМАЦИЯ О БД                            ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Путь:                    {self.db_path:<40} ║
║  {db_info:<60} ║
║  Тип:                     SQLite3                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
            
            text_widget = tk.Label(settings_frame, text=info_text, 
                                  font=("Courier", 11), fg="#16a34a", 
                                  bg="#0f172a", justify='left')
            text_widget.pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
        
        # Кнопки действий
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="🔄 Пересоздать БД", 
                  command=self.recreate_db).pack(side='left', padx=5)
        ttk.Button(action_frame, text="💾 Резервная копия", 
                  command=self.backup_db).pack(side='left', padx=5)
        ttk.Button(action_frame, text="⬅️ Назад", 
                  command=self.show_main_menu).pack(side='left', padx=5)
    
    def recreate_db(self):
        """Пересоздать БД"""
        if messagebox.askyesno("Подтверждение", "Это удалит все данные! Продолжить?"):
            try:
                if os.path.exists(self.db_path):
                    os.remove(self.db_path)
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        username TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE subscriptions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        plan TEXT NOT NULL,
                        status TEXT DEFAULT 'active',
                        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        end_date TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        action TEXT NOT NULL,
                        details TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Успех", "БД пересоздана!")
                self.show_settings()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
    
    def backup_db(self):
        """Резервная копия БД"""
        try:
            if not os.path.exists(self.db_path):
                messagebox.showerror("Ошибка", "БД не найдена!")
                return
            
            backup_name = f"sigmavpn_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            import shutil
            shutil.copy(self.db_path, backup_name)
            
            messagebox.showinfo("Успех", f"Резервная копия создана: {backup_name}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания копии: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseLauncher(root)
    root.mainloop()
