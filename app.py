#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Railway переменные окружения
PORT = int(os.getenv('PORT', 5000))
БД_ПУТЬ = os.getenv('DATABASE_PATH', 'sigmavpn.db')

# ==================== ИНИЦИАЛИЗАЦИЯ БД ====================
def инициализировать_бд():
    """Инициализировать базу данных при запуске"""
    if not os.path.exists(БД_ПУТЬ):
        print("📦 Создание базы данных...")
        conn = sqlite3.connect(БД_ПУТЬ)
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица подписок
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Таблица логов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
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
        print("✓ База данных создана успешно!")
    else:
        print("✓ База данных уже существует")

def хеш_пароля(пароль):
    """Хешировать пароль"""
    return hashlib.sha256(пароль.encode()).hexdigest()

def подключиться():
    """Подключиться к базе данных"""
    conn = sqlite3.connect(БД_ПУТЬ)
    conn.row_factory = sqlite3.Row
    return conn

# ==================== РЕГИСТРАЦИЯ ====================
@app.route('/api/register', methods=['POST'])
def регистрация():
    """Регистрация нового пользователя"""
    try:
        данные = request.get_json()
        email = данные.get('email', '').strip()
        пароль = данные.get('password', '').strip()
        имя = данные.get('username', '').strip()
        
        print(f"📝 Попытка регистрации: {email}")
        
        # Валидация
        if not email or not пароль or not имя:
            return jsonify({'успех': False, 'ошибка': 'Заполните все поля'}), 400
        
        if len(пароль) < 6:
            return jsonify({'успех': False, 'ошибка': 'Пароль должен быть минимум 6 символов'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Проверить, существует ли пользователь
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"❌ Email уже зарегистрирован: {email}")
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Email уже зарегистрирован'}), 400
        
        # Добавить пользователя
        хеш = хеш_пароля(пароль)
        print(f"🔐 Хеш пароля: {хеш[:20]}...")
        
        cursor.execute("""
            INSERT INTO users (email, password, username) 
            VALUES (?, ?, ?)
        """, (email, хеш, имя))
        conn.commit()
        
        user_id = cursor.lastrowid
        print(f"✅ Пользователь создан: ID={user_id}, email={email}")
        
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Регистрация успешна!',
            'user_id': user_id,
            'username': имя
        }), 201
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {str(e)}")
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== РЕГИСТРАЦИЯ ЧЕРЕЗ GOOGLE ====================
@app.route('/api/register-google', methods=['POST'])
def регистрация_google():
    """Регистрация через Google"""
    try:
        данные = request.get_json()
        email = данные.get('email', '').strip()
        имя = данные.get('username', '').strip()
        google_id = данные.get('google_id', '').strip()
        picture = данные.get('picture', '')
        
        # Валидация
        if not email or not имя or not google_id:
            return jsonify({'успех': False, 'ошибка': 'Заполните все поля'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Проверить, существует ли пользователь
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        существующий = cursor.fetchone()
        
        if существующий:
            # Если пользователь уже существует, просто вернуть его ID
            conn.close()
            return jsonify({
                'успех': True,
                'сообщение': 'Пользователь уже зарегистрирован',
                'user_id': существующий['id'],
                'username': имя
            }), 200
        
        # Добавить пользователя (без пароля для Google)
        cursor.execute("""
            INSERT INTO users (email, password, username) 
            VALUES (?, ?, ?)
        """, (email, 'google_' + google_id, имя))
        conn.commit()
        
        user_id = cursor.lastrowid
        
        # Добавить лог
        cursor.execute("""
            INSERT INTO logs (user_id, action, details) 
            VALUES (?, ?, ?)
        """, (user_id, 'google_registration', f'Регистрация через Google: {email}'))
        conn.commit()
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Регистрация через Google успешна!',
            'user_id': user_id,
            'username': имя
        }), 201
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== ВХОД ====================
@app.route('/api/login', methods=['POST'])
def вход():
    """Вход пользователя"""
    try:
        данные = request.get_json()
        email = данные.get('email', '').strip()
        пароль = данные.get('password', '').strip()
        
        print(f"📝 Попытка входа: {email}")
        
        if not email or not пароль:
            return jsonify({'успех': False, 'ошибка': 'Email и пароль обязательны'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Найти пользователя
        cursor.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
        пользователь = cursor.fetchone()
        
        if not пользователь:
            print(f"❌ Пользователь не найден: {email}")
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден'}), 401
        
        # Проверить пароль
        хеш = хеш_пароля(пароль)
        print(f"🔐 Проверка пароля...")
        print(f"   Введённый хеш: {хеш[:20]}...")
        print(f"   Сохранённый хеш: {пользователь['password'][:20]}...")
        
        if пользователь['password'] != хеш:
            print(f"❌ Неверный пароль для {email}")
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Неверный пароль'}), 401
        
        print(f"✅ Пароль верный!")
        
        # Добавить лог
        cursor.execute("""
            INSERT INTO logs (user_id, action, details) 
            VALUES (?, ?, ?)
        """, (пользователь['id'], 'login', f'Вход с email: {email}'))
        conn.commit()
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Вход успешен!',
            'user_id': пользователь['id'],
            'username': пользователь['username'],
            'email': email
        }), 200
        
    except Exception as e:
        print(f"❌ Ошибка входа: {str(e)}")
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== ВХОД ЧЕРЕЗ GOOGLE ====================
@app.route('/api/login-google', methods=['POST'])
def вход_google():
    """Вход через Google"""
    try:
        данные = request.get_json()
        email = данные.get('email', '').strip()
        google_id = данные.get('google_id', '').strip()
        
        if not email or not google_id:
            return jsonify({'успех': False, 'ошибка': 'Email и Google ID обязательны'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Найти пользователя
        cursor.execute("SELECT id, username FROM users WHERE email = ?", (email,))
        пользователь = cursor.fetchone()
        
        if not пользователь:
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден. Сначала зарегистрируйтесь'}), 401
        
        # Добавить лог
        cursor.execute("""
            INSERT INTO logs (user_id, action, details) 
            VALUES (?, ?, ?)
        """, (пользователь['id'], 'google_login', f'Вход через Google: {email}'))
        conn.commit()
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Вход через Google успешен!',
            'user_id': пользователь['id'],
            'username': пользователь['username'],
            'email': email
        }), 200
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== ПРОФИЛЬ ====================
@app.route('/api/profile/<int:user_id>', methods=['GET'])
def профиль(user_id):
    """Получить профиль пользователя"""
    try:
        conn = подключиться()
        cursor = conn.cursor()
        
        # Получить пользователя
        cursor.execute("""
            SELECT id, email, username, created_at FROM users WHERE id = ?
        """, (user_id,))
        пользователь = cursor.fetchone()
        
        if not пользователь:
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден'}), 404
        
        # Получить подписку
        cursor.execute("""
            SELECT id, plan, status, start_date, end_date FROM subscriptions 
            WHERE user_id = ? ORDER BY start_date DESC LIMIT 1
        """, (user_id,))
        подписка = cursor.fetchone()
        
        conn.close()
        
        результат = {
            'успех': True,
            'пользователь': {
                'id': пользователь['id'],
                'email': пользователь['email'],
                'username': пользователь['username'],
                'создан': пользователь['created_at']
            }
        }
        
        if подписка:
            результат['подписка'] = {
                'id': подписка['id'],
                'план': подписка['plan'],
                'статус': подписка['status'],
                'начало': подписка['start_date'],
                'конец': подписка['end_date']
            }
        
        return jsonify(результат), 200
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== ПОДПИСКА ====================
@app.route('/api/subscription', methods=['POST'])
def создать_подписку():
    """Создать подписку для пользователя"""
    try:
        данные = request.get_json()
        user_id = данные.get('user_id')
        план = данные.get('plan', 'Стандарт')
        
        if not user_id:
            return jsonify({'успех': False, 'ошибка': 'user_id обязателен'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Проверить пользователя
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден'}), 404
        
        # Определить длительность подписки
        дни = 30
        if план == 'Премиум':
            дни = 365
        elif план == 'Базовый':
            дни = 7
        
        начало = datetime.now()
        конец = начало + timedelta(days=дни)
        
        # Добавить подписку
        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan, status, start_date, end_date) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, план, 'active', начало.isoformat(), конец.isoformat()))
        
        # Добавить лог
        cursor.execute("""
            INSERT INTO logs (user_id, action, details) 
            VALUES (?, ?, ?)
        """, (user_id, 'subscription_created', f'Создана подписка: {план}'))
        
        conn.commit()
        subscription_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': f'Подписка "{план}" активирована!',
            'subscription_id': subscription_id,
            'план': план,
            'начало': начало.isoformat(),
            'конец': конец.isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500


# ==================== СБРОС ПАРОЛЯ ====================
@app.route('/api/reset-password', methods=['POST'])
def сброс_пароля():
    """Сброс пароля пользователя"""
    try:
        данные = request.get_json()
        email = данные.get('email', '').strip()
        
        if not email:
            return jsonify({'успех': False, 'ошибка': 'Email обязателен'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Найти пользователя
        cursor.execute("SELECT id, username FROM users WHERE email = ?", (email,))
        пользователь = cursor.fetchone()
        
        if not пользователь:
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден'}), 404
        
        # Генерировать новый пароль
        import random
        import string
        новый_пароль = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        хеш = хеш_пароля(новый_пароль)
        
        # Обновить пароль
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (хеш, пользователь['id'])
        )
        
        # Добавить лог
        cursor.execute(
            "INSERT INTO logs (user_id, action, details) VALUES (?, ?, ?)",
            (пользователь['id'], 'password_reset', f'Сброс пароля для email: {email}')
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Пароль успешно сброшен!',
            'новый_пароль': новый_пароль
        }), 200
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== СМЕНА ПАРОЛЯ ====================
@app.route('/api/change-password', methods=['POST'])
def смена_пароля():
    """Смена пароля пользователя"""
    try:
        данные = request.get_json()
        user_id = данные.get('user_id')
        новый_пароль = данные.get('new_password', '').strip()
        
        if not user_id or not новый_пароль:
            return jsonify({'успех': False, 'ошибка': 'user_id и пароль обязательны'}), 400
        
        if len(новый_пароль) < 8:
            return jsonify({'успех': False, 'ошибка': 'Пароль должен быть минимум 8 символов'}), 400
        
        conn = подключиться()
        cursor = conn.cursor()
        
        # Проверить пользователя
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'успех': False, 'ошибка': 'Пользователь не найден'}), 404
        
        # Обновить пароль
        хеш = хеш_пароля(новый_пароль)
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (хеш, user_id)
        )
        
        # Добавить лог
        cursor.execute(
            "INSERT INTO logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, 'password_changed', 'Пароль изменён пользователем')
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'успех': True,
            'сообщение': 'Пароль успешно изменён!'
        }), 200
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== СТАТИСТИКА ====================
@app.route('/api/stats', methods=['GET'])
def статистика():
    """Получить статистику"""
    try:
        conn = подключиться()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM users")
        кол_пользователей = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM subscriptions WHERE status = 'active'")
        кол_активных = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM logs")
        кол_логов = cursor.fetchone()['count']
        
        conn.close()
        
        return jsonify({
            'успех': True,
            'статистика': {
                'пользователей': кол_пользователей,
                'активных_подписок': кол_активных,
                'логов': кол_логов
            }
        }), 200
        
    except Exception as e:
        return jsonify({'успех': False, 'ошибка': str(e)}), 500

# ==================== СТАТИЧЕСКИЕ ФАЙЛЫ ====================
@app.route('/')
def главная():
    """Главная страница"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def статические_файлы(filename):
    """Статические файлы"""
    return send_from_directory('.', filename)

# ==================== ЗАПУСК ====================
if __name__ == '__main__':
    инициализировать_бд()
    print("\n🚀 Запуск SigmaVPN API сервера...")
    print(f"📍 http://localhost:{PORT}")
    print("📊 База данных: sigmavpn.db")
    print("✓ Сервер готов к работе!\n")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=PORT)

