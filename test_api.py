#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

API_URL = 'http://localhost:5000/api'

def test_api():
    """Тестировать API endpoints"""
    
    print("\n" + "="*60)
    print("🧪 Тестирование SigmaVPN API")
    print("="*60 + "\n")
    
    # Проверка доступности сервера
    print("[1/5] Проверка доступности сервера...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print("✓ Сервер доступен\n")
    except:
        print("❌ Сервер недоступен!")
        print("Убедитесь, что запущен app.py\n")
        return
    
    # Тест регистрации
    print("[2/5] Тест регистрации...")
    test_user = {
        "username": "TestUser",
        "email": f"test{int(time.time())}@example.com",
        "password": "TestPassword123"
    }
    
    try:
        response = requests.post(f'{API_URL}/register', json=test_user)
        data = response.json()
        
        if data.get('успех'):
            user_id = data.get('user_id')
            print(f"✓ Регистрация успешна!")
            print(f"  User ID: {user_id}")
            print(f"  Email: {test_user['email']}\n")
        else:
            print(f"❌ Ошибка: {data.get('ошибка')}\n")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}\n")
        return
    
    # Тест входа
    print("[3/5] Тест входа...")
    try:
        response = requests.post(f'{API_URL}/login', json={
            "email": test_user['email'],
            "password": test_user['password']
        })
        data = response.json()
        
        if data.get('успех'):
            print(f"✓ Вход успешен!")
            print(f"  Username: {data.get('username')}\n")
        else:
            print(f"❌ Ошибка: {data.get('ошибка')}\n")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}\n")
    
    # Тест создания подписки
    print("[4/5] Тест создания подписки...")
    try:
        response = requests.post(f'{API_URL}/subscription', json={
            "user_id": user_id,
            "plan": "Стандарт"
        })
        data = response.json()
        
        if data.get('успех'):
            print(f"✓ Подписка создана!")
            print(f"  План: {data.get('план')}")
            print(f"  Начало: {data.get('начало')}")
            print(f"  Конец: {data.get('конец')}\n")
        else:
            print(f"❌ Ошибка: {data.get('ошибка')}\n")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}\n")
    
    # Тест получения профиля
    print("[5/5] Тест получения профиля...")
    try:
        response = requests.get(f'{API_URL}/profile/{user_id}')
        data = response.json()
        
        if data.get('успех'):
            user = data.get('пользователь', {})
            sub = data.get('подписка', {})
            print(f"✓ Профиль получен!")
            print(f"  Email: {user.get('email')}")
            print(f"  Username: {user.get('username')}")
            if sub:
                print(f"  Подписка: {sub.get('план')} ({sub.get('статус')})\n")
        else:
            print(f"❌ Ошибка: {data.get('ошибка')}\n")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}\n")
    
    # Тест статистики
    print("Бонус: Получение статистики...")
    try:
        response = requests.get(f'{API_URL}/stats')
        data = response.json()
        
        if data.get('успех'):
            stats = data.get('статистика', {})
            print(f"✓ Статистика:")
            print(f"  Пользователей: {stats.get('пользователей')}")
            print(f"  Активных подписок: {stats.get('активных_подписок')}")
            print(f"  Логов: {stats.get('логов')}\n")
    except Exception as e:
        print(f"❌ Ошибка: {e}\n")
    
    print("="*60)
    print("✓ Тестирование завершено!")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\n⚠️  Тестирование прервано пользователем")
