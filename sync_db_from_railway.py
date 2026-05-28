#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Синхронизация БД с Railway
Скачивает актуальную БД с Railway перед запуском панели
"""

import os
import sys
import sqlite3
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

LOCAL_DB_PATH = Path(__file__).parent / 'sigmavpn.db'
BACKUP_DB_PATH = Path(__file__).parent / 'sigmavpn.db.backup'

def print_header(text):
    """Печать заголовка"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    """Печать успеха"""
    print(f"✅ {text}")

def print_error(text):
    """Печать ошибки"""
    print(f"❌ {text}")

def print_info(text):
    """Печать информации"""
    print(f"ℹ️  {text}")

def print_warning(text):
    """Печать предупреждения"""
    print(f"⚠️  {text}")

def get_db_size(path):
    """Получить размер БД в MB"""
    if path.exists():
        return path.stat().st_size / 1024 / 1024
    return 0

def backup_local_db():
    """Создать резервную копию локальной БД"""
    if LOCAL_DB_PATH.exists():
        try:
            shutil.copy2(LOCAL_DB_PATH, BACKUP_DB_PATH)
            size = get_db_size(BACKUP_DB_PATH)
            print_success(f"Резервная копия создана ({size:.2f} MB)")
            return True
        except Exception as e:
            print_warning(f"Не удалось создать резервную копию: {e}")
            return False
    return True

def download_db_from_railway():
    """Скачать БД с Railway через Railway CLI"""
    print_header("📥 СКАЧИВАНИЕ БД С RAILWAY")
    
    try:
        # Проверить, установлен ли Railway CLI
        result = subprocess.run(
            ["railway", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            print_warning("Railway CLI не установлен")
            print_info("Установите: npm install -g @railway/cli")
            return False
        
        print_success("Railway CLI найден")
        
        # Скачать БД через Railway shell
        print_info("Подключаюсь к Railway...")
        
        # Экспортировать БД в SQL
        result = subprocess.run(
            ["railway", "run", "pg_dump", "-U", "postgres", "railway"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print_warning("Не удалось экспортировать БД через pg_dump")
            return False
        
        # Сохранить SQL дамп
        sql_dump = result.stdout
        
        # Создать SQLite БД из SQL дампа
        print_info("Конвертирую PostgreSQL в SQLite...")
        
        conn = sqlite3.connect(str(LOCAL_DB_PATH))
        cursor = conn.cursor()
        
        # Парсить и выполнить SQL команды
        for line in sql_dump.split('\n'):
            line = line.strip()
            if line and not line.startswith('--'):
                try:
                    # Преобразовать PostgreSQL синтаксис в SQLite
                    line = line.replace('SERIAL', 'INTEGER')
                    line = line.replace('TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                    
                    if line.endswith(';'):
                        cursor.execute(line)
                except Exception as e:
                    pass  # Пропустить ошибки парсинга
        
        conn.commit()
        conn.close()
        
        size = get_db_size(LOCAL_DB_PATH)
        print_success(f"БД скачана с Railway ({size:.2f} MB)")
        return True
        
    except subprocess.TimeoutExpired:
        print_error("Timeout при подключении к Railway")
        return False
    except Exception as e:
        print_warning(f"Ошибка при скачивании: {e}")
        return False

def verify_local_db():
    """Проверить локальную БД"""
    print_header("🔍 ПРОВЕРКА ЛОКАЛЬНОЙ БД")
    
    if not LOCAL_DB_PATH.exists():
        print_warning("Локальная БД не найдена")
        return False
    
    try:
        conn = sqlite3.connect(str(LOCAL_DB_PATH))
        cursor = conn.cursor()
        
        # Получить список таблиц
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """)
        tables = cursor.fetchall()
        
        size = get_db_size(LOCAL_DB_PATH)
        print_success(f"БД найдена ({size:.2f} MB)")
        print_info(f"Таблиц: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print_info(f"  • {table_name}: {count} строк")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Ошибка при проверке БД: {e}")
        return False

def create_empty_db():
    """Создать пустую БД"""
    try:
        conn = sqlite3.connect(str(LOCAL_DB_PATH))
        cursor = conn.cursor()
        
        # Создать таблицы
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telegram_users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telegram_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                amount INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                payment_id TEXT UNIQUE,
                yandex_payment_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (telegram_id) REFERENCES telegram_users(telegram_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telegram_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                devices INTEGER DEFAULT 1,
                FOREIGN KEY (telegram_id) REFERENCES telegram_users(telegram_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        size = get_db_size(LOCAL_DB_PATH)
        print_success(f"Пустая БД создана ({size:.2f} MB)")
        return True
        
    except Exception as e:
        print_error(f"Ошибка при создании БД: {e}")
        return False

def sync_database():
    """Синхронизировать БД"""
    print_header("🔄 СИНХРОНИЗАЦИЯ БД")
    
    # Шаг 1: Создать резервную копию
    print_info("Шаг 1: Создание резервной копии...")
    backup_local_db()
    
    # Шаг 2: Попытаться скачать с Railway
    print_info("Шаг 2: Скачивание БД с Railway...")
    if download_db_from_railway():
        print_success("БД успешно синхронизирована с Railway")
        return True
    
    # Шаг 3: Если не удалось, использовать локальную
    print_warning("Не удалось скачать с Railway")
    print_info("Шаг 3: Проверка локальной БД...")
    
    if verify_local_db():
        print_success("Используется локальная БД")
        return True
    
    # Шаг 4: Если локальной нет, создать пустую
    print_warning("Локальная БД не найдена")
    print_info("Шаг 4: Создание пустой БД...")
    
    if create_empty_db():
        print_success("Пустая БД создана")
        return True
    
    return False

def main():
    """Главная функция"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔄 СИНХРОНИЗАЦИЯ БД SIGMAVPN С RAILWAY".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print_info(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Локальная БД: {LOCAL_DB_PATH}")
    
    # Синхронизировать БД
    success = sync_database()
    
    # Финальная проверка
    print_header("✅ ФИНАЛЬНАЯ ПРОВЕРКА")
    verify_local_db()
    
    if success:
        print_header("🎉 СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА")
        print_success("БД готова к использованию!")
        return 0
    else:
        print_header("⚠️  СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА С ОШИБКАМИ")
        print_warning("БД может быть неполной или пустой")
        return 1

if __name__ == '__main__':
    sys.exit(main())
