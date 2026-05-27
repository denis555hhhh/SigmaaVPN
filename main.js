/* ===== MOBILE MENU ===== */
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobileMenu');
if (burger && mobileMenu) {
  burger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });
}

/* ===== LOADING SCREEN ===== */
window.addEventListener('load', () => {
  const loadingScreen = document.getElementById('loadingScreen');
  if (loadingScreen) {
    setTimeout(() => {
      loadingScreen.classList.add('hidden');
    }, 3500);
  }
});

/* ===== FAQ ACCORDION ===== */
document.querySelectorAll('.faq__q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq__item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq__item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});

/* ===== BILLING TOGGLE (pricing page) ===== */
const billingToggle = document.getElementById('billingToggle');
if (billingToggle) {
  const prices = document.querySelectorAll('.price-num[data-monthly]');
  const notes = {
    basic: document.getElementById('note-basic'),
    standard: document.getElementById('note-standard'),
    premium: document.getElementById('note-premium'),
  };
  const labelMonthly = document.getElementById('labelMonthly');
  const labelYearly = document.getElementById('labelYearly');

  billingToggle.addEventListener('change', () => {
    const isYearly = billingToggle.checked;
    prices.forEach(el => {
      el.textContent = isYearly ? el.dataset.yearly : el.dataset.monthly;
    });
    const noteText = isYearly ? 'Оплата ежегодно (экономия 40%)' : 'Оплата ежемесячно';
    Object.values(notes).forEach(n => { if (n) n.textContent = noteText; });
    if (labelMonthly) labelMonthly.style.opacity = isYearly ? '0.5' : '1';
    if (labelYearly) labelYearly.style.opacity = isYearly ? '1' : '0.5';
  });
}

/* ===== CHECKOUT: plan from URL ===== */
const planData = {
  basic:    { name: 'Базовый',  price: '99 ₽/мес',  total: '99 ₽',  features: ['✓ 1 устройство', '✓ 30 стран', '✓ 100 Мбит/с', '✓ AES-256'] },
  standard: { name: 'Стандарт', price: '199 ₽/мес', total: '199 ₽', features: ['✓ 3 устройства', '✓ 60 стран', '✓ 1 Гбит/с', '✓ Kill Switch'] },
  premium:  { name: 'Премиум',  price: '349 ₽/мес', total: '349 ₽', features: ['✓ 6 устройств', '✓ 90+ стран', '✓ 10 Гбит/с', '✓ Выделенный IP'] },
};

const orderPlan = document.getElementById('orderPlan');
const orderFeatures = document.getElementById('orderFeatures');
const orderTotal = document.getElementById('orderTotal');

if (orderPlan) {
  const params = new URLSearchParams(window.location.search);
  const plan = planData[params.get('plan')] || planData.standard;
  orderPlan.querySelector('.order-plan__name').textContent = plan.name;
  orderPlan.querySelector('.order-plan__price').textContent = plan.price;
  orderTotal.textContent = plan.total;
  orderFeatures.innerHTML = plan.features.map(f => `<li>${f}</li>`).join('');
}

/* ===== CARD NUMBER FORMATTING ===== */
const cardNumber = document.getElementById('cardNumber');
if (cardNumber) {
  cardNumber.addEventListener('input', e => {
    let val = e.target.value.replace(/\D/g, '').substring(0, 16);
    e.target.value = val.replace(/(.{4})/g, '$1 ').trim();
  });
}

const cardExpiry = document.getElementById('cardExpiry');
if (cardExpiry) {
  cardExpiry.addEventListener('input', e => {
    let val = e.target.value.replace(/\D/g, '').substring(0, 4);
    if (val.length >= 2) val = val.substring(0, 2) + '/' + val.substring(2);
    e.target.value = val;
  });
}

/* ===== CHECKOUT FORM SUBMIT ===== */
const checkoutForm = document.getElementById('checkoutForm');
const successModal = document.getElementById('successModal');
if (checkoutForm && successModal) {
  checkoutForm.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;

    const email = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      emailError.textContent = 'Введите корректный email';
      email.classList.add('error');
      valid = false;
    } else {
      emailError.textContent = '';
      email.classList.remove('error');
    }

    const password = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    if (!password.value || password.value.length < 8) {
      passwordError.textContent = 'Пароль должен содержать минимум 8 символов';
      password.classList.add('error');
      valid = false;
    } else {
      passwordError.textContent = '';
      password.classList.remove('error');
    }

    if (valid) {
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.textContent = 'Обработка...';
      submitBtn.disabled = true;
      setTimeout(() => {
        window.location.href = 'https://funpay.com/lots/offer?id=69831833';
      }, 1200);
    }
  });

  successModal.addEventListener('click', e => {
    if (e.target === successModal) successModal.classList.remove('open');
  });
}

/* ===== LOGIN FORM ===== */
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', e => {
    e.preventDefault();
    const email = document.getElementById('loginEmail');
    const password = document.getElementById('loginPassword');
    const emailError = document.getElementById('loginEmailError');
    const passwordError = document.getElementById('loginPasswordError');
    let valid = true;

    if (!email.value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      emailError.textContent = 'Введите корректный email';
      email.classList.add('error');
      valid = false;
    } else {
      emailError.textContent = '';
      email.classList.remove('error');
    }

    if (!password.value) {
      passwordError.textContent = 'Введите пароль';
      password.classList.add('error');
      valid = false;
    } else {
      passwordError.textContent = '';
      password.classList.remove('error');
    }

    if (valid) {
      const btn = loginForm.querySelector('button[type="submit"]');
      btn.textContent = 'Вход...';
      btn.disabled = true;
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 1000);
    }
  });
}

/* ===== SCROLL ANIMATIONS ===== */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .plan-card, .review-card, .how__step').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

/* ===== SMOOTH SCROLL ANIMATIONS FOR ALL SECTIONS ===== */
const scrollObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    } else {
      entry.target.classList.remove('visible');
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('section, .container').forEach(el => {
  el.classList.add('scroll-animate');
  scrollObserver.observe(el);
});


/* ===== AUTHORIZATION CHECK ===== */
document.addEventListener('DOMContentLoaded', () => {
  const userId = localStorage.getItem('user_id');
  const username = localStorage.getItem('username');
  
  const authActions = document.getElementById('authActions');
  const userActions = document.getElementById('userActions');
  const userGreeting = document.getElementById('userGreeting');
  
  const mobileAuthActions = document.getElementById('mobileAuthActions');
  const mobileUserActions = document.getElementById('mobileUserActions');
  
  if (userId && username) {
    // Пользователь авторизован
    if (authActions) authActions.style.display = 'none';
    if (userActions) {
      userActions.style.display = 'flex';
      if (userGreeting) userGreeting.textContent = `Привет, ${username}!`;
    }
    
    if (mobileAuthActions) mobileAuthActions.style.display = 'none';
    if (mobileUserActions) mobileUserActions.style.display = 'block';
  } else {
    // Пользователь не авторизован
    if (authActions) authActions.style.display = 'flex';
    if (userActions) userActions.style.display = 'none';
    
    if (mobileAuthActions) mobileAuthActions.style.display = 'flex';
    if (mobileUserActions) mobileUserActions.style.display = 'none';
  }
});


/* ===== DISCORD PROFILE MODAL ===== */
const discordProfileBtn = document.getElementById('discordProfileBtn');
const discordProfileModal = document.getElementById('discordProfileModal');

if (discordProfileBtn && discordProfileModal) {
  // Открыть модальное окно при клике на кнопку
  discordProfileBtn.addEventListener('click', (e) => {
    e.preventDefault();
    discordProfileModal.style.display = 'block';
    discordProfileModal.classList.add('active');
  });
  
  // Закрыть модальное окно при клике вне его
  document.addEventListener('click', (e) => {
    if (discordProfileModal.style.display === 'block' && 
        !discordProfileModal.contains(e.target) && 
        !discordProfileBtn.contains(e.target)) {
      discordProfileModal.style.display = 'none';
      discordProfileModal.classList.remove('active');
    }
  });
  
  // Закрыть при нажатии Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && discordProfileModal.style.display === 'block') {
      discordProfileModal.style.display = 'none';
      discordProfileModal.classList.remove('active');
    }
  });
}
