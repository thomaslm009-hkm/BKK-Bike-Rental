/* ==========================================================================
   BKK Motorbike Rental - Multi-Step Booking & Payment Engine
   ========================================================================== */

const BookingEngine = {
  currentStep: 1,
  selectedBike: null,
  bookingState: {
    durationDays: 1,
    startDate: null,
    endDate: null,
    location: 'sathorn',
    isDelivery: false,
    addons: {
      helmetPro: false,
      waiver: true,
      phoneMount: true
    },
    userType: 'international', // international | domestic
    pricing: {
      rentalTotal: 300,
      addonsTotal: 80,
      deliveryTotal: 0,
      depositTotal: 2000,
      grandTotal: 2380
    },
    kycCompleted: false,
    paymentCompleted: false,
    bookingId: null
  },
  qrTimerInterval: null,

  init() {
    this.bindEvents();
    this.setDefaultDates();
  },

  setDefaultDates() {
    const today = new Date();
    const nextDay = new Date();
    nextDay.setDate(today.getDate() + 1);

    const startInput = document.getElementById('search-start-date') || document.getElementById('modal-start-date');
    const endInput = document.getElementById('search-end-date') || document.getElementById('modal-end-date');

    const fmt = (d) => d.toISOString().split('T')[0];
    if (startInput) startInput.value = fmt(today);
    if (endInput) endInput.value = fmt(nextDay);
  },

  openBooking(bikeId) {
    const bike = FLEET_DATA.find(b => b.id === bikeId) || FLEET_DATA[0];
    this.selectedBike = bike;
    this.currentStep = 1;
    this.bookingState.bookingId = 'BK-' + Math.floor(100000 + Math.random() * 900000);

    // Populate modal bike info
    const imgEl = document.getElementById('modal-selected-bike-img');
    const nameEl = document.getElementById('modal-selected-bike-name');
    const rateEl = document.getElementById('modal-selected-bike-rate');

    if (imgEl) imgEl.src = bike.image;
    if (nameEl) nameEl.textContent = bike.name;
    if (rateEl) rateEl.textContent = `฿${bike.rates.daily}/day • ฿${bike.rates.weekly}/wk • ฿${bike.rates.monthly}/mo`;

    this.calculateTotal();
    this.updateStepUI();

    const overlay = document.getElementById('booking-modal-overlay');
    if (overlay) overlay.classList.add('active');
  },

  closeModal() {
    const overlay = document.getElementById('booking-modal-overlay');
    if (overlay) overlay.classList.remove('active');
    if (this.qrTimerInterval) clearInterval(this.qrTimerInterval);
  },

  goToStep(step) {
    if (step < 1 || step > 4) return;
    this.currentStep = step;
    this.updateStepUI();

    if (step === 4) {
      this.generatePromptPayQR();
    }
  },

  updateStepUI() {
    // Update step bubbles
    document.querySelectorAll('.booking-steps-bar .step-item').forEach((item, index) => {
      const stepIndex = index + 1;
      item.classList.remove('active', 'completed');
      if (stepIndex === this.currentStep) {
        item.classList.add('active');
      } else if (stepIndex < this.currentStep) {
        item.classList.add('completed');
      }
    });

    // Update panels
    document.querySelectorAll('.step-panel').forEach(panel => {
      panel.classList.remove('active');
    });
    const activePanel = document.getElementById(`booking-step-${this.currentStep}`);
    if (activePanel) activePanel.classList.add('active');
  },

  calculateTotal() {
    if (!this.selectedBike) return;

    const days = parseInt(this.bookingState.durationDays) || 1;
    let rentalRate = 0;

    if (days >= 30) {
      const months = Math.floor(days / 30);
      const remDays = days % 30;
      rentalRate = (months * this.selectedBike.rates.monthly) + (remDays * this.selectedBike.rates.daily);
    } else if (days >= 7) {
      const weeks = Math.floor(days / 7);
      const remDays = days % 7;
      rentalRate = (weeks * this.selectedBike.rates.weekly) + (remDays * this.selectedBike.rates.daily);
    } else {
      rentalRate = days * this.selectedBike.rates.daily;
    }

    // Addons
    let addonsRate = 0;
    const isWaiver = this.bookingState.addons.waiver;
    const isHelmet = this.bookingState.addons.helmetPro;

    if (isWaiver) {
      const waiverDaily = this.selectedBike.tier === 'premium' ? 150 : 80;
      addonsRate += waiverDaily * days;
    }
    if (isHelmet) {
      addonsRate += 50 * days;
    }

    // Delivery fee
    const deliveryFee = this.bookingState.isDelivery ? 200 : 0;

    // Deposit
    const depositAmount = this.bookingState.userType === 'domestic'
      ? this.selectedBike.deposit.domestic
      : this.selectedBike.deposit.international;

    const grandTotal = rentalRate + addonsRate + deliveryFee + depositAmount;

    this.bookingState.pricing = {
      rentalTotal: rentalRate,
      addonsTotal: addonsRate,
      deliveryTotal: deliveryFee,
      depositTotal: depositAmount,
      grandTotal: grandTotal
    };

    // Update breakdown UI in modal
    this.renderBreakdownUI();
  },

  renderBreakdownUI() {
    const p = this.bookingState.pricing;
    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setTxt('summary-duration-text', `${this.bookingState.durationDays} Day(s) Rental`);
    setTxt('summary-rental-fee', `฿${p.rentalTotal.toLocaleString()}`);
    setTxt('summary-addons-fee', `฿${p.addonsTotal.toLocaleString()}`);
    setTxt('summary-delivery-fee', p.deliveryTotal > 0 ? `฿${p.deliveryTotal.toLocaleString()}` : 'Free Hub Pickup');
    setTxt('summary-deposit-fee', `฿${p.depositTotal.toLocaleString()}`);
    setTxt('summary-grand-total', `฿${p.grandTotal.toLocaleString()}`);
    setTxt('qr-amount-display', `฿${p.grandTotal.toLocaleString()}`);
  },

  generatePromptPayQR() {
    const canvas = document.getElementById('promptpay-qr-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = 200;
    canvas.height = 200;

    // Draw stylized mock PromptPay QR with high aesthetic precision
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, 200, 200);

    // Draw QR outer corner squares
    ctx.fillStyle = '#0a1128';
    const drawFinder = (x, y) => {
      ctx.fillRect(x, y, 40, 40);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(x + 6, y + 6, 28, 28);
      ctx.fillStyle = '#0a1128';
      ctx.fillRect(x + 12, y + 12, 16, 16);
    };

    drawFinder(15, 15);
    drawFinder(145, 15);
    drawFinder(15, 145);

    // Draw simulated QR matrix dots
    ctx.fillStyle = '#0a1128';
    for (let row = 0; row < 18; row++) {
      for (let col = 0; col < 18; col++) {
        const px = 15 + col * 9.5;
        const py = 15 + row * 9.5;
        // Avoid corners
        if ((row < 5 && col < 5) || (row < 5 && col > 12) || (row > 12 && col < 5)) continue;
        if ((row * 7 + col * 13) % 3 === 0 || (row + col) % 4 === 0) {
          ctx.fillRect(px, py, 6.5, 6.5);
        }
      }
    }

    // Draw PromptPay Center Badge
    ctx.fillStyle = '#003d6b';
    ctx.beginPath();
    ctx.arc(100, 100, 20, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 9px Plus Jakarta Sans, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('PROMPT', 100, 96);
    ctx.fillText('PAY', 100, 106);

    // Start 10-minute countdown
    let secondsLeft = 600;
    if (this.qrTimerInterval) clearInterval(this.qrTimerInterval);
    const timerEl = document.getElementById('qr-timer-countdown');

    this.qrTimerInterval = setInterval(() => {
      secondsLeft--;
      if (secondsLeft <= 0) {
        clearInterval(this.qrTimerInterval);
        if (timerEl) timerEl.textContent = 'Expired. Tap to refresh.';
        return;
      }
      const m = Math.floor(secondsLeft / 60).toString().padStart(2, '0');
      const s = (secondsLeft % 60).toString().padStart(2, '0');
      if (timerEl) timerEl.textContent = `${m}:${s}`;
    }, 1000);
  },

  simulateInstantPayment() {
    const btn = document.getElementById('btn-simulate-pay');
    if (btn) {
      btn.innerHTML = '<span class="pulse-dot"></span> Verifying PromptPay Slip...';
      btn.disabled = true;
    }

    setTimeout(() => {
      this.bookingState.paymentCompleted = true;
      if (this.qrTimerInterval) clearInterval(this.qrTimerInterval);
      this.closeModal();

      // Show success toast
      App.showToast(`Payment Confirmed for ${this.selectedBike.name}! Digital Key Ready.`, 'success');

      // Update bike status in local dataset
      this.selectedBike.status = 'rented';
      if (window.AdminPortal) AdminPortal.refreshMetrics();

      // Launch Smart Key Digital Key HUD automatically
      setTimeout(() => {
        SmartKeyHUD.openHUD(this.selectedBike, this.bookingState.bookingId);
      }, 600);
    }, 1200);
  },

  simulateKYCUpload() {
    const preview = document.getElementById('kyc-preview-box');
    const dropzone = document.getElementById('kyc-dropzone-area');
    const docName = document.getElementById('kyc-doc-filename');

    if (dropzone) dropzone.style.display = 'none';
    if (preview) preview.classList.add('active');
    if (docName) docName.textContent = 'Passport_Verified_DLT_OK.jpg (Auto-Watermarked)';

    this.bookingState.kycCompleted = true;
    App.showToast('KYC Identity Document Verified Successfully!', 'success');
  },

  bindEvents() {
    // Add-on checkboxes
    const waiverCheck = document.getElementById('addon-waiver-check');
    const helmetCheck = document.getElementById('addon-helmet-check');
    const deliverySelect = document.getElementById('modal-pickup-hub');
    const durationPresets = document.querySelectorAll('.modal-preset-btn');

    if (waiverCheck) {
      waiverCheck.addEventListener('change', (e) => {
        this.bookingState.addons.waiver = e.target.checked;
        this.calculateTotal();
      });
    }

    if (helmetCheck) {
      helmetCheck.addEventListener('change', (e) => {
        this.bookingState.addons.helmetPro = e.target.checked;
        this.calculateTotal();
      });
    }

    if (deliverySelect) {
      deliverySelect.addEventListener('change', (e) => {
        this.bookingState.isDelivery = (e.target.value === 'delivery');
        this.calculateTotal();
      });
    }

    durationPresets.forEach(btn => {
      btn.addEventListener('click', (e) => {
        durationPresets.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const days = parseInt(btn.dataset.days) || 1;
        this.bookingState.durationDays = days;
        this.calculateTotal();
      });
    });

    // KYC Dropzone simulated click
    const dropzone = document.getElementById('kyc-dropzone-area');
    if (dropzone) {
      dropzone.addEventListener('click', () => this.simulateKYCUpload());
    }

    // Modal close buttons
    const closeBtn = document.getElementById('modal-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeModal());
  }
};
