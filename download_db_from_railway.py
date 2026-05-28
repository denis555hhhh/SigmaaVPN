#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для скачивания БД с Railway
"""

import os
import shutil
from pathlib import Path

def download_db():
    """Скачать БД с Railway"""
    print("📥 Скачивание БД с Railway...")
    print("=" * 50)
    
    # Пути
    railway_db = "sigmavpn.db"
    local_db = "sigmavpn.db"
    backup_db = "sigmavpn_backup.db"
    
    # Проверить, существует ли БД
    if os.path.exists(railway_db):
        print(f"✅ БД найдена: {railway_db}")
        print(f"📊 Размер: {os.path.getsize(railway_db) / 1024 / 1024:.2f} MB")
        
        # Создать резервную копию
        if os.path.exists(local_db):
            shutil.copy(local_db, backup_db)
            print(f"💾 Резервная копия создана: {backup_db}")
        
        # Скопировать БД
        shutil.copy(railway_db, local_db)
        print(f"✅ БД скопирована: {local_db}")
        print("=" * 50)
        print("✨ БД готова к использованию!")
        print(f"📁 Откройте панель управления: SigmaVPN_Bot_Admin.exe")
        
    else:
        print("❌ БД не найдена!")
        print("Убедитесь, что файл sigmavpn.db находится в этой папке")
        print("=" * 50)
        print("\n📝 ИНСТРУКЦИЯ:")
        print("1. Откройте Railway Dashboard")
        print("2. Откройте сервис (web или worker)")
        print("3. Найдите файл sigmavpn.db")
        print("4. Скачайте его в эту папку")
        print("5. Запустите этот скрипт снова")

if __name__ == '__main__':
    download_db()
    input("\nНажмите Enter для выхода...")
