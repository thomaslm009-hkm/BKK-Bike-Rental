/* ==========================================================================
   BKK Motorbike Rental - Main Application Coordinator
   ========================================================================== */

const App = {
  currentLang: 'en',
  fleetFilter: 'all',
  activeDurationPricing: 'daily', // daily | weekly | monthly

  init() {
    this.renderFleetGrid();
    if (typeof ReviewsManager !== 'undefined') ReviewsManager.init();
    this.renderReviews();
    this.renderFAQ();
    this.bindGlobalEvents();
    this.setLanguage(this.currentLang);

    // Init modules
    BookingEngine.init();
    SmartKeyHUD.init();
    if (window.AdminPortal) AdminPortal.init();
  },

  renderFleetGrid() {
    const grid = document.getElementById('fleet-catalog-grid');
    if (!grid) return;

    let filtered = FLEET_DATA;
    if (this.fleetFilter !== 'all') {
      filtered = FLEET_DATA.filter(b => b.tier === this.fleetFilter);
    }

    grid.innerHTML = filtered.map(b => {
      let priceDisplay = `฿${b.rates.daily}`;
      let unitText = '/ day';
      let hintText = `Weekly: ฿${b.rates.weekly.toLocaleString()} • Monthly: ฿${b.rates.monthly.toLocaleString()}`;

      if (this.activeDurationPricing === 'weekly') {
        priceDisplay = `฿${b.rates.weekly.toLocaleString()}`;
        unitText = '/ 7 days';
      } else if (this.activeDurationPricing === 'monthly') {
        priceDisplay = `฿${b.rates.monthly.toLocaleString()}`;
        unitText = '/ 30 days';
      }

      const tierBadgeClass = b.tier === 'premium' ? 'tier-premium' : 'tier-standard';
      const isAvailable = b.status === 'available';

      return `
        <div class="bike-card" data-tier="${b.tier}">
          <div class="bike-img-wrapper">
            <span class="bike-tier-badge ${tierBadgeClass}">${b.tier.toUpperCase()}</span>
            <span class="bike-availability-badge">
              <span class="pulse-dot"></span> ${isAvailable ? 'Ready to Ride' : 'Active on Road'}
            </span>
            <img src="${b.image}" alt="${b.name}" class="bike-img" loading="lazy">
          </div>
          <div class="bike-content">
            <h3 class="bike-name">${b.name}</h3>
            <p class="bike-sub">${b.cc}cc • ${b.transmission} • ${b.storage}</p>
            
            <ul class="bike-features-list">
              <li class="bike-feature-item">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V18h-2v-1.07A7 7 0 0 1 5.07 11H6v-2h-.93A7 7 0 0 1 11 5.07V4h2v1.07A7 7 0 0 1 18.93 11H18v2h.93A7 7 0 0 1 13 16.93zM12 8a4 4 0 1 0 4 4 4 4 0 0 0-4-4z"/></svg>
                GPS IoT Tracker
              </li>
              <li class="bike-feature-item">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                2 Helmets Included
              </li>
              <li class="bike-feature-item">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
                Smart Key Access
              </li>
              <li class="bike-feature-item">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
                Por Ror Bor Insurance
              </li>
            </ul>

            <div class="bike-pricing-block">
              <div class="bike-price-wrap">
                <div class="price-main">${priceDisplay} <span>${unitText}</span></div>
                <div class="price-tier-hint">${hintText}</div>
              </div>
              <button class="btn btn-primary" onclick="BookingEngine.openBooking('${b.id}')">
                Book Now
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  renderReviews() {
    if (typeof ReviewsManager !== 'undefined') {
      ReviewsManager.renderReviews();
      return;
    }
    const grid = document.getElementById('reviews-grid');
    if (!grid) return;
    grid.innerHTML = REVIEWS_DATA.map(r => `
      <div class="review-card">
        <div class="review-stars">★★★★★</div>
        <p class="review-quote">"${r.comment}"</p>
        <div class="review-author">
          <div class="author-avatar">${r.avatar}</div>
          <div>
            <div class="author-name">${r.name}</div>
            <div class="author-role">${r.role}</div>
          </div>
        </div>
      </div>
    `).join('');
  },

  renderFAQ() {
    const container = document.getElementById('faq-accordion');
    if (!container) return;
    const isTh = this.currentLang === 'th';

    container.innerHTML = FAQ_DATA.map((f, i) => `
      <div class="faq-item ${i === 0 ? 'open' : ''}">
        <button class="faq-question" onclick="this.parentElement.classList.toggle('open')">
          <span>${isTh ? f.q_th : f.q_en}</span>
          <span class="faq-icon">+</span>
        </button>
        <div class="faq-answer">
          <p style="white-space: pre-line;">${isTh ? f.a_th : f.a_en}</p>
        </div>
      </div>
    `).join('');
  },

  setLanguage(lang) {
    this.currentLang = lang;
    document.body.className = (lang === 'th' ? 'lang-th' : '');

    // Toggle button UI
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    this.renderFAQ();
  },

  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${type === 'success' ? '✅' : (type === 'danger' ? '⚠️' : 'ℹ️')}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  bindGlobalEvents() {
    // Language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.setLanguage(btn.dataset.lang);
      });
    });

    // Fleet category filters
    document.querySelectorAll('.fleet-filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.fleet-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.fleetFilter = btn.dataset.tier;
        this.renderFleetGrid();
      });
    });

    // Hero duration preset buttons
    document.querySelectorAll('.hero-preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.hero-preset-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const days = parseInt(btn.dataset.days) || 1;
        if (days >= 30) this.activeDurationPricing = 'monthly';
        else if (days >= 7) this.activeDurationPricing = 'weekly';
        else this.activeDurationPricing = 'daily';
        this.renderFleetGrid();
      });
    });

    // Hero Search Button
    const searchBtn = document.getElementById('btn-hero-search');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        const tierSelect = document.getElementById('search-tier-select');
        if (tierSelect && tierSelect.value !== 'all') {
          this.fleetFilter = tierSelect.value;
          document.querySelectorAll('.fleet-filter-btn').forEach(b => {
            b.classList.toggle('active', b.dataset.tier === this.fleetFilter);
          });
        }
        this.renderFleetGrid();
        const catalogSection = document.getElementById('fleet-catalog');
        if (catalogSection) catalogSection.scrollIntoView({ behavior: 'smooth' });
        this.showToast('Updated Fleet Inventory for Selected Dates!', 'success');
      });
    }

    // Direct HUD launch button in navbar
    const hudNavBtn = document.getElementById('nav-open-hud-btn');
    if (hudNavBtn) {
      hudNavBtn.addEventListener('click', () => {
        SmartKeyHUD.openHUD(FLEET_DATA[0], 'BK-DEMO-LIVE');
      });
    }
  }
};

// Bootstrap on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
