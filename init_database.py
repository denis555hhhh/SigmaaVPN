#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

DB_PATH = 'sigmavpn.db'

def init_database():
    """Инициализировать базу данных"""
    try:
        # Удалить старую БД если существует
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print(f"✓ Старая база данных удалена")
        
        # Создать новую БД
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Таблица 'users' создана")
        
        # Таблица подписок
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
        print("✓ Таблица 'subscriptions' создана")
        
        # Таблица логов
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
        print("✓ Таблица 'logs' создана")
        
        conn.commit()
        conn.close()
        
        print(f"\n✓ База данных '{DB_PATH}' успешно инициализирована!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании БД: {e}")
        return False

if __name__ == '__main__':
    init_database()
