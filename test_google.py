#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

API_URL = 'http://localhost:5000/api'

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def test_google_registration():
    """Тестировать регистрацию через Google"""
    print_header("🧪 ТЕСТ РЕГИСТРАЦИИ ЧЕРЕЗ GOOGLE")
    
    try:
        # Данные для регистрации
        user_data = {
            'username': 'Google User',
            'email': 'googleuser@example.com',
            'google_id': 'google_123456789',
            'picture': 'https://example.com/picture.jpg'
        }
        
        print(f"📤 Отправка запроса регистрации Google...")
        print(f"   Email: {user_data['email']}")
        print(f"   Google ID: {user_data['google_id']}")
        
        response = requests.post(
            f'{API_URL}/register-google',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 Ответ получен. Статус: {response.status_code}")
        data = response.json()
        print(f"   Ответ: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('успех'):
            print(f"✅ Регистрация Google успешна!")
            user_id = data.get('user_id')
            return user_id
        else:
            print(f"❌ Ошибка регистрации: {data.get('ошибка')}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_google_login():
    """Тестировать вход через Google"""
    print_header("🧪 ТЕСТ ВХОДА ЧЕРЕЗ GOOGLE")
    
    try:
        # Данные для входа
        login_data = {
            'email': 'googleuser@example.com',
            'google_id': 'google_123456789'
        }
        
        print(f"📤 Отправка запроса входа Google...")
        print(f"   Email: {login_data['email']}")
        print(f"   Google ID: {login_data['google_id']}")
        
        response = requests.post(
            f'{API_URL}/login-google',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 Ответ получен. Статус: {response.status_code}")
        data = response.json()
        print(f"   Ответ: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('успех'):
            print(f"✅ Вход Google успешен!")
            return True
        else:
            print(f"❌ Ошибка входа: {data.get('ошибка')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_regular_registration():
    """Тестировать обычную регистрацию"""
    print_header("🧪 ТЕСТ ОБЫЧНОЙ РЕГИСТРАЦИИ")
    
    try:
        # Данные для регистрации
        user_data = {
            'username': 'Test User',
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        
        print(f"📤 Отправка запроса регистрации...")
        print(f"   Email: {user_data['email']}")
        print(f"   Username: {user_data['username']}")
        
        response = requests.post(
            f'{API_URL}/register',
            json=user_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 Ответ получен. Статус: {response.status_code}")
        data = response.json()
        print(f"   Ответ: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('успех'):
            print(f"✅ Регистрация успешна!")
            return data.get('user_id')
        else:
            print(f"❌ Ошибка регистрации: {data.get('ошибка')}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_regular_login():
    """Тестировать обычный вход"""
    print_header("🧪 ТЕСТ ОБЫЧНОГО ВХОДА")
    
    try:
        # Данные для входа
        login_data = {
            'email': 'testuser@example.com',
            'password': 'TestPassword123'
        }
        
        print(f"📤 Отправка запроса входа...")
        print(f"   Email: {login_data['email']}")
        
        response = requests.post(
            f'{API_URL}/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 Ответ получен. Статус: {response.status_code}")
        data = response.json()
        print(f"   Ответ: {json.dumps(data, ensure_ascii=False, indent=2)}")
        
        if data.get('успех'):
            print(f"✅ Вход успешен!")
            return True
        else:
            print(f"❌ Ошибка входа: {data.get('ошибка')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║                  🧪 ТЕСТИРОВАНИЕ GOOGLE SIGN-IN 🧪                       ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    
    # Проверка доступности сервера
    print_header("🔍 ПРОВЕРКА ДОСТУПНОСТИ СЕРВЕРА")
    try:
        response = requests.get(f'{API_URL}/stats', timeout=5)
        print(f"✅ Сервер доступен на {API_URL}")
        print(f"   Статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Сервер недоступен!")
        print(f"   Ошибка: {e}")
        print(f"\n   Убедитесь что запущен: python app.py")
        return
    
    # Тесты
    print("\n")
    test_regular_registration()
    test_regular_login()
    test_google_registration()
    test_google_login()
    
    # Итоги
    print_header("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("Если все тесты прошли успешно - система готова к использованию!")
    print("\n")

if __name__ == '__main__':
    main()
