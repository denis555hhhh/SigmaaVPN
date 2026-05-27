// ==================== ИНИЦИАЛИЗАЦИЯ ====================
document.addEventListener('DOMContentLoaded', () => {
  // Проверить авторизацию
  const userId = localStorage.getItem('user_id');
  const username = localStorage.getItem('username');
  const email = localStorage.getItem('email');

  if (!userId) {
    // Если не авторизован, перенаправить на вход
    window.location.href = 'login.html';
    return;
  }

  // Загрузить данные профиля
  loadProfile();
  loadSubscription();
});

// ==================== ЗАГРУЗКА ПРОФИЛЯ ====================
async function loadProfile() {
  try {
    const username = localStorage.getItem('username');
    const email = localStorage.getItem('email');

    document.getElementById('cabUsername').textContent = username || 'Пользователь';
    document.getElementById('cabEmail').textContent = email || 'email@example.com';
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error);
  }
}

// ==================== ЗАГРУЗКА ПОДПИСКИ ====================
async function loadSubscription() {
  try {
    const userId = localStorage.getItem('user_id');
    const plan = localStorage.getItem('plan') || 'Стандарт';
    const subscriptionId = localStorage.getItem('subscription_id');

    document.getElementById('subPlan').textContent = plan;
    document.getElementById('subStatus').textContent = 'Активна';

    // Определить преимущества по тарифу
    const benefits = {
      'Базовый': ['1 устройство', '16 стран', 'Базовая скорость'],
      'Стандарт': ['3 устройства', '16 стран', 'Высокая скорость'],
      'Премиум': ['6 устройств', '16 стран', 'Максимальная скорость']
    };

    const planBenefits = benefits[plan] || benefits['Стандарт'];
    document.getElementById('benefit1').textContent = '✓ ' + planBenefits[0];
    document.getElementById('benefit2').textContent = '✓ ' + planBenefits[1];
    document.getElementById('benefit3').textContent = '✓ ' + planBenefits[2];

    // Установить даты (примерно)
    const startDate = new Date();
    const endDate = new Date();
    
    if (plan === 'Премиум') {
      endDate.setFullYear(endDate.getFullYear() + 1);
    } else {
      endDate.setMonth(endDate.getMonth() + 1);
    }

    document.getElementById('subStart').textContent = startDate.toLocaleDateString('ru-RU');
    document.getElementById('subEnd').textContent = endDate.toLocaleDateString('ru-RU');
  } catch (error) {
    console.error('Ошибка загрузки подписки:', error);
  }
}

// ==================== НАВИГАЦИЯ ПО ТАБАМ ====================
document.querySelectorAll('.cabinet-nav__item').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();

    // Убрать активный класс со всех
    document.querySelectorAll('.cabinet-nav__item').forEach(i => {
      i.classList.remove('active');
    });
    document.querySelectorAll('.cabinet-tab').forEach(tab => {
      tab.classList.remove('active');
    });

    // Добавить активный класс текущему
    item.classList.add('active');
    const tabName = item.getAttribute('data-tab');
    document.getElementById(`tab-${tabName}`).classList.add('active');
  });
});

// ==================== ВЫХОД ====================
// Функция выхода удалена

// ==================== РЕДАКТИРОВАНИЕ ПРОФИЛЯ ====================
document.getElementById('editProfileBtn').addEventListener('click', () => {
  alert('⚠️ Функция редактирования профиля будет доступна в ближайшее время');
});

// ==================== СОХРАНЕНИЕ НАСТРОЕК ====================
document.getElementById('settingsForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const newPassword = document.getElementById('settingsPassword').value;
  const confirmPassword = document.getElementById('settingsPasswordConfirm').value;

  if (!newPassword) {
    alert('Введите новый пароль');
    return;
  }

  if (newPassword !== confirmPassword) {
    alert('Пароли не совпадают');
    return;
  }

  if (newPassword.length < 8) {
    alert('Пароль должен быть минимум 8 символов');
    return;
  }

  try {
    const userId = localStorage.getItem('user_id');
    const response = await fetch('http://localhost:5000/api/change-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        new_password: newPassword
      })
    });

    const data = await response.json();

    if (data.успех) {
      alert('✅ Пароль успешно изменён!');
      document.getElementById('settingsForm').reset();
    } else {
      alert('❌ Ошибка: ' + data.ошибка);
    }
  } catch (error) {
    alert('❌ Ошибка подключения: ' + error.message);
  }
});
