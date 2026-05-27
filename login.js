// API URL
const API_URL = 'http://localhost:5000/api';

// Form elements
const loginForm = document.getElementById('loginForm');
const loginEmail = document.getElementById('loginEmail');
const loginPassword = document.getElementById('loginPassword');
const remember = document.getElementById('remember');

// Error messages
const errors = {
  loginEmail: document.getElementById('loginEmailError'),
  loginPassword: document.getElementById('loginPasswordError')
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

  if (!loginEmail.value.trim()) {
    showError('loginEmail', 'Введите email');
    isValid = false;
  } else if (!isValidEmail(loginEmail.value)) {
    showError('loginEmail', 'Некорректный email');
    isValid = false;
  } else {
    clearError('loginEmail');
  }

  if (!loginPassword.value) {
    showError('loginPassword', 'Введите пароль');
    isValid = false;
  } else {
    clearError('loginPassword');
  }

  return isValid;
}

// Handle login
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (!validateForm()) return;

  const submitBtn = loginForm.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Вход...';

  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: loginEmail.value.trim(),
        password: loginPassword.value
      })
    });

    console.log('📥 Ответ входа. Статус:', response.status);
    const data = await response.json();
    console.log('Данные ответа:', data);

    if (data.успех) {
      console.log('✅ Вход успешен! User ID:', data.user_id);
      
      // Save user data
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('username', data.username);
      localStorage.setItem('email', data.email);
      localStorage.setItem('is_logged_in', 'true');

      console.log('💾 Данные сохранены в localStorage');

      // Save remember me preference
      if (remember.checked) {
        localStorage.setItem('remember_me', 'true');
      }

      // Redirect to cabinet
      setTimeout(() => {
        window.location.href = 'cabinet.html';
      }, 500);
    } else {
      console.error('❌ Ошибка входа:', data.ошибка);
      alert('Ошибка входа: ' + data.ошибка);
    }
  } catch (error) {
    console.error('❌ Ошибка подключения:', error);
    alert('Ошибка подключения: ' + error.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Войти';
  }
});

// Load saved email if remember me was checked
window.addEventListener('load', () => {
  if (localStorage.getItem('remember_me') === 'true') {
    const savedEmail = localStorage.getItem('email');
    if (savedEmail) {
      loginEmail.value = savedEmail;
      remember.checked = true;
    }
  }
});

// ==================== GOOGLE ВХОД ====================
// Обработчик для кнопки Google
const googleBtn = document.querySelector('.btn--social');
if (googleBtn) {
  googleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    alert('⚠️ Google Sign-In требует дополнительной настройки.\n\nИспользуйте обычный вход выше - он работает отлично!');
  });
}

// ==================== СБРОС ПАРОЛЯ ====================
const forgotPasswordLink = document.getElementById('forgotPasswordLink');
if (forgotPasswordLink) {
  forgotPasswordLink.addEventListener('click', (e) => {
    e.preventDefault();
    
    const email = prompt('Введите ваш email для сброса пароля:');
    
    if (!email) {
      return;
    }
    
    if (!isValidEmail(email)) {
      alert('❌ Некорректный email');
      return;
    }
    
    // Отправить запрос на сброс пароля
    fetch('http://localhost:5000/api/reset-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.успех) {
        alert('✅ ' + data.сообщение + '\n\nНовый пароль: ' + data.новый_пароль + '\n\nПожалуйста, измените его после входа!');
      } else {
        alert('❌ Ошибка: ' + data.ошибка);
      }
    })
    .catch(error => {
      alert('❌ Ошибка подключения: ' + error.message);
    });
  });
}
