// API URL
const API_URL = 'http://localhost:5000/api';

// Form elements
const checkoutForm = document.getElementById('checkoutForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const agreeCheckbox = document.getElementById('agree');

// Error messages
const errors = {
  email: document.getElementById('emailError'),
  password: document.getElementById('passwordError')
};

// FunPay redirect URLs
const FUNPAY_URLS = {
  'Базовый': 'https://funpay.com/lots/offer?id=69831732',
  'Стандарт': 'https://funpay.com/lots/offer?id=69831833',
  'Премиум': 'https://funpay.com/lots/offer?id=69832017'
};

// Validate email
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
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

// Validate form
function validateForm() {
  let isValid = true;

  if (!emailInput.value.trim()) {
    showError('email', 'Введите email');
    isValid = false;
  } else if (!isValidEmail(emailInput.value)) {
    showError('email', 'Некорректный email');
    isValid = false;
  } else {
    clearError('email');
  }

  if (!passwordInput.value) {
    showError('password', 'Введите пароль');
    isValid = false;
  } else if (passwordInput.value.length < 8) {
    showError('password', 'Пароль должен быть минимум 8 символов');
    isValid = false;
  } else {
    clearError('password');
  }

  if (!agreeCheckbox.checked) {
    showError('email', 'Примите условия использования');
    isValid = false;
  }

  return isValid;
}

// Get selected plan
function getSelectedPlan() {
  const planElement = document.getElementById('orderPlan');
  const planName = planElement.querySelector('.order-plan__name').textContent;
  return planName;
}

// Handle checkout
checkoutForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (!validateForm()) return;

  const submitBtn = checkoutForm.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Обработка...';

  try {
    // Step 1: Register user
    const registerResponse = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: emailInput.value.split('@')[0],
        email: emailInput.value.trim(),
        password: passwordInput.value
      })
    });

    const registerData = await registerResponse.json();

    if (!registerData.успех) {
      showError('email', registerData.ошибка || 'Ошибка регистрации');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Оплатить и начать';
      return;
    }

    const userId = registerData.user_id;
    const selectedPlan = getSelectedPlan();

    // Step 2: Create subscription
    const subscriptionResponse = await fetch(`${API_URL}/subscription`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        plan: selectedPlan
      })
    });

    const subscriptionData = await subscriptionResponse.json();

    if (!subscriptionData.успех) {
      showError('email', subscriptionData.ошибка || 'Ошибка создания подписки');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Оплатить и начать';
      return;
    }

    // Save user data to localStorage
    localStorage.setItem('user_id', userId);
    localStorage.setItem('username', registerData.username);
    localStorage.setItem('email', emailInput.value);
    localStorage.setItem('subscription_id', subscriptionData.subscription_id);
    localStorage.setItem('plan', selectedPlan);
    localStorage.setItem('is_logged_in', 'true');

    // Step 3: Redirect to FunPay
    const funpayUrl = FUNPAY_URLS[selectedPlan];
    if (funpayUrl) {
      window.location.href = funpayUrl;
    } else {
      showError('email', 'Ошибка: неизвестный тариф');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Оплатить и начать';
    }
  } catch (error) {
    console.error('Ошибка:', error);
    showError('email', 'Ошибка подключения к серверу');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Оплатить и начать';
  }
});

// Update order summary based on URL parameters
window.addEventListener('load', () => {
  const params = new URLSearchParams(window.location.search);
  const plan = params.get('plan');

  if (plan) {
    const planMap = {
      'basic': { name: 'Базовый', price: '99 ₽/мес', features: ['✓ 1 устройство', '✓ 10 стран', '✓ 512 Мбит/с', '✓ Kill Switch'] },
      'standard': { name: 'Стандарт', price: '199 ₽/мес', features: ['✓ 3 устройства', '✓ 60 стран', '✓ 1 Гбит/с', '✓ Kill Switch'] },
      'premium': { name: 'Премиум', price: '399 ₽/мес', features: ['✓ Неограниченные устройства', '✓ 150+ стран', '✓ 10 Гбит/с', '✓ Kill Switch', '✓ Приоритет'] }
    };

    if (planMap[plan]) {
      const planData = planMap[plan];
      document.querySelector('.order-plan__name').textContent = planData.name;
      document.querySelector('.order-plan__price').textContent = planData.price;
      document.getElementById('orderTotal').textContent = planData.price;

      const featuresList = document.getElementById('orderFeatures');
      featuresList.innerHTML = planData.features.map(f => `<li>${f}</li>`).join('');
    }
  }
});
