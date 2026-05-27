// API URL
const API_URL = 'http://localhost:5000/api';

// Form elements
const regForm = document.getElementById('regForm');
const regName = document.getElementById('regName');
const regEmail = document.getElementById('regEmail');
const regPassword = document.getElementById('regPassword');
const regPasswordConfirm = document.getElementById('regPasswordConfirm');
const regAgree = document.getElementById('regAgree');

// Steps
const stepOne = document.getElementById('stepOne');
const stepTwo = document.getElementById('stepTwo');
const stepThree = document.getElementById('stepThree');

// Buttons
const toStep2 = document.getElementById('toStep2');
const backToStep1 = document.getElementById('backToStep1');
const toStep3 = document.getElementById('toStep3');

// Step indicators
const step1Dot = document.getElementById('step1-dot');
const step2Dot = document.getElementById('step2-dot');
const step3Dot = document.getElementById('step3-dot');

// Password strength
const passBar = document.getElementById('passBar');
const passLabel = document.getElementById('passLabel');
const togglePass = document.getElementById('togglePass');

// Error messages
const errors = {
  regName: document.getElementById('regNameError'),
  regEmail: document.getElementById('regEmailError'),
  regPassword: document.getElementById('regPasswordError'),
  regPasswordConfirm: document.getElementById('regPasswordConfirmError'),
  regAgree: document.getElementById('regAgreeError')
};

// Validate email
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Check password strength
function checkPasswordStrength(password) {
  let strength = 0;
  if (password.length >= 8) strength++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  if (/\d/.test(password)) strength++;
  if (/[^a-zA-Z\d]/.test(password)) strength++;

  const colors = ['#ff4757', '#ffa502', '#ffd93d', '#6bcf7f'];
  const labels = ['Слабый', 'Средний', 'Хороший', 'Сильный'];

  passBar.style.width = (strength * 25) + '%';
  passBar.style.backgroundColor = colors[strength - 1] || '#ddd';
  passLabel.textContent = labels[strength - 1] || '';
}

// Show error
function showError(field, message) {
  if (errors[field]) {
    errors[field].textContent = message;
  }
}

// Clear error
function clearError(field) {
  if (errors[field]) {
    errors[field].textContent = '';
  }
}

// Validate step 1
function validateStep1() {
  let isValid = true;

  if (!regName.value.trim()) {
    showError('regName', 'Введите имя');
    isValid = false;
  } else {
    clearError('regName');
  }

  if (!regEmail.value.trim()) {
    showError('regEmail', 'Введите email');
    isValid = false;
  } else if (!isValidEmail(regEmail.value)) {
    showError('regEmail', 'Некорректный email');
    isValid = false;
  } else {
    clearError('regEmail');
  }

  if (!regPassword.value) {
    showError('regPassword', 'Введите пароль');
    isValid = false;
  } else if (regPassword.value.length < 8) {
    showError('regPassword', 'Пароль должен быть минимум 8 символов');
    isValid = false;
  } else {
    clearError('regPassword');
  }

  if (regPassword.value !== regPasswordConfirm.value) {
    showError('regPasswordConfirm', 'Пароли не совпадают');
    isValid = false;
  } else {
    clearError('regPasswordConfirm');
  }

  return isValid;
}

// Validate step 2
function validateStep2() {
  if (!regAgree.checked) {
    showError('regAgree', 'Примите условия использования');
    return false;
  }
  clearError('regAgree');
  return true;
}

// Go to step 2
toStep2.addEventListener('click', () => {
  if (validateStep1()) {
    stepOne.style.display = 'none';
    stepTwo.style.display = 'block';
    step1Dot.classList.remove('active');
    step2Dot.classList.add('active');
  }
});

// Back to step 1
backToStep1.addEventListener('click', () => {
  stepTwo.style.display = 'none';
  stepOne.style.display = 'block';
  step1Dot.classList.add('active');
  step2Dot.classList.remove('active');
});

// Register user
toStep3.addEventListener('click', async () => {
  if (!validateStep2()) return;

  toStep3.disabled = true;
  toStep3.textContent = 'Регистрация...';

  try {
    const username = regName.value.trim();
    const email = regEmail.value.trim();
    const password = regPassword.value;
    const selectedPlan = document.querySelector('input[name="plan"]:checked').value;
    
    const planMap = {
      'basic': 'Базовый',
      'standard': 'Стандарт',
      'premium': 'Премиум'
    };

    console.log('📤 Отправка запроса регистрации...');
    console.log('API URL: http://localhost:5000/api');
    console.log('Данные:', { username, email, plan: planMap[selectedPlan] });

    // Регистрация
    const regResponse = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password
      })
    });

    console.log('📥 Ответ получен. Статус:', regResponse.status);
    const regData = await regResponse.json();
    console.log('Данные ответа:', regData);

    if (!regData.успех) {
      console.error('❌ Ошибка регистрации:', regData.ошибка);
      alert('Ошибка регистрации: ' + regData.ошибка);
      toStep3.disabled = false;
      toStep3.textContent = 'Зарегистрироваться';
      return;
    }

    console.log('✅ Регистрация успешна! User ID:', regData.user_id);
    const userId = regData.user_id;

    // Создание подписки
    console.log('📤 Создание подписки...');
    const subResponse = await fetch('http://localhost:5000/api/subscription', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        plan: planMap[selectedPlan]
      })
    });

    console.log('📥 Ответ подписки. Статус:', subResponse.status);
    const subData = await subResponse.json();
    console.log('Данные подписки:', subData);

    if (!subData.успех) {
      console.error('❌ Ошибка подписки:', subData.ошибка);
      alert('Ошибка создания подписки: ' + subData.ошибка);
      toStep3.disabled = false;
      toStep3.textContent = 'Зарегистрироваться';
      return;
    }

    console.log('✅ Подписка создана! Subscription ID:', subData.subscription_id);

    // Сохранение данных
    localStorage.setItem('user_id', userId);
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('subscription_id', subData.subscription_id);
    localStorage.setItem('plan', planMap[selectedPlan]);

    console.log('💾 Данные сохранены в localStorage');
    console.log('Сохранённые данные:', {
      user_id: userId,
      username: username,
      email: email,
      subscription_id: subData.subscription_id,
      plan: planMap[selectedPlan]
    });

    // Показ успеха
    stepTwo.style.display = 'none';
    stepThree.style.display = 'block';
    step2Dot.classList.remove('active');
    step3Dot.classList.add('active');

    document.getElementById('successMsg').textContent = 
      `Добро пожаловать, ${username}!`;

    console.log('🎉 Регистрация завершена успешно!');

    // Перенаправление в личный кабинет
    setTimeout(() => {
      window.location.href = 'cabinet.html';
    }, 2000);

  } catch (error) {
    console.error('❌ Ошибка:', error);
    console.error('Сообщение:', error.message);
    console.error('Stack:', error.stack);
    alert('Ошибка: ' + error.message + '\n\nОткройте консоль (F12) для подробностей');
    toStep3.disabled = false;
    toStep3.textContent = 'Зарегистрироваться';
  }
});

// Password strength check
regPassword.addEventListener('input', () => {
  checkPasswordStrength(regPassword.value);
});

// Toggle password visibility
togglePass.addEventListener('click', (e) => {
  e.preventDefault();
  const type = regPassword.type === 'password' ? 'text' : 'password';
  regPassword.type = type;
  togglePass.textContent = type === 'password' ? '👁' : '👁‍🗨';
});

// ==================== ПЛАН ВЫБОР ====================
// Обработчик для переключения между тарифами
document.querySelectorAll('.reg-plan').forEach(plan => {
  plan.addEventListener('click', (e) => {
    // Убрать активный класс со всех
    document.querySelectorAll('.reg-plan').forEach(p => {
      p.classList.remove('selected');
    });
    
    // Добавить активный класс текущему
    plan.classList.add('selected');
    
    // Отметить radio button
    const radio = plan.querySelector('input[type="radio"]');
    if (radio) {
      radio.checked = true;
    }
  });
});

// Установить начальный выбор (Стандарт)
document.getElementById('planStandard').classList.add('selected');

// ==================== GOOGLE ВХОД ====================
// Обработчик для кнопки Google
const googleBtn = document.querySelector('.btn--social');
if (googleBtn) {
  googleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('⚠️ Google Sign-In требует дополнительной настройки.\n\nИспользуйте обычную регистрацию выше - она работает отлично!');
  });
}
