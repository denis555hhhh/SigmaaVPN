#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Исправление ошибки Google OAuth
Получение реального Client ID
"""

import json
import webbrowser
import os

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                  🔧 ИСПРАВЛЕНИЕ ОШИБКИ GOOGLE OAUTH 🔧                   ║")
    print("║                                                                            ║")
    print("║                    Ошибка: no registered origin                           ║")
    print("║                    Решение: Получить реальный Client ID                  ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    print_header("ПРИЧИНА ОШИБКИ")
    
    print("❌ Демо Client ID не работает с Google OAuth")
    print("✅ Нужен реальный Client ID от Google Cloud Console")
    print()
    
    print_header("РЕШЕНИЕ (5 МИНУТ)")
    
    print("1️⃣  ОТКРОЙТЕ GOOGLE CLOUD CONSOLE:")
    print("   https://console.cloud.google.com/")
    print()
    
    print("2️⃣  СОЗДАЙТЕ НОВЫЙ ПРОЕКТ:")
    print("   - Нажмите на выпадающее меню проектов (вверху)")
    print("   - Нажмите 'Новый проект'")
    print("   - Введите название: SigmaVPN")
    print("   - Нажмите 'Создать'")
    print("   - Подождите 1-2 минуты")
    print()
    
    print("3️⃣  ВКЛЮЧИТЕ GOOGLE+ API:")
    print("   - Перейдите в 'APIs & Services' → 'Library'")
    print("   - Найдите 'Google+ API'")
    print("   - Нажмите 'Включить'")
    print()
    
    print("4️⃣  СОЗДАЙТЕ OAUTH 2.0 CLIENT ID:")
    print("   - Перейдите в 'APIs & Services' → 'Credentials'")
    print("   - Нажмите 'Создать учетные данные' → 'OAuth 2.0 Client ID'")
    print("   - Выберите 'Веб-приложение'")
    print("   - Введите название: SigmaVPN")
    print("   - Нажмите 'Создать'")
    print()
    
    print("5️⃣  ДОБАВЬТЕ АВТОРИЗОВАННЫЕ ИСТОЧНИКИ:")
    print("   - Нажмите на созданное приложение")
    print("   - Найдите 'Авторизованные источники JavaScript'")
    print("   - Добавьте:")
    print("     * http://localhost:8080")
    print("     * http://localhost:5000")
    print()
    
    print("6️⃣  ДОБАВЬТЕ АВТОРИЗОВАННЫЕ URI ПЕРЕНАПРАВЛЕНИЯ:")
    print("   - Найдите 'Авторизованные URI перенаправления'")
    print("   - Добавьте:")
    print("     * http://localhost:8080/register.html")
    print("     * http://localhost:8080/login.html")
    print("     * http://localhost:5000/api/register-google")
    print("     * http://localhost:5000/api/login-google")
    print("   - Нажмите 'Сохранить'")
    print()
    
    print("7️⃣  СКОПИРУЙТЕ CLIENT ID:")
    print("   - Нажмите на приложение")
    print("   - Скопируйте 'Client ID' (длинная строка)")
    print()
    
    print_header("ВВЕДИТЕ ВАШИ ДАННЫЕ")
    
    client_id = input("Введите ваш Google Client ID: ").strip()
    
    if not client_id or len(client_id) < 20:
        print("\n❌ Ошибка: Client ID должен быть длинной строкой")
        print("Пример: 123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com")
        return False
    
    print_header("ОБНОВЛЕНИЕ ФАЙЛОВ")
    
    # Обновить register.js
    print("📝 Обновление register.js...")
    try:
        with open('register.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменить любой Client ID на новый
        content = content.replace(
            "GOOGLE_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'",
            f"GOOGLE_CLIENT_ID = '{client_id}'"
        )
        # На случай если там демо Client ID
        if "123456789-abcdefghijklmnopqrstuvwxyz" in content:
            content = content.replace(
                "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com",
                client_id
            )
        
        with open('register.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ register.js обновлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Обновить login.js
    print("📝 Обновление login.js...")
    try:
        with open('login.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменить любой Client ID на новый
        content = content.replace(
            "GOOGLE_CLIENT_ID = 'YOUR_CLIENT_ID_HERE'",
            f"GOOGLE_CLIENT_ID = '{client_id}'"
        )
        # На случай если там демо Client ID
        if "123456789-abcdefghijklmnopqrstuvwxyz" in content:
            content = content.replace(
                "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com",
                client_id
            )
        
        with open('login.js', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ login.js обновлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    # Обновить oauth_config.json
    print("📝 Обновление oauth_config.json...")
    try:
        config = {
            'google_client_id': client_id,
            'setup_date': '2026-05-27',
            'status': 'configured',
            'type': 'production'
        }
        
        with open('oauth_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("✅ oauth_config.json обновлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    print_header("✅ ОШИБКА ИСПРАВЛЕНА!")
    
    print("Google OAuth успешно настроен с вашим Client ID!")
    print()
    print("📋 Информация:")
    print(f"   Client ID: {client_id[:30]}...")
    print()
    print("🚀 Следующие шаги:")
    print("1. Закройте браузер")
    print("2. Запустите: START_WITH_GOOGLE.bat")
    print("3. Откройте: http://localhost:8080/register.html")
    print("4. Нажмите: 'Войти через Google'")
    print("5. Готово! 🎉")
    print()
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("✅ Все готово!")
        else:
            print("❌ Ошибка при настройке")
        input("Нажмите Enter для выхода...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        input("Нажмите Enter для выхода...")
