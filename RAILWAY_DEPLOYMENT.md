# 🚀 Развертывание SigmaVPN на Railway

## Шаг 1: Подготовка к развертыванию

Все необходимые файлы уже созданы:
- ✅ `Procfile` - конфигурация для запуска
- ✅ `requirements.txt` - зависимости Python
- ✅ `runtime.txt` - версия Python
- ✅ `.gitignore` - исключаемые файлы
- ✅ `app.py` - обновлен для Railway

## Шаг 2: Инициализация Git репозитория

```bash
cd "c:\Users\Gnida222\Desktop\Сайт впн"
git init
git add .
git commit -m "Initial commit: SigmaVPN website with API"
```

## Шаг 3: Создание аккаунта на Railway

1. Перейдите на https://railway.app
2. Нажмите "Sign Up" (Зарегистрироваться)
3. Выберите способ регистрации (GitHub, Google или Email)
4. Подтвердите email

## Шаг 4: Создание нового проекта на Railway

### Способ 1: Через GitHub (рекомендуется)

1. Создайте репозиторий на GitHub:
   - Перейдите на https://github.com/new
   - Назовите репозиторий: `sigmavpn-website`
   - Выберите "Public" или "Private"
   - Нажмите "Create repository"

2. Добавьте удаленный репозиторий:
```bash
git remote add origin https://github.com/YOUR_USERNAME/sigmavpn-website.git
git branch -M main
git push -u origin main
```

3. На Railway:
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub"
   - Авторизуйте GitHub
   - Выберите репозиторий `sigmavpn-website`
   - Нажмите "Deploy"

### Способ 2: Через Railway CLI

1. Установите Railway CLI:
```bash
npm install -g @railway/cli
```

2. Авторизуйтесь:
```bash
railway login
```

3. Инициализируйте проект:
```bash
railway init
```

4. Разверните:
```bash
railway up
```

## Шаг 5: Конфигурация переменных окружения

На странице проекта в Railway:

1. Перейдите в "Variables"
2. Добавьте переменные:
   - `PORT` = `5000` (автоматически)
   - `DATABASE_PATH` = `sigmavpn.db`

## Шаг 6: Проверка развертывания

1. Railway автоматически создаст URL вашего приложения
2. Откройте URL в браузере
3. Проверьте, что сайт загружается

## Шаг 7: Обновление API URL в JavaScript

Обновите файлы JavaScript для использования Railway URL:

### В `register.js`, `login.js`, `checkout.js`:

```javascript
// Вместо:
const API_URL = 'http://localhost:5000';

// Используйте:
const API_URL = 'https://your-railway-app.railway.app';
```

Или используйте относительные пути:
```javascript
const API_URL = '';  // Будет использовать текущий домен
```

## Шаг 8: Развертывание обновлений

После каждого изменения:

```bash
git add .
git commit -m "Update: описание изменений"
git push origin main
```

Railway автоматически перестроит и развернет приложение.

## 📊 Мониторинг

На странице проекта Railway вы можете:
- Просмотреть логи: "Logs"
- Проверить метрики: "Metrics"
- Управлять переменными: "Variables"
- Просмотреть домен: "Settings"

## 🔗 Полезные ссылки

- Railway документация: https://docs.railway.app
- Flask на Railway: https://docs.railway.app/guides/flask
- Переменные окружения: https://docs.railway.app/develop/variables

## ⚠️ Важные замечания

1. **База данных**: SQLite хранится локально на Railway. Для продакшена рекомендуется использовать PostgreSQL.

2. **Статические файлы**: Все HTML, CSS, JS файлы должны быть в корневой папке проекта.

3. **CORS**: Уже настроен в `app.py` для всех источников.

4. **Порт**: Railway автоматически назначает порт через переменную `PORT`.

## 🚀 Быстрый старт

```bash
# 1. Инициализация Git
git init
git add .
git commit -m "Initial commit"

# 2. Создание репозитория на GitHub и push
git remote add origin https://github.com/YOUR_USERNAME/sigmavpn-website.git
git push -u origin main

# 3. На Railway: Deploy from GitHub
# Выберите репозиторий и нажмите Deploy

# 4. Готово! Ваш сайт доступен по Railway URL
```

## 📝 Структура проекта для Railway

```
sigmavpn-website/
├── app.py                 # Flask приложение
├── Procfile              # Конфигурация запуска
├── requirements.txt      # Зависимости
├── runtime.txt          # Версия Python
├── .gitignore           # Исключаемые файлы
├── index.html           # Главная страница
├── style.css            # Стили
├── main.js              # Основной JavaScript
├── register.js          # Регистрация
├── login.js             # Вход
├── cabinet.js           # Личный кабинет
├── configurator.js      # Конфигуратор подписок
├── key-configurator.js  # Конфигуратор ключей
└── sigmavpn.db         # База данных (создается автоматически)
```

## ✅ Проверка после развертывания

1. Откройте главную страницу
2. Проверьте регистрацию
3. Проверьте вход
4. Проверьте личный кабинет
5. Проверьте конфигуратор подписок
6. Проверьте конфигуратор ключей

Если все работает - поздравляем! 🎉 Ваш сайт успешно развернут на Railway!
