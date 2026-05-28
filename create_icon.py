#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Создание иконки со щитком для приложения
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Создать иконку со щитком"""
    print("🎨 Создание иконки со щитком...")
    
    # Размеры
    size = 256
    
    # Создать изображение
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Цвета
    shield_color = '#00d4ff'  # Голубой
    shield_dark = '#0099cc'   # Тёмный голубой
    text_color = '#ffffff'    # Белый
    
    # Рисовать щиток
    # Основной щиток
    shield_points = [
        (size * 0.2, size * 0.15),      # Верхний левый
        (size * 0.8, size * 0.15),      # Верхний правый
        (size * 0.8, size * 0.5),       # Правый середина
        (size * 0.5, size * 0.85),      # Нижний центр
        (size * 0.2, size * 0.5),       # Левый середина
    ]
    
    # Рисовать щиток
    draw.polygon(shield_points, fill=shield_color, outline=shield_dark)
    
    # Рисовать внутренний щиток (для эффекта)
    inner_points = [
        (size * 0.25, size * 0.2),
        (size * 0.75, size * 0.2),
        (size * 0.75, size * 0.48),
        (size * 0.5, size * 0.78),
        (size * 0.25, size * 0.48),
    ]
    draw.polygon(inner_points, fill='#00ffff', outline=shield_color)
    
    # Рисовать галочку внутри щитка
    check_x = size * 0.5
    check_y = size * 0.5
    check_size = size * 0.15
    
    # Вертикальная линия галочки
    draw.line([
        (check_x - check_size * 0.3, check_y),
        (check_x - check_size * 0.1, check_y + check_size * 0.2),
        (check_x + check_size * 0.3, check_y - check_size * 0.2)
    ], fill=shield_dark, width=int(size * 0.03))
    
    # Сохранить иконку
    icon_path = 'shield_icon.png'
    img.save(icon_path, 'PNG')
    print(f"✅ Иконка создана: {icon_path}")
    
    # Создать ICO файл для Windows
    try:
        # Создать разные размеры
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        
        for size_tuple in sizes:
            resized = img.resize(size_tuple, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # Сохранить как ICO
        icons[0].save('shield_icon.ico', 'ICO', sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]])
        print("✅ ICO файл создан: shield_icon.ico")
        
    except Exception as e:
        print(f"⚠️  Ошибка при создании ICO: {e}")
        print("📝 Используйте PNG файл вместо этого")

if __name__ == '__main__':
    create_icon()
