#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Получение Google OAuth токена автоматически
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser
import time

class OAuthHandler(BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        """Обработать callback от Google"""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            OAuthHandler.auth_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head>
                <meta charset="utf-8">
                <title>OAuth успешен</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: #f0f0f0; }
                    .success { background: #4CAF50; color: white; padding: 20px; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="success">
                    <h1>✅ OAuth успешен!</h1>
                    <p>Вы можете закрыть это окно</p>
                </div>
            </body>
            </html>
            """)
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Отключить логирование"""
        pass

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                  🔐 ПОЛУЧЕНИЕ GOOGLE OAUTH ТОКЕНА 🔐                     ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Проверить конфиг
    if not os.path.exists('oauth_config.json'):
        print("❌ Ошибка: oauth_config.json не найден")
        print("Запустите setup_oauth.py сначала")
        return
    
    with open('oauth_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    client_id = config.get('google_client_id')
    
    if not client_id or client_id == 'YOUR_CLIENT_ID_HERE':
        print("❌ Ошибка: Google Client ID не настроен")
        print("Запустите setup_oauth.py для настройки")
        return
    
    print_header("ПОЛУЧЕНИЕ ТОКЕНА")
    
    print("1️⃣  Запуск локального сервера на порту 8888...")
    
    # Запустить локальный сервер
    server = HTTPServer(('localhost', 8888), OAuthHandler)
    
    # Построить URL для авторизации
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri=http://localhost:8888/callback&"
        f"response_type=code&"
        f"scope=openid%20email%20profile"
    )
    
    print("✅ Сервер запущен")
    print()
    print("2️⃣  Открытие браузера для авторизации...")
    
    # Открыть браузер
    webbrowser.open(auth_url)
    
    print("✅ Браузер открыт")
    print()
    print("3️⃣  Ожидание авторизации...")
    print("   (Выберите аккаунт Google и разрешите доступ)")
    print()
    
    # Ждать callback
    timeout = time.time() + 300  # 5 минут timeout
    while OAuthHandler.auth_code is None and time.time() < timeout:
        server.handle_request()
    
    server.server_close()
    
    if OAuthHandler.auth_code:
        print("✅ Авторизация успешна!")
        print()
        print("📋 Ваш Authorization Code:")
        print(f"   {OAuthHandler.auth_code}")
        print()
        
        # Сохранить в конфиг
        config['auth_code'] = OAuthHandler.auth_code
        config['status'] = 'authorized'
        
        with open('oauth_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ Authorization Code сохранен в oauth_config.json")
        print()
        print("Готово! Теперь вы можете использовать Google OAuth")
    else:
        print("❌ Timeout: авторизация не была завершена")

if __name__ == '__main__':
    main()
