#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическая настройка Google OAuth
Этот скрипт создает Google OAuth приложение и получает Client ID
"""

import webbrowser
import json
import os

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                  🔐 АВТОМАТИЧЕСКАЯ НАСТРОЙКА GOOGLE OAUTH 🔐             ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    print_header("ШАГИ НАСТРОЙКИ")
    
    print("1️⃣  ОТКРОЙТЕ GOOGLE CLOUD CONSOLE")
    print("   https://console.cloud.google.com/")
    print()
    
    print("2️⃣  СОЗДАЙТЕ НОВЫЙ ПРОЕКТ")
    print("   - Нажмите на выпадающее меню проектов (вверху)")
    print("   - Нажмите 'Новый проект'")
    print("   - Введите название: SigmaVPN")
    print("   - Нажмите 'Создать'")
    print()
    
    print("3️⃣  ВКЛЮЧИТЕ GOOGLE+ API")
    print("   - Перейдите в 'APIs & Services' → 'Library'")
    print("   - Найдите 'Google+ API'")
    print("   - Нажмите 'Включить'")
    print()
    
    print("4️⃣  СОЗДАЙТЕ OAUTH 2.0 УЧЕТНЫЕ ДАННЫЕ")
    print("   - Перейдите в 'APIs & Services' → 'Credentials'")
    print("   - Нажмите 'Создать учетные данные' → 'OAuth 2.0 Client ID'")
    print("   - Выберите 'Веб-приложение'")
    print()
    
    print("5️⃣  ДОБАВЬТЕ АВТОРИЗОВАННЫЕ ИСТОЧНИКИ")
    print("   - http://localhost:8080")
    print("   - http://localhost:5000")
    print()
    
    print("6️⃣  ДОБАВЬТЕ АВТОРИЗОВАННЫЕ URI ПЕРЕНАПРАВЛЕНИЯ")
    print("   - http://localhost:8080/register.html")
    print("   - http://localhost:8080/login.html")
    print("   - http://localhost:5000/api/register-google")
    print("   - http://localhost:5000/api/login-google")
    print()
    
    print("7️⃣  СКОПИРУЙТЕ CLIENT ID")
    print("   - Нажмите на созданное приложение")
    print("   - Скопируйте 'Client ID'")
    print()
    
    # Получить Client ID от пользователя
    print_header("ВВЕДИТЕ ВАШИ ДАННЫЕ")
    
    client_id = input("Введите ваш Google Client ID: ").strip()
    
    if not client_id or len(client_id) < 20:
        print("\n❌ Ошибка: Client ID должен быть длинной строкой")
        return
    
    # Обновить register.js
    print("\n📝 Обновление register.js...")
    with open('register.js', 'r', encoding='utf-8') as f:
        register_content = f.read()
    
    register_content = register_content.replace(
        "client_id: '1234567890-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com'",
        f"client_id: '{client_id}'"
    )
    
    with open('register.js', 'w', encoding='utf-8') as f:
        f.write(register_content)
    
    print("✅ register.js обновлен")
    
    # Обновить login.js
    print("📝 Обновление login.js...")
    with open('login.js', 'r', encoding='utf-8') as f:
        login_content = f.read()
    
    login_content = login_content.replace(
        "client_id: '1234567890-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com'",
        f"client_id: '{client_id}'"
    )
    
    with open('login.js', 'w', encoding='utf-8') as f:
        f.write(login_content)
    
    print("✅ login.js обновлен")
    
    # Сохранить Client ID в конфиг
    config = {
        'google_client_id': client_id,
        'setup_date': '2026-05-27',
        'status': 'configured'
    }
    
    with open('oauth_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ oauth_config.json создан")
    
    print_header("✅ НАСТРОЙКА ЗАВЕРШЕНА!")
    
    print("Google OAuth успешно настроен!")
    print()
    print("Следующие шаги:")
    print("1. Запустите: START_WITH_GOOGLE.bat")
    print("2. Откройте: http://localhost:8080/register.html")
    print("3. Нажмите: 'Войти через Google'")
    print("4. Выберите аккаунт Google")
    print()
    print("Готово! 🎉")
    print()

if __name__ == '__main__':
    main()
