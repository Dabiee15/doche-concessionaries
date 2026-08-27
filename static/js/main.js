document.addEventListener('DOMContentLoaded', function () {
  console.log('Doche Concessionaries Engine Active');

  // --- 1. Glowing Scroll Line Animation ---
  const progressBar = document.getElementById('scrollProgressBar');
  window.addEventListener('scroll', function () {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (docHeight > 0 && progressBar) {
      const scrollPercent = (scrollTop / docHeight) * 100;
      progressBar.style.width = scrollPercent + '%';
    }
  });

  // --- 2. Light Mode / Dark Mode Switcher ---
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeText = document.getElementById('themeText');

  // Load saved theme or default to light
  const savedTheme = localStorage.getItem('doche_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeUI(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function () {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('doche_theme', newTheme);
      updateThemeUI(newTheme);
    });
  }

  function updateThemeUI(theme) {
    if (themeText) {
      themeText.textContent = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
    }
  }

  // --- 3. Interactive Scheduler Notice & Price Calculations ---
  const serviceSelect = document.getElementById('id_service');
  const productSelect = document.getElementById('id_product');
  const dateInput = document.getElementById('id_booking_date');
  const livePriceEst = document.getElementById('live_price_est');
  const noticeBadge = document.getElementById('notice_badge');

  // Interactive chip selector for services
  const serviceChips = document.querySelectorAll('.service-chip-card');
  serviceChips.forEach(chip => {
    chip.addEventListener('click', function () {
      const sId = this.dataset.serviceId;
      serviceChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');

      if (serviceSelect) {
        serviceSelect.value = sId;
        serviceSelect.dispatchEvent(new Event('change'));
      }
    });
  });

  function updateNoticeAndPrice() {
    let basePrice = 0;
    let minDays = 1;

    if (serviceSelect && serviceSelect.value) {
      const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
      if (selectedOption) {
        minDays = parseInt(selectedOption.dataset.notice || '2', 10);
        basePrice += parseFloat(selectedOption.dataset.price || '0');
      }
    }

    if (productSelect && productSelect.value) {
      const selectedProdOpt = productSelect.options[productSelect.selectedIndex];
      if (selectedProdOpt) {
        basePrice += parseFloat(selectedProdOpt.dataset.price || '0');
      }
    }

    if (dateInput) {
      const today = new Date();
      today.setDate(today.getDate() + minDays);
      const minDateStr = today.toISOString().split('T')[0];
      dateInput.min = minDateStr;

      if (!dateInput.value || dateInput.value < minDateStr) {
        dateInput.value = minDateStr;
      }
    }

    if (noticeBadge) {
      noticeBadge.textContent = `Requires min ${minDays} day(s) advance notice`;
    }

    if (livePriceEst) {
      const total = basePrice > 0 ? basePrice : 3500;
      livePriceEst.textContent = 'N' + total.toLocaleString('en-US', { minimumFractionDigits: 2 });
    }
  }

  if (serviceSelect) serviceSelect.addEventListener('change', updateNoticeAndPrice);
  if (productSelect) productSelect.addEventListener('change', updateNoticeAndPrice);

  updateNoticeAndPrice();
});
