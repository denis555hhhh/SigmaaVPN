#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

print("Проверка app.py...")
print(f"Размер файла: {os.path.getsize('app.py')} байт")

try:
    print("Импортирую Flask...")
    from flask import Flask
    print("✓ Flask импортирован")
    
    print("Импортирую app...")
    from app import app
    print("✓ app импортирован")
    
    print("Проверяю маршруты...")
    for rule in app.url_map.iter_rules():
        print(f"  - {rule.rule} ({rule.methods})")
    
    print("\n✓ Все хорошо! Сервер готов к запуску.")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
