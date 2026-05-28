#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скачивание БД с Railway через прямое подключение к PostgreSQL
Не требует Railway CLI или Node.js
Использует переменные из .env файла
"""

import os
import sys
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Загрузить переменные из .env файла
load_dotenv()

LOCAL_DB_PATH = Path(__file__).parent / 'sigmavpn.db'
BACKUP_DB_PATH = Path(__file__).parent / 'sigmavpn.db.backup'

# Railway PostgreSQL конфигурация
# Способ 1: Использовать DATABASE_URL если она установлена
RAILWAY_DB_URL = os.getenv('DATABASE_URL', '')

# Способ 2: Если DATABASE_URL не установлена, построить из отдельных переменных
if not RAILWAY_DB_URL:
    PGHOST = os.getenv('PGHOST', '')
    PGPORT = os.getenv('PGPORT', '5432')
    PGUSER = os.getenv('PGUSER', 'postgres')
    PGPASSWORD = os.getenv('PGPASSWORD', '')
    PGDATABASE = os.getenv('PGDATABASE', 'railway')
    
    if PGHOST and PGPASSWORD:
        RAILWAY_DB_URL = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'

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
    """Скачать БД с Railway через прямое подключение"""
    print_header("📥 СКАЧИВАНИЕ БД С RAILWAY")
    
    # Проверить DATABASE_URL
    if not RAILWAY_DB_URL:
        print_warning("DATABASE_URL не установлена")
        print_info("Используется локальная БД")
        return False
    
    try:
        # Попытка установить psycopg2
        try:
            import psycopg2
        except ImportError:
            print_info("Установка psycopg2...")
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], 
                         capture_output=True)
            import psycopg2
        
        print_info("Подключаюсь к Railway PostgreSQL...")
        
        # Подключиться к Railway БД
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cursor = conn.cursor()
        
        print_success("Подключение к Railway установлено")
        
        # Получить список таблиц
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print_info(f"Найдено таблиц: {len(tables)}")
        
        # Создать локальную SQLite БД
        print_info("Создаю локальную SQLite БД...")
        local_conn = sqlite3.connect(str(LOCAL_DB_PATH))
        local_cursor = local_conn.cursor()
        
        # Копировать каждую таблицу
        for table_name in tables:
            print_info(f"  Копирую таблицу: {table_name}")
            
            try:
                # Получить структуру таблицы
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                
                if not columns:
                    continue
                
                # Создать таблицу в SQLite
                create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
                col_names = []
                
                for col in columns:
                    col_name = col[0]
                    col_type = col[1]
                    is_nullable = col[2]
                    
                    col_names.append(col_name)
                    
                    # Преобразовать типы данных PostgreSQL в SQLite
                    if 'int' in col_type.lower():
                        sqlite_type = 'INTEGER'
                    elif 'text' in col_type.lower() or 'varchar' in col_type.lower():
                        sqlite_type = 'TEXT'
                    elif 'timestamp' in col_type.lower() or 'date' in col_type.lower():
                        sqlite_type = 'TIMESTAMP'
                    elif 'boolean' in col_type.lower():
                        sqlite_type = 'INTEGER'
                    elif 'numeric' in col_type.lower() or 'decimal' in col_type.lower():
                        sqlite_type = 'REAL'
                    else:
                        sqlite_type = 'TEXT'
                    
                    nullable = '' if is_nullable == 'NO' else ''
                    create_sql += f"{col_name} {sqlite_type} {nullable}, "
                
                create_sql = create_sql.rstrip(', ') + ")"
                
                try:
                    local_cursor.execute(create_sql)
                except:
                    pass  # Таблица уже существует
                
                # Получить данные
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if rows:
                    # Вставить данные
                    placeholders = ', '.join(['?' for _ in col_names])
                    insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    
                    for row in rows:
                        try:
                            local_cursor.execute(insert_sql, row)
                        except Exception as e:
                            pass  # Пропустить ошибки вставки
                    
                    print_info(f"    Скопировано строк: {len(rows)}")
                else:
                    print_info(f"    Таблица пуста")
                    
            except Exception as e:
                print_warning(f"    Ошибка при копировании таблицы {table_name}: {e}")
                continue
        
        local_conn.commit()
        local_conn.close()
        conn.close()
        
        size = get_db_size(LOCAL_DB_PATH)
        print_success(f"БД скачана с Railway ({size:.2f} MB)")
        return True
        
    except Exception as e:
        print_error(f"Ошибка при скачивании: {e}")
        print_info("Убедитесь что DATABASE_URL установлена правильно")
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

def main():
    """Главная функция"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  📥 СКАЧИВАНИЕ БД SIGMAVPN С RAILWAY".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    print_info(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Локальная БД: {LOCAL_DB_PATH}")
    
    # Шаг 1: Создать резервную копию
    print_info("Шаг 1: Создание резервной копии...")
    backup_local_db()
    
    # Шаг 2: Попытаться скачать с Railway
    print_info("Шаг 2: Скачивание БД с Railway...")
    if download_db_from_railway():
        print_success("БД успешно скачана с Railway")
    else:
        print_warning("Не удалось скачать с Railway")
        print_info("Шаг 3: Проверка локальной БД...")
        
        if verify_local_db():
            print_success("Используется локальная БД")
        else:
            print_error("Локальная БД не найдена")
            return 1
    
    # Финальная проверка
    print_header("✅ ФИНАЛЬНАЯ ПРОВЕРКА")
    verify_local_db()
    
    print_header("🎉 СКАЧИВАНИЕ ЗАВЕРШЕНО")
    print_success("БД готова к использованию!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
