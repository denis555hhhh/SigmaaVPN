#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

БД_ПУТЬ = 'sigmavpn.db'

def подключиться():
    """Подключиться к базе данных"""
    return sqlite3.connect(БД_ПУТЬ)

def показать_таблицы():
    """Показать все таблицы в базе данных"""
    conn = подключиться()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    таблицы = cursor.fetchall()
    
    print("\n📊 Таблицы в базе данных:")
    for таблица in таблицы:
        print(f"  ✓ {таблица[0]}")
    
    conn.close()

def показать_пользователей():
    """Показать всех пользователей"""
    conn = подключиться()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, username, created_at FROM users;")
    пользователи = cursor.fetchall()
    
    print("\n👥 Пользователи:")
    if пользователи:
        for пользователь in пользователи:
            print(f"  ID: {пользователь[0]}")
            print(f"  Email: {пользователь[1]}")
            print(f"  Имя: {пользователь[2]}")
            print(f"  Создан: {пользователь[3]}")
            print()
    else:
        print("  Пользователей нет")
    
    conn.close()

def добавить_пользователя(email, пароль, имя):
    """Добавить нового пользователя"""
    conn = подключиться()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO users (email, password, username) 
            VALUES (?, ?, ?)
        """, (email, пароль, имя))
        conn.commit()
        print(f"✅ Пользователь '{имя}' добавлен успешно!")
    except sqlite3.IntegrityError:
        print(f"❌ Ошибка: Email '{email}' уже существует")
    finally:
        conn.close()

def добавить_подписку(user_id, план, статус='active'):
    """Добавить подписку пользователю"""
    conn = подключиться()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan, status) 
            VALUES (?, ?, ?)
        """, (user_id, план, статус))
        conn.commit()
        print(f"✅ Подписка '{план}' добавлена пользователю ID {user_id}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()

def показать_подписки():
    """Показать все подписки"""
    conn = подключиться()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.id, u.username, s.plan, s.status, s.start_date 
        FROM subscriptions s 
        JOIN users u ON s.user_id = u.id
    """)
    подписки = cursor.fetchall()
    
    print("\n📋 Подписки:")
    if подписки:
        for подписка in подписки:
            print(f"  ID: {подписка[0]}")
            print(f"  Пользователь: {подписка[1]}")
            print(f"  План: {подписка[2]}")
            print(f"  Статус: {подписка[3]}")
            print(f"  Начало: {подписка[4]}")
            print()
    else:
        print("  Подписок нет")
    
    conn.close()

def статистика():
    """Показать статистику базы данных"""
    conn = подключиться()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users;")
    кол_пользователей = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM subscriptions;")
    кол_подписок = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM logs;")
    кол_логов = cursor.fetchone()[0]
    
    print("\n📈 Статистика базы данных:")
    print(f"  👥 Пользователей: {кол_пользователей}")
    print(f"  📋 Подписок: {кол_подписок}")
    print(f"  📝 Логов: {кол_логов}")
    
    conn.close()

def главное_меню():
    """Главное меню"""
    while True:
        print("\n" + "="*50)
        print("🔐 УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ SIGMAVPN")
        print("="*50)
        print("1. Показать таблицы")
        print("2. Показать пользователей")
        print("3. Добавить пользователя")
        print("4. Показать подписки")
        print("5. Добавить подписку")
        print("6. Статистика")
        print("0. Выход")
        print("="*50)
        
        выбор = input("Выберите действие (0-6): ").strip()
        
        if выбор == '1':
            показать_таблицы()
        elif выбор == '2':
            показать_пользователей()
        elif выбор == '3':
            email = input("Email: ").strip()
            пароль = input("Пароль: ").strip()
            имя = input("Имя пользователя: ").strip()
            добавить_пользователя(email, пароль, имя)
        elif выбор == '4':
            показать_подписки()
        elif выбор == '5':
            user_id = input("ID пользователя: ").strip()
            план = input("План (Базовый/Стандарт/Премиум): ").strip()
            добавить_подписку(int(user_id), план)
        elif выбор == '6':
            статистика()
        elif выбор == '0':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    if not os.path.exists(БД_ПУТЬ):
        print("❌ База данных не найдена!")
        print("Создайте её, запустив: python create_database.py")
    else:
        главное_меню()
