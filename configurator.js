// ===== CONFIGURATOR LOGIC =====

// Base prices for different speeds (per month)
const basePrices = {
  100: 99,      // 100 Мбит/с
  1000: 199,    // 1 Гбит/с
  10000: 349    // 10 Гбит/с
};

// Feature prices (per month)
const featurePrices = {
  killSwitch: 0,        // Included in base
  dedicatedIP: 50,
  obfuscation: 30,
  adBlock: 20,
  support24: 40
};

// Period discounts
const periodDiscounts = {
  1: 0,      // 0% discount
  3: 0.05,   // 5% discount
  12: 0.20   // 20% discount
};

// Current configuration
let config = {
  devices: 3,
  countries: 16,
  speed: 1000,
  features: {
    killSwitch: true,
    dedicatedIP: false,
    obfuscation: false,
    adBlock: false,
    support24: false
  },
  period: 1
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  updatePreview();
});

function setupEventListeners() {
  // Devices slider
  const devicesSlider = document.getElementById('devicesSlider');
  devicesSlider.addEventListener('input', (e) => {
    config.devices = parseInt(e.target.value);
    document.getElementById('devicesValue').textContent = config.devices;
    updatePreview();
  });

  // Countries slider
  const countriesSlider = document.getElementById('countriesSlider');
  countriesSlider.addEventListener('input', (e) => {
    config.countries = parseInt(e.target.value);
    document.getElementById('countriesValue').textContent = config.countries;
    updatePreview();
  });

  // Speed buttons
  document.querySelectorAll('.speed-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      config.speed = parseInt(e.target.dataset.speed);
      
      // Update speed display
      const speedText = {
        100: '100 Мбит/с',
        1000: '1 Гбит/с',
        10000: '10 Гбит/с'
      };
      document.getElementById('speedValue').textContent = speedText[config.speed];
      updatePreview();
    });
  });

  // Feature checkboxes
  document.querySelectorAll('.feature-checkbox input').forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      const featureName = e.target.id;
      config.features[featureName] = e.target.checked;
      updatePreview();
    });
  });

  // Period buttons
  document.querySelectorAll('.period-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      config.period = parseInt(e.target.dataset.period);
      
      // Update period display
      const periodText = {
        1: '1 месяц',
        3: '3 месяца',
        12: '12 месяцев'
      };
      document.getElementById('previewPeriod').textContent = periodText[config.period];
      updatePreview();
    });
  });

  // Buy button
  document.getElementById('buyBtn').addEventListener('click', () => {
    const totalPrice = calculateTotalPrice();
    alert(`Переход на оплату: ${totalPrice} ₽`);
    // In real implementation, redirect to FunPay or payment gateway
  });
}

function calculateBasePrice() {
  return basePrices[config.speed] || 199;
}

function calculateFeaturesPrice() {
  let price = 0;
  
  // Kill Switch is included in base price, don't add extra
  if (config.features.dedicatedIP) price += featurePrices.dedicatedIP;
  if (config.features.obfuscation) price += featurePrices.obfuscation;
  if (config.features.adBlock) price += featurePrices.adBlock;
  if (config.features.support24) price += featurePrices.support24;
  
  return price;
}

function calculateMonthlyPrice() {
  const basePrice = calculateBasePrice();
  const featuresPrice = calculateFeaturesPrice();
  return basePrice + featuresPrice;
}

function calculateTotalPrice() {
  const monthlyPrice = calculateMonthlyPrice();
  const discount = periodDiscounts[config.period] || 0;
  const totalMonths = config.period;
  
  // Apply discount to total
  const totalBeforeDiscount = monthlyPrice * totalMonths;
  const totalAfterDiscount = totalBeforeDiscount * (1 - discount);
  
  return Math.round(totalAfterDiscount);
}

function updatePreview() {
  // Update specs
  document.getElementById('previewDevices').textContent = config.devices;
  document.getElementById('previewCountries').textContent = config.countries;
  
  // Update features list
  const featuresList = [];
  if (config.features.killSwitch) featuresList.push('✓ Kill Switch');
  if (config.features.dedicatedIP) featuresList.push('✓ Выделенный IP');
  if (config.features.obfuscation) featuresList.push('✓ Обфускация трафика');
  if (config.features.adBlock) featuresList.push('✓ Блокировка рекламы');
  if (config.features.support24) featuresList.push('✓ Поддержка 24/7');
  
  const previewFeatures = document.getElementById('previewFeatures');
  previewFeatures.innerHTML = featuresList.map(f => `<li>${f}</li>`).join('');
  
  // Calculate prices
  const basePrice = calculateBasePrice();
  const featuresPrice = calculateFeaturesPrice();
  const monthlyPrice = calculateMonthlyPrice();
  const totalPrice = calculateTotalPrice();
  const discount = periodDiscounts[config.period] || 0;
  
  // Update pricing display
  document.getElementById('basePrice').textContent = `${basePrice} ₽`;
  document.getElementById('featuresPrice').textContent = `${featuresPrice} ₽`;
  document.getElementById('monthlyPrice').textContent = `${monthlyPrice} ₽`;
  
  // Show discount if applicable
  if (discount > 0) {
    const discountPercent = Math.round(discount * 100);
    document.getElementById('totalPrice').textContent = `${totalPrice} ₽ (-${discountPercent}%)`;
  } else {
    document.getElementById('totalPrice').textContent = `${totalPrice} ₽`;
  }
}
