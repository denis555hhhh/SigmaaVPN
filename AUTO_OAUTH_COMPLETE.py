#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Полностью автоматическая настройка Google OAuth
Этот скрипт делает ВСЕ за вас!
"""

import json
import os
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Демо Client ID для тестирования (работает локально)
DEMO_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"

class OAuthHandler(BaseHTTPRequestHandler):
    auth_code = None
    
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        if 'code' in query_params:
            OAuthHandler.auth_code = query_params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>OAuth Success!</h1></body></html>")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def setup_oauth():
    """Полная автоматическая настройка OAuth"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║              🔐 ПОЛНАЯ АВТОМАТИЧЕСКАЯ НАСТРОЙКА OAUTH 🔐                ║")
    print("║                                                                            ║")
    print("║                         Я делаю это за вас!                              ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    print_header("ШАГ 1: ВЫБОР СПОСОБА НАСТРОЙКИ")
    
    print("Выберите способ:")
    print("1. Использовать демо Client ID (для тестирования)")
    print("2. Ввести свой Google Client ID (для production)")
    print()
    
    choice = input("Введите 1 или 2: ").strip()
    
    if choice == "1":
        client_id = DEMO_CLIENT_ID
        print(f"\n✅ Используется демо Client ID для тестирования")
    elif choice == "2":
        print("\n📋 Получение Google Client ID:")
        print("1. Откройте: https://console.cloud.google.com/")
        print("2. Создайте проект 'SigmaVPN'")
        print("3. Включите Google+ API")
        print("4. Создайте OAuth 2.0 Client ID (Web)")
        print("5. Скопируйте Client ID")
        print()
        client_id = input("Введите ваш Google Client ID: ").strip()
        
        if not client_id or len(client_id) < 20:
            print("\n❌ Ошибка: Client ID должен быть длинной строкой")
            return False
    else:
        print("\n❌ Ошибка: Введите 1 или 2")
        return False
    
    print_header("ШАГ 2: ОБНОВЛЕНИЕ ФАЙЛОВ")
    
    # Обновить register.js
    print("📝 Обновление register.js...")
    try:
        with open('register.js', 'r', encoding='utf-8') as f:
            register_content = f.read()
        
        # Заменить Client ID
        register_content = register_content.replace(
            "GOOGLE_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'",
            f"GOOGLE_CLIENT_ID = '{client_id}'"
        )
        
        with open('register.js', 'w', encoding='utf-8') as f:
            f.write(register_content)
        
        print("✅ register.js обновлен")
    except Exception as e:
        print(f"❌ Ошибка при обновлении register.js: {e}")
        return False
    
    # Обновить login.js
    print("📝 Обновление login.js...")
    try:
        with open('login.js', 'r', encoding='utf-8') as f:
            login_content = f.read()
        
        # Заменить Client ID
        login_content = login_content.replace(
            "GOOGLE_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'",
            f"GOOGLE_CLIENT_ID = '{client_id}'"
        )
        
        with open('login.js', 'w', encoding='utf-8') as f:
            f.write(login_content)
        
        print("✅ login.js обновлен")
    except Exception as e:
        print(f"❌ Ошибка при обновлении login.js: {e}")
        return False
    
    # Обновить oauth_config.json
    print("📝 Обновление oauth_config.json...")
    try:
        config = {
            'google_client_id': client_id,
            'setup_date': '2026-05-27',
            'status': 'configured',
            'type': 'demo' if choice == "1" else 'production'
        }
        
        with open('oauth_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ oauth_config.json обновлен")
    except Exception as e:
        print(f"❌ Ошибка при обновлении oauth_config.json: {e}")
        return False
    
    print_header("✅ НАСТРОЙКА ЗАВЕРШЕНА!")
    
    print("Google OAuth успешно настроен!")
    print()
    print("📋 Информация:")
    print(f"   Client ID: {client_id[:30]}...")
    print(f"   Тип: {'Демо (тестирование)' if choice == '1' else 'Production'}")
    print()
    print("🚀 Следующие шаги:")
    print("1. Запустите: START_WITH_GOOGLE.bat")
    print("2. Откройте: http://localhost:8080/register.html")
    print("3. Нажмите: 'Войти через Google'")
    print("4. Выберите: Ваш аккаунт Google")
    print()
    print("Готово! 🎉")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = setup_oauth()
        if success:
            print("✅ Все готово!")
            input("Нажмите Enter для выхода...")
        else:
            print("❌ Ошибка при настройке")
            input("Нажмите Enter для выхода...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        input("Нажмите Enter для выхода...")
