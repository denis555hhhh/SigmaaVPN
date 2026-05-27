#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'sigmavpn_admin_secret_key_2026'
CORS(app)

DB_PATH = 'sigmavpn.db'
ADMIN_PASSWORD = hashlib.sha256('admin123'.encode()).hexdigest()

# HTML Шаблон
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 SigmaVPN - Админ Панель</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(22, 163, 74, 0.1);
            border: 2px solid #16a34a;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        header h1 {
            color: #16a34a;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .nav {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .nav button {
            background: #16a34a;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .nav button:hover {
            background: #15803d;
            transform: translateY(-2px);
        }
        
        .nav button.active {
            background: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
        }
        
        .content {
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #16a34a;
            border-radius: 10px;
            padding: 20px;
            min-height: 500px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #16a34a;
        }
        
        th {
            background: rgba(22, 163, 74, 0.2);
            color: #16a34a;
            font-weight: bold;
        }
        
        tr:hover {
            background: rgba(22, 163, 74, 0.1);
        }
        
        .btn {
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
        }
        
        .btn-delete {
            background: #dc2626;
            color: white;
        }
        
        .btn-delete:hover {
            background: #b91c1c;
        }
        
        .btn-edit {
            background: #3b82f6;
            color: white;
            margin-right: 5px;
        }
        
        .btn-edit:hover {
            background: #2563eb;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(22, 163, 74, 0.1);
            border: 2px solid #16a34a;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-card h3 {
            color: #16a34a;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .stat-card .number {
            font-size: 32px;
            font-weight: bold;
            color: #22c55e;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #16a34a;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px;
            background: #0f172a;
            border: 1px solid #16a34a;
            border-radius: 5px;
            color: white;
            font-size: 14px;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            box-shadow: 0 0 10px rgba(22, 163, 74, 0.5);
        }
        
        .btn-submit {
            background: #16a34a;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            width: 100%;
        }
        
        .btn-submit:hover {
            background: #15803d;
        }
        
        .alert {
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            color: #22c55e;
        }
        
        .alert-error {
            background: rgba(220, 38, 38, 0.2);
            border: 1px solid #dc2626;
            color: #dc2626;
        }
        
        .hidden {
            display: none;
        }
        
        .logout {
            position: absolute;
            top: 20px;
            right: 20px;
        }
        
        .logout button {
            background: #dc2626;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .logout button:hover {
            background: #b91c1c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logout">
            <button onclick="logout()">🚪 Выход</button>
        </div>
        
        <header>
            <h1>🔒 SigmaVPN - Админ Панель</h1>
            <p>Полное управление базой данных</p>
        </header>
        
        <div class="nav">
            <button class="active" onclick="showSection('dashboard')">📊 Панель управления</button>
            <button onclick="showSection('users')">👥 Пользователи</button>
            <button onclick="showSection('subscriptions')">📋 Подписки</button>
            <button onclick="showSection('logs')">📝 Логи</button>
            <button onclick="showSection('settings')">⚙️ Настройки</button>
        </div>
        
        <div class="content">
            <!-- Dashboard -->
            <div id="dashboard" class="section">
                <h2>📊 Панель управления</h2>
                <div class="stats" id="stats"></div>
            </div>
            
            <!-- Users -->
            <div id="users" class="section hidden">
                <h2>👥 Управление пользователями</h2>
                <button class="btn btn-edit" onclick="showAddUserForm()">➕ Добавить пользователя</button>
                <div id="addUserForm" class="hidden" style="margin: 20px 0; padding: 20px; background: rgba(22, 163, 74, 0.1); border-radius: 5px;">
                    <h3>Добавить нового пользователя</h3>
                    <div class="form-group">
                        <label>Email:</label>
                        <input type="email" id="newUserEmail" placeholder="user@example.com">
                    </div>
                    <div class="form-group">
                        <label>Username:</label>
                        <input type="text" id="newUserUsername" placeholder="username">
                    </div>
                    <div class="form-group">
                        <label>Пароль:</label>
                        <input type="password" id="newUserPassword" placeholder="password">
                    </div>
                    <button class="btn-submit" onclick="addUser()">Добавить</button>
                </div>
                <table id="usersTable"></table>
            </div>
            
            <!-- Subscriptions -->
            <div id="subscriptions" class="section hidden">
                <h2>📋 Управление подписками</h2>
                <button class="btn btn-edit" onclick="showAddSubForm()">➕ Добавить подписку</button>
                <div id="addSubForm" class="hidden" style="margin: 20px 0; padding: 20px; background: rgba(22, 163, 74, 0.1); border-radius: 5px;">
                    <h3>Добавить новую подписку</h3>
                    <div class="form-group">
                        <label>ID пользователя:</label>
                        <input type="number" id="newSubUserId" placeholder="1">
                    </div>
                    <div class="form-group">
                        <label>План:</label>
                        <select id="newSubPlan">
                            <option>Базовый</option>
                            <option>Стандарт</option>
                            <option>Премиум</option>
                        </select>
                    </div>
                    <button class="btn-submit" onclick="addSubscription()">Добавить</button>
                </div>
                <table id="subsTable"></table>
            </div>
            
            <!-- Logs -->
            <div id="logs" class="section hidden">
                <h2>📝 Логи системы</h2>
                <button class="btn btn-delete" onclick="clearLogs()">🗑️ Очистить логи</button>
                <table id="logsTable"></table>
            </div>
            
            <!-- Settings -->
            <div id="settings" class="section hidden">
                <h2>⚙️ Настройки</h2>
                <div style="margin: 20px 0;">
                    <button class="btn btn-edit" onclick="backupDB()">💾 Резервная копия</button>
                    <button class="btn btn-delete" onclick="recreateDB()">🔄 Пересоздать БД</button>
                </div>
                <div id="dbInfo" style="margin-top: 20px; padding: 20px; background: rgba(22, 163, 74, 0.1); border-radius: 5px;"></div>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(section) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(section).classList.remove('hidden');
            
            document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            if (section === 'dashboard') loadDashboard();
            if (section === 'users') loadUsers();
            if (section === 'subscriptions') loadSubscriptions();
            if (section === 'logs') loadLogs();
            if (section === 'settings') loadSettings();
        }
        
        function loadDashboard() {
            fetch('/api/admin/stats')
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    for (let key in data) {
                        html += `<div class="stat-card"><h3>${key}</h3><div class="number">${data[key]}</div></div>`;
                    }
                    document.getElementById('stats').innerHTML = html;
                });
        }
        
        function loadUsers() {
            fetch('/api/admin/users')
                .then(r => r.json())
                .then(users => {
                    let html = '<tr><th>ID</th><th>Email</th><th>Username</th><th>Создан</th><th>Действия</th></tr>';
                    users.forEach(u => {
                        html += `<tr>
                            <td>${u.id}</td>
                            <td>${u.email}</td>
                            <td>${u.username}</td>
                            <td>${u.created_at}</td>
                            <td><button class="btn btn-delete" onclick="deleteUser(${u.id})">🗑️ Удалить</button></td>
                        </tr>`;
                    });
                    document.getElementById('usersTable').innerHTML = html;
                });
        }
        
        function loadSubscriptions() {
            fetch('/api/admin/subscriptions')
                .then(r => r.json())
                .then(subs => {
                    let html = '<tr><th>ID</th><th>Email</th><th>План</th><th>Статус</th><th>Начало</th><th>Конец</th><th>Действия</th></tr>';
                    subs.forEach(s => {
                        html += `<tr>
                            <td>${s.id}</td>
                            <td>${s.email}</td>
                            <td>${s.plan}</td>
                            <td>${s.status}</td>
                            <td>${s.start_date}</td>
                            <td>${s.end_date || '-'}</td>
                            <td><button class="btn btn-delete" onclick="deleteSubscription(${s.id})">🗑️ Удалить</button></td>
                        </tr>`;
                    });
                    document.getElementById('subsTable').innerHTML = html;
                });
        }
        
        function loadLogs() {
            fetch('/api/admin/logs')
                .then(r => r.json())
                .then(logs => {
                    let html = '<tr><th>ID</th><th>User ID</th><th>Action</th><th>Details</th><th>Время</th></tr>';
                    logs.forEach(l => {
                        html += `<tr>
                            <td>${l.id}</td>
                            <td>${l.user_id || '-'}</td>
                            <td>${l.action}</td>
                            <td>${l.details || '-'}</td>
                            <td>${l.created_at}</td>
                        </tr>`;
                    });
                    document.getElementById('logsTable').innerHTML = html;
                });
        }
        
        function loadSettings() {
            fetch('/api/admin/dbinfo')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('dbInfo').innerHTML = `
                        <p><strong>Путь:</strong> ${data.path}</p>
                        <p><strong>Размер:</strong> ${data.size} KB</p>
                        <p><strong>Тип:</strong> SQLite3</p>
                    `;
                });
        }
        
        function showAddUserForm() {
            document.getElementById('addUserForm').classList.toggle('hidden');
        }
        
        function showAddSubForm() {
            document.getElementById('addSubForm').classList.toggle('hidden');
        }
        
        function addUser() {
            const data = {
                email: document.getElementById('newUserEmail').value,
                username: document.getElementById('newUserUsername').value,
                password: document.getElementById('newUserPassword').value
            };
            
            fetch('/api/admin/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(r => r.json()).then(data => {
                alert(data.message);
                loadUsers();
                document.getElementById('addUserForm').classList.add('hidden');
            });
        }
        
        function deleteUser(id) {
            if (confirm('Удалить пользователя?')) {
                fetch(`/api/admin/users/${id}`, {method: 'DELETE'})
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message);
                        loadUsers();
                    });
            }
        }
        
        function addSubscription() {
            const data = {
                user_id: document.getElementById('newSubUserId').value,
                plan: document.getElementById('newSubPlan').value
            };
            
            fetch('/api/admin/subscriptions', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            }).then(r => r.json()).then(data => {
                alert(data.message);
                loadSubscriptions();
                document.getElementById('addSubForm').classList.add('hidden');
            });
        }
        
        function deleteSubscription(id) {
            if (confirm('Удалить подписку?')) {
                fetch(`/api/admin/subscriptions/${id}`, {method: 'DELETE'})
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message);
                        loadSubscriptions();
                    });
            }
        }
        
        function clearLogs() {
            if (confirm('Очистить все логи? Это действие необратимо!')) {
                fetch('/api/admin/logs', {method: 'DELETE'})
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message);
                        loadLogs();
                    });
            }
        }
        
        function backupDB() {
            fetch('/api/admin/backup', {method: 'POST'})
                .then(r => r.json())
                .then(data => alert(data.message));
        }
        
        function recreateDB() {
            if (confirm('Пересоздать БД? Все данные будут удалены!')) {
                fetch('/api/admin/recreate', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message);
                        loadDashboard();
                    });
            }
        }
        
        function logout() {
            fetch('/api/admin/logout', {method: 'POST'})
                .then(() => location.reload());
        }
        
        loadDashboard();
    </script>
</body>
</html>
'''

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'admin' not in session:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>🔒 SigmaVPN - Админ Вход</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    margin: 0;
                }
                .login-box {
                    background: rgba(30, 41, 59, 0.9);
                    border: 2px solid #16a34a;
                    border-radius: 10px;
                    padding: 40px;
                    text-align: center;
                    width: 300px;
                }
                h1 {
                    color: #16a34a;
                    margin-bottom: 30px;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    background: #0f172a;
                    border: 1px solid #16a34a;
                    border-radius: 5px;
                    color: white;
                    font-size: 14px;
                }
                button {
                    width: 100%;
                    padding: 10px;
                    background: #16a34a;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    margin-top: 20px;
                }
                button:hover {
                    background: #15803d;
                }
                .info {
                    color: #94a3b8;
                    font-size: 12px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="login-box">
                <h1>🔒 Админ Панель</h1>
                <form method="POST" action="/api/admin/login">
                    <input type="password" name="password" placeholder="Пароль" required>
                    <button type="submit">Вход</button>
                </form>
                <div class="info">Пароль: admin123</div>
            </div>
        </body>
        </html>
        ''')
    
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    password = request.form.get('password', '')
    if hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD:
        session['admin'] = True
        return {'success': True}, 302, {'Location': '/'}
    return {'success': False, 'message': 'Неверный пароль'}, 401

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.clear()
    return {'message': 'Вы вышли'}

@app.route('/api/admin/stats')
def admin_stats():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM users")
    users = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM subscriptions WHERE status = 'active'")
    active_subs = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM logs")
    logs = cursor.fetchone()['count']
    
    conn.close()
    
    return {
        '👥 Пользователей': users,
        '📊 Активных подписок': active_subs,
        '📝 Записей в логах': logs
    }

@app.route('/api/admin/users')
def admin_users():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return users

@app.route('/api/admin/users', methods=['POST'])
def admin_add_user():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        cursor.execute("""
            INSERT INTO users (email, username, password)
            VALUES (?, ?, ?)
        """, (data['email'], data['username'], password_hash))
        conn.commit()
        conn.close()
        return {'message': 'Пользователь добавлен'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {'message': 'Пользователь удален'}

@app.route('/api/admin/subscriptions')
def admin_subscriptions():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.*, u.email FROM subscriptions s
        JOIN users u ON s.user_id = u.id
    """)
    subs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return subs

@app.route('/api/admin/subscriptions', methods=['POST'])
def admin_add_subscription():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan, status)
            VALUES (?, ?, 'active')
        """, (data['user_id'], data['plan']))
        conn.commit()
        conn.close()
        return {'message': 'Подписка добавлена'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/admin/subscriptions/<int:sub_id>', methods=['DELETE'])
def admin_delete_subscription(sub_id):
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
    conn.commit()
    conn.close()
    
    return {'message': 'Подписка удалена'}

@app.route('/api/admin/logs')
def admin_logs():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 100")
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return logs

@app.route('/api/admin/logs', methods=['DELETE'])
def admin_clear_logs():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    
    return {'message': 'Логи очищены'}

@app.route('/api/admin/dbinfo')
def admin_dbinfo():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    if os.path.exists(DB_PATH):
        size = os.path.getsize(DB_PATH) / 1024
    else:
        size = 0
    
    return {
        'path': DB_PATH,
        'size': f'{size:.2f}',
        'type': 'SQLite3'
    }

@app.route('/api/admin/backup', methods=['POST'])
def admin_backup():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        import shutil
        backup_name = f"sigmavpn_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy(DB_PATH, backup_name)
        return {'message': f'Резервная копия создана: {backup_name}'}
    except Exception as e:
        return {'error': str(e)}, 400

@app.route('/api/admin/recreate', methods=['POST'])
def admin_recreate():
    if 'admin' not in session:
        return {'error': 'Unauthorized'}, 401
    
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        
        conn = sqlite3.connect(DB_PATH)
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
        
        return {'message': 'БД пересоздана'}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    print("🚀 Запуск веб-админ панели на http://localhost:5001")
    app.run(debug=False, host='0.0.0.0', port=5001)
