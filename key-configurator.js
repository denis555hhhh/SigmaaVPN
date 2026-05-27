// ===== KEY CONFIGURATOR LOGIC =====

// Хранилище ключей (в реальном приложении это будет база данных)
let keys = JSON.parse(localStorage.getItem('happ_keys')) || [];

// Текущая конфигурация
let currentConfig = {
  name: '',
  device: 'windows',
  expiry: 30,
  access: 'basic',
  regions: ['eu', 'us', 'asia']
};

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  renderKeysList();
});

function setupEventListeners() {
  // Выбор типа устройства
  document.querySelectorAll('.device-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
      e.currentTarget.classList.add('active');
      currentConfig.device = e.currentTarget.dataset.device;
    });
  });

  // Выбор срока действия
  document.querySelectorAll('.expiry-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.expiry-btn').forEach(b => b.classList.remove('active'));
      e.currentTarget.classList.add('active');
      currentConfig.expiry = parseInt(e.currentTarget.dataset.expiry);
    });
  });

  // Выбор уровня доступа
  document.querySelectorAll('input[name="access"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      currentConfig.access = e.target.value;
    });
  });

  // Выбор регионов
  const selectAllCheckbox = document.getElementById('selectAll');
  const regionCheckboxes = document.querySelectorAll('.region-checkbox input[type="checkbox"]:not(#selectAll)');

  selectAllCheckbox.addEventListener('change', (e) => {
    regionCheckboxes.forEach(checkbox => {
      checkbox.checked = e.target.checked;
    });
    updateRegions();
  });

  regionCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      updateRegions();
      // Обновить состояние "Все регионы"
      const allChecked = Array.from(regionCheckboxes).every(cb => cb.checked);
      selectAllCheckbox.checked = allChecked;
    });
  });

  // Создание ключа
  document.getElementById('generateKeyBtn').addEventListener('click', generateKey);

  // Поиск ключей
  document.getElementById('searchKeys').addEventListener('input', filterKeys);

  // Фильтр по устройству
  document.getElementById('filterDevice').addEventListener('change', filterKeys);

  // Модальные окна
  document.getElementById('closeKeyModal').addEventListener('click', closeKeyModal);
  document.getElementById('closeModalBtn').addEventListener('click', closeKeyModal);
  document.getElementById('copyKeyBtn').addEventListener('click', copyKeyToClipboard);

  document.getElementById('closeDetailsModal').addEventListener('click', closeDetailsModal);
  document.getElementById('closeDetailsBtn').addEventListener('click', closeDetailsModal);
  document.getElementById('revokeKeyBtn').addEventListener('click', revokeKey);

  // Закрытие модалей при клике вне
  document.getElementById('keyModal').addEventListener('click', (e) => {
    if (e.target.id === 'keyModal') closeKeyModal();
  });

  document.getElementById('keyDetailsModal').addEventListener('click', (e) => {
    if (e.target.id === 'keyDetailsModal') closeDetailsModal();
  });
}

function updateRegions() {
  const selected = Array.from(document.querySelectorAll('.region-checkbox input[type="checkbox"]:not(#selectAll):checked'))
    .map(cb => cb.value);
  currentConfig.regions = selected;
}

function generateKey() {
  const keyName = document.getElementById('keyName').value.trim();

  if (!keyName) {
    alert('Пожалуйста, введите название ключа');
    return;
  }

  if (keyName.length > 50) {
    alert('Название ключа не должно превышать 50 символов');
    return;
  }

  if (currentConfig.regions.length === 0) {
    alert('Выберите хотя бы один регион');
    return;
  }

  // Генерируем ключ
  const keyId = generateKeyId();
  const keyValue = generateKeyValue();
  const now = new Date();
  const expiryDate = currentConfig.expiry === 0 
    ? null 
    : new Date(now.getTime() + currentConfig.expiry * 24 * 60 * 60 * 1000);

  const newKey = {
    id: keyId,
    name: keyName,
    value: keyValue,
    device: currentConfig.device,
    access: currentConfig.access,
    regions: [...currentConfig.regions],
    created: now.toISOString(),
    expires: expiryDate ? expiryDate.toISOString() : null,
    status: 'active'
  };

  keys.push(newKey);
  localStorage.setItem('happ_keys', JSON.stringify(keys));

  // Показываем модаль с ключом
  showKeyModal(newKey);

  // Очищаем форму
  document.getElementById('keyName').value = '';
  renderKeysList();
}

function generateKeyId() {
  return 'key_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
}

function generateKeyValue() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < 64; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function showKeyModal(key) {
  const modal = document.getElementById('keyModal');
  document.getElementById('keyValue').textContent = key.value;
  document.getElementById('modalKeyName').textContent = key.name;
  document.getElementById('modalKeyDevice').textContent = getDeviceName(key.device);
  document.getElementById('modalKeyExpiry').textContent = getExpiryText(key.expires);
  document.getElementById('modalKeyAccess').textContent = getAccessName(key.access);
  modal.classList.add('open');
}

function closeKeyModal() {
  document.getElementById('keyModal').classList.remove('open');
}

function copyKeyToClipboard() {
  const keyValue = document.getElementById('keyValue').textContent;
  navigator.clipboard.writeText(keyValue).then(() => {
    alert('✅ Ключ скопирован в буфер обмена');
  });
}

function renderKeysList() {
  const keysList = document.getElementById('keysList');
  const emptyState = document.getElementById('emptyState');

  if (keys.length === 0) {
    keysList.innerHTML = '';
    emptyState.style.display = 'flex';
    return;
  }

  emptyState.style.display = 'none';
  keysList.innerHTML = keys.map(key => `
    <div class="key-card" data-key-id="${key.id}" data-device="${key.device}">
      <div class="key-card__header">
        <div class="key-card__title">
          <span class="key-device-icon">${getDeviceIcon(key.device)}</span>
          <span class="key-card__name">${key.name}</span>
        </div>
        <span class="key-status ${key.status}">${getStatusText(key.status)}</span>
      </div>

      <div class="key-card__info">
        <div class="info-badge">
          <span class="badge-icon">🔐</span>
          <span>${getAccessName(key.access)}</span>
        </div>
        <div class="info-badge">
          <span class="badge-icon">⏰</span>
          <span>${getExpiryText(key.expires)}</span>
        </div>
        <div class="info-badge">
          <span class="badge-icon">🌍</span>
          <span>${key.regions.length} регион${key.regions.length !== 1 ? 'ов' : ''}</span>
        </div>
      </div>

      <div class="key-card__footer">
        <span class="key-id">ID: ${key.id.substring(0, 20)}...</span>
        <button class="btn btn--outline btn--sm" onclick="showKeyDetails('${key.id}')">Подробнее</button>
      </div>
    </div>
  `).join('');
}

function showKeyDetails(keyId) {
  const key = keys.find(k => k.id === keyId);
  if (!key) return;

  document.getElementById('detailName').textContent = key.name;
  document.getElementById('detailId').textContent = key.id;
  document.getElementById('detailDevice').textContent = getDeviceName(key.device);
  document.getElementById('detailAccess').textContent = getAccessName(key.access);
  document.getElementById('detailCreated').textContent = formatDate(new Date(key.created));
  document.getElementById('detailExpires').textContent = key.expires ? formatDate(new Date(key.expires)) : 'Без ограничений';
  document.getElementById('detailStatus').textContent = getStatusText(key.status);
  document.getElementById('detailRegions').textContent = key.regions.map(r => getRegionName(r)).join(', ');

  // Сохраняем ID для удаления
  document.getElementById('revokeKeyBtn').dataset.keyId = keyId;

  document.getElementById('keyDetailsModal').classList.add('open');
}

function closeDetailsModal() {
  document.getElementById('keyDetailsModal').classList.remove('open');
}

function revokeKey() {
  const keyId = document.getElementById('revokeKeyBtn').dataset.keyId;
  if (confirm('Вы уверены? Этот ключ больше не будет работать.')) {
    keys = keys.filter(k => k.id !== keyId);
    localStorage.setItem('happ_keys', JSON.stringify(keys));
    closeDetailsModal();
    renderKeysList();
    alert('✅ Ключ отозван');
  }
}

function filterKeys() {
  const searchTerm = document.getElementById('searchKeys').value.toLowerCase();
  const deviceFilter = document.getElementById('filterDevice').value;

  const filtered = keys.filter(key => {
    const matchesSearch = key.name.toLowerCase().includes(searchTerm) || key.id.includes(searchTerm);
    const matchesDevice = !deviceFilter || key.device === deviceFilter;
    return matchesSearch && matchesDevice;
  });

  const keysList = document.getElementById('keysList');
  const emptyState = document.getElementById('emptyState');

  if (filtered.length === 0) {
    keysList.innerHTML = '';
    emptyState.style.display = 'flex';
    emptyState.querySelector('.empty-icon').textContent = '🔍';
    emptyState.querySelector('p').textContent = 'Ключи не найдены';
    return;
  }

  emptyState.style.display = 'none';
  keysList.innerHTML = filtered.map(key => `
    <div class="key-card" data-key-id="${key.id}" data-device="${key.device}">
      <div class="key-card__header">
        <div class="key-card__title">
          <span class="key-device-icon">${getDeviceIcon(key.device)}</span>
          <span class="key-card__name">${key.name}</span>
        </div>
        <span class="key-status ${key.status}">${getStatusText(key.status)}</span>
      </div>

      <div class="key-card__info">
        <div class="info-badge">
          <span class="badge-icon">🔐</span>
          <span>${getAccessName(key.access)}</span>
        </div>
        <div class="info-badge">
          <span class="badge-icon">⏰</span>
          <span>${getExpiryText(key.expires)}</span>
        </div>
        <div class="info-badge">
          <span class="badge-icon">🌍</span>
          <span>${key.regions.length} регион${key.regions.length !== 1 ? 'ов' : ''}</span>
        </div>
      </div>

      <div class="key-card__footer">
        <span class="key-id">ID: ${key.id.substring(0, 20)}...</span>
        <button class="btn btn--outline btn--sm" onclick="showKeyDetails('${key.id}')">Подробнее</button>
      </div>
    </div>
  `).join('');
}

// Вспомогательные функции
function getDeviceIcon(device) {
  const icons = {
    windows: '🪟',
    mac: '🍎',
    linux: '🐧',
    ios: '📱',
    android: '🤖'
  };
  return icons[device] || '💻';
}

function getDeviceName(device) {
  const names = {
    windows: 'Windows',
    mac: 'macOS',
    linux: 'Linux',
    ios: 'iOS',
    android: 'Android'
  };
  return names[device] || device;
}

function getAccessName(access) {
  const names = {
    basic: 'Базовый',
    premium: 'Премиум',
    admin: 'Администратор'
  };
  return names[access] || access;
}

function getStatusText(status) {
  const texts = {
    active: '✅ Активен',
    expired: '⏰ Истек',
    revoked: '🗑️ Отозван'
  };
  return texts[status] || status;
}

function getRegionName(region) {
  const names = {
    eu: '🇪🇺 Европа',
    us: '🇺🇸 США',
    asia: '🌏 Азия',
    ru: '🇷🇺 Россия'
  };
  return names[region] || region;
}

function getExpiryText(expiryDate) {
  if (!expiryDate) return 'Без ограничений';
  
  const expiry = new Date(expiryDate);
  const now = new Date();
  const daysLeft = Math.ceil((expiry - now) / (1000 * 60 * 60 * 24));

  if (daysLeft < 0) return 'Истек';
  if (daysLeft === 0) return 'Истекает сегодня';
  if (daysLeft === 1) return 'Истекает завтра';
  if (daysLeft <= 7) return `Истекает через ${daysLeft} дней`;
  
  return `Истекает ${formatDate(expiry)}`;
}

function formatDate(date) {
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return date.toLocaleDateString('ru-RU', options);
}
