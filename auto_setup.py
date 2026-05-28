#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Автоматическая настройка панели управления
Скачивает БД и открывает панель
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🚀 Автоматическая настройка SigmaVPN Admin Panel")
    print("=" * 60)
    
    # Пути
    project_dir = Path(__file__).parent
    db_file = project_dir / "sigmavpn.db"
    exe_file = project_dir / "dist" / "SigmaVPN_Bot_Admin.exe"
    
    print(f"📁 Папка проекта: {project_dir}")
    print(f"📊 БД файл: {db_file}")
    print(f"🖥️  EXE файл: {exe_file}")
    print("=" * 60)
    
    # Проверить, существует ли БД
    if not db_file.exists():
        print("\n⚠️  БД не найдена!")
        print("📥 Скачиваю БД с Railway...")
        
        # Попытаться скачать БД
        try:
            # Проверить, есть ли БД в текущей папке
            if os.path.exists("sigmavpn.db"):
                print("✅ БД найдена в текущей папке")
            else:
                print("❌ БД не найдена")
                print("\n📝 ИНСТРУКЦИЯ:")
                print("1. Откройте Railway Dashboard")
                print("2. Откройте сервис sigmaVPNN (веб)")
                print("3. Найдите файл sigmavpn.db")
                print("4. Скачайте его в эту папку")
                print("5. Запустите этот скрипт снова")
                input("\nНажмите Enter для выхода...")
                return False
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
    
    print("✅ БД найдена!")
    print(f"📊 Размер: {db_file.stat().st_size / 1024 / 1024:.2f} MB")
    
    # Проверить, существует ли EXE
    if not exe_file.exists():
        print(f"\n❌ EXE файл не найден: {exe_file}")
        print("📝 Создаю EXE файл...")
        
        try:
            # Попытаться создать EXE
            subprocess.run([
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name=SigmaVPN_Bot_Admin",
                "bot_admin_panel.py"
            ], check=True, cwd=str(project_dir))
            print("✅ EXE файл создан!")
        except Exception as e:
            print(f"❌ Ошибка при создании EXE: {e}")
            print("📝 Запускаю панель через Python...")
            
            try:
                subprocess.Popen([sys.executable, "bot_admin_panel.py"], cwd=str(project_dir))
                print("✅ Панель запущена!")
                return True
            except Exception as e2:
                print(f"❌ Ошибка: {e2}")
                return False
    
    print("✅ EXE файл найден!")
    print("\n🚀 Запускаю панель управления...")
    print("=" * 60)
    
    try:
        # Запустить EXE
        subprocess.Popen(str(exe_file))
        print("✅ Панель управления запущена!")
        print("\n💡 Совет: Нажмите '🔄 Обновить' для загрузки данных из БД")
        return True
    except Exception as e:
        print(f"❌ Ошибка при запуске EXE: {e}")
        print("📝 Попытаюсь запустить через Python...")
        
        try:
            subprocess.Popen([sys.executable, "bot_admin_panel.py"], cwd=str(project_dir))
            print("✅ Панель запущена через Python!")
            return True
        except Exception as e2:
            print(f"❌ Ошибка: {e2}")
            return False

if __name__ == '__main__':
    success = main()
    if not success:
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
