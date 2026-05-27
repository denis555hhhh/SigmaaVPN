#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для обновления API URLs после развертывания на Railway
"""

import os
import re

def update_api_url(file_path, new_url):
    """Обновить API URL в файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Заменить старый URL на новый
        updated_content = re.sub(
            r"const API_URL = '[^']*'",
            f"const API_URL = '{new_url}'",
            content
        )
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
    except Exception as e:
        print(f"❌ Ошибка при обновлении {file_path}: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print("🚀 ОБНОВЛЕНИЕ API URLs ДЛЯ RAILWAY")
    print("="*70 + "\n")
    
    # Получить Railway URL
    railway_url = input("📍 Введите ваш Railway URL (например: https://sigma-production.railway.app): ").strip()
    
    if not railway_url:
        print("❌ URL не может быть пустым!")
        return
    
    if not railway_url.startswith('https://'):
        railway_url = 'https://' + railway_url
    
    # Файлы для обновления
    files_to_update = [
        'register.js',
        'login.js',
        'checkout.js',
        'cabinet.js'
    ]
    
    print(f"\n📝 Обновление API URLs на: {railway_url}\n")
    
    updated_count = 0
    for file_name in files_to_update:
        file_path = os.path.join(os.getcwd(), file_name)
        
        if os.path.exists(file_path):
            if update_api_url(file_path, railway_url):
                print(f"✅ {file_name} - обновлен")
                updated_count += 1
            else:
                print(f"ℹ️  {file_name} - уже содержит правильный URL")
        else:
            print(f"⚠️  {file_name} - файл не найден")
    
    print(f"\n{'='*70}")
    print(f"✅ Обновлено файлов: {updated_count}")
    print(f"{'='*70}\n")
    
    # Предложить закоммитить
    commit = input("💾 Закоммитить и отправить изменения? (y/n): ").strip().lower()
    
    if commit == 'y':
        print("\n📦 Добавление файлов...")
        os.system('git add .')
        
        print("💾 Создание коммита...")
        os.system('git commit -m "Update API URLs for Railway deployment"')
        
        print("🚀 Отправка на GitHub...")
        os.system('git push origin main')
        
        print("\n✅ Готово! Railway автоматически перестроит приложение!")
    
    print("\n" + "="*70)
    print("🎉 РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
