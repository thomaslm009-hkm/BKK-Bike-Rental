/* ==========================================================================
   BKK Motorbike Rental - IoT Smart Key & Active Ride Telemetry HUD
   ========================================================================== */

const SmartKeyHUD = {
  isUnlocked: false,
  tripActive: false,
  activeBike: null,
  activeBookingId: null,
  rideTimerInterval: null,
  simulatedSpeedInterval: null,
  rideSeconds: 0,
  currentSpeed: 0,
  tripKm: 0.0,

  init() {
    this.bindEvents();
    this.renderStateUI();
  },

  // Synthesize realistic scooter chirp & unlock sounds using Web Audio API
  playSound(type) {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();

      if (type === 'unlock') {
        // High dual chirp
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1400, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(2200, ctx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.2);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.2);

        setTimeout(() => {
          const osc2 = ctx.createOscillator();
          const gain2 = ctx.createGain();
          osc2.connect(gain2);
          gain2.connect(ctx.destination);
          osc2.type = 'sine';
          osc2.frequency.setValueAtTime(1800, ctx.currentTime);
          osc2.frequency.exponentialRampToValueAtTime(2600, ctx.currentTime + 0.15);
          gain2.gain.setValueAtTime(0.3, ctx.currentTime);
          gain2.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.25);
          osc2.start(ctx.currentTime);
          osc2.stop(ctx.currentTime + 0.25);
        }, 120);
      } else if (type === 'lock') {
        // Low solid double chirp
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(800, ctx.currentTime);
        gain.gain.setValueAtTime(0.35, ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.15);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.15);
      }
    } catch (e) {
      console.log('Web Audio not supported or blocked by user gesture policy');
    }
  },

  openHUD(bike, bookingId) {
    const modal = document.getElementById('smart-key-modal-overlay');

    // Only re-initialize if it's a completely new bike and no trip is running
    const isNewBike = bike && this.activeBike && bike.id !== this.activeBike.id && !this.tripActive;

    if (!this.activeBike || isNewBike) {
      this.activeBike = bike || FLEET_DATA[0];
      this.activeBookingId = bookingId || 'BK-DEMO-8821';
      this.isUnlocked = false;
      this.tripActive = false;
      this.rideSeconds = 0;
      this.tripKm = 0.0;
      this.currentSpeed = 0;
    } else if (bike && !this.activeBike) {
      this.activeBike = bike;
      this.activeBookingId = bookingId || 'BK-DEMO-8821';
    }

    // Populate modal fields
    const bikeTitle = document.getElementById('hud-bike-title');
    const plate = document.getElementById('hud-plate-number');
    const iotId = document.getElementById('hud-iot-device');
    const fuel = document.getElementById('hud-fuel-level');
    const battery = document.getElementById('hud-battery-volt');
    const odo = document.getElementById('hud-odometer');

    if (bikeTitle) bikeTitle.textContent = this.activeBike.name;
    if (plate) plate.textContent = this.activeBike.plateNumber;
    if (iotId) iotId.textContent = `IoT ID: ${this.activeBike.iotDeviceId}`;
    if (fuel) fuel.textContent = `${this.activeBike.fuelLevel}%`;
    if (battery) battery.textContent = `${this.activeBike.batteryVoltage}V`;
    if (odo) odo.textContent = `${this.activeBike.odometerKm} km`;

    // Hide floating widget while full modal is active
    this.hideFloatingWidget();

    this.renderStateUI();
    this.syncMetricsUI();

    if (modal) modal.classList.add('active');
  },

  closeHUD() {
    const modal = document.getElementById('smart-key-modal-overlay');
    if (modal) modal.classList.remove('active');

    // IF trip is active or bike is unlocked:
    // DO NOT reset timers or intervals! Keep trip running in background
    if (this.tripActive || this.isUnlocked) {
      this.showFloatingWidget();
      App.showToast('Vehicle active! Monitoring live telemetry on floating widget.', 'info');
    } else {
      this.hideFloatingWidget();
      this.stopRideTelemetry();
    }
  },

  toggleLock() {
    this.isUnlocked = !this.isUnlocked;

    if (this.isUnlocked) {
      this.tripActive = true;
      this.playSound('unlock');
      App.showToast(`🔑 Signal Sent! ${this.activeBike.name} Unlocked & Engine Ready`, 'success');
      this.startRideTelemetry();
    } else {
      this.playSound('lock');
      App.showToast(`🔒 Signal Sent! ${this.activeBike.name} Locked & Parked`, 'info');
      this.pauseRideTelemetry();
    }

    this.renderStateUI();
    this.syncMetricsUI();
  },

  renderStateUI() {
    const ring = document.getElementById('hud-status-ring');
    const stateText = document.getElementById('hud-state-text');
    const actionBtn = document.getElementById('btn-hud-toggle-lock');
    const icon = document.getElementById('hud-fob-icon');
    const widgetQuickLockBtn = document.getElementById('widget-quick-lock-btn');
    const widgetPill = document.getElementById('floating-ride-widget');
    const widgetStatusText = document.getElementById('widget-status-text');

    if (this.isUnlocked) {
      if (ring) { ring.className = 'smart-fob-status-ring unlocked'; }
      if (stateText) { stateText.textContent = 'SYSTEM UNLOCKED • ENGINE READY'; stateText.style.color = '#10B981'; }
      if (icon) { icon.textContent = '🔓'; }
      if (actionBtn) {
        actionBtn.innerHTML = '<span>🔒</span> Lock & Immobilize Motorbike';
        actionBtn.className = 'btn btn-secondary btn-block';
      }
      if (widgetQuickLockBtn) {
        widgetQuickLockBtn.innerHTML = '🔒 Quick Lock';
        widgetQuickLockBtn.className = 'btn btn-sm btn-outline-accent';
      }
      if (widgetPill) { widgetPill.classList.remove('locked'); }
      if (widgetStatusText) { widgetStatusText.textContent = 'RIDE ACTIVE'; }
    } else {
      if (ring) { ring.className = 'smart-fob-status-ring locked'; }
      if (stateText) {
        stateText.textContent = this.tripActive ? 'PARKED & LOCKED • IMMOBILIZER ACTIVE' : 'SYSTEM LOCKED • IMMOBILIZER ON';
        stateText.style.color = '#EF4444';
      }
      if (icon) { icon.textContent = '🔒'; }
      if (actionBtn) {
        actionBtn.innerHTML = '<span>🔑</span> Tap to Unlock Motorbike';
        actionBtn.className = 'btn btn-primary btn-block';
      }
      if (widgetQuickLockBtn) {
        widgetQuickLockBtn.innerHTML = '🔑 Tap Unlock';
        widgetQuickLockBtn.className = 'btn btn-sm btn-primary';
      }
      if (widgetPill) { widgetPill.classList.add('locked'); }
      if (widgetStatusText) { widgetStatusText.textContent = 'PARKED'; }
    }
  },

  startRideTelemetry() {
    if (this.rideTimerInterval) clearInterval(this.rideTimerInterval);
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);

    // Speedometer simulation (varies between 25 and 58 km/h while riding)
    this.simulatedSpeedInterval = setInterval(() => {
      if (this.isUnlocked) {
        const targetSpeed = Math.floor(28 + Math.random() * 28);
        this.currentSpeed = targetSpeed;
      } else {
        this.currentSpeed = 0;
      }
      this.syncMetricsUI();
    }, 1500);

    // Trip duration & distance timer (keeps incrementing every second)
    this.rideTimerInterval = setInterval(() => {
      this.rideSeconds++;
      if (this.isUnlocked) {
        this.tripKm += 0.012; // distance increments while unlocked
      }
      this.syncMetricsUI();
    }, 1000);
  },

  pauseRideTelemetry() {
    // When locked during an active trip: speed drops to 0, but timer keeps overall rental duration
    this.currentSpeed = 0;
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);
    this.syncMetricsUI();
  },

  stopRideTelemetry() {
    if (this.rideTimerInterval) clearInterval(this.rideTimerInterval);
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);
    this.rideTimerInterval = null;
    this.simulatedSpeedInterval = null;
    this.currentSpeed = 0;
  },

  syncMetricsUI() {
    const m = Math.floor(this.rideSeconds / 60).toString().padStart(2, '0');
    const s = (this.rideSeconds % 60).toString().padStart(2, '0');
    const timeFormatted = `${m}:${s}`;
    const speedFormatted = `${this.currentSpeed} km/h`;
    const distFormatted = `${this.tripKm.toFixed(2)} km`;
    const fuelFormatted = this.activeBike ? `${this.activeBike.fuelLevel}%` : '95%';
    const batteryFormatted = this.activeBike ? `${this.activeBike.batteryVoltage}V` : '12.6V';
    const bikeName = this.activeBike ? this.activeBike.name : 'Honda Click 160';

    // Update Modal HUD Elements
    const timeEl = document.getElementById('hud-trip-timer');
    const speedEl = document.getElementById('hud-speed-gauge');
    const distEl = document.getElementById('hud-trip-dist');
    const fuelEl = document.getElementById('hud-fuel-level');
    const battEl = document.getElementById('hud-battery-volt');

    if (timeEl) timeEl.textContent = timeFormatted;
    if (speedEl) speedEl.textContent = this.isUnlocked ? speedFormatted : '0 km/h (Parked)';
    if (distEl) distEl.textContent = distFormatted;
    if (fuelEl) fuelEl.textContent = fuelFormatted;
    if (battEl) battEl.textContent = batteryFormatted;

    // Update Floating Widget Elements
    const wTimer = document.getElementById('widget-timer');
    const wSpeed = document.getElementById('widget-speed');
    const wFuel = document.getElementById('widget-fuel');
    const wBatt = document.getElementById('widget-battery');
    const wName = document.getElementById('widget-bike-name');

    if (wTimer) wTimer.textContent = timeFormatted;
    if (wSpeed) wSpeed.textContent = this.isUnlocked ? speedFormatted : '0 km/h';
    if (wFuel) wFuel.textContent = fuelFormatted;
    if (wBatt) wBatt.textContent = batteryFormatted;
    if (wName) wName.textContent = bikeName;
  },

  showFloatingWidget() {
    const widget = document.getElementById('floating-ride-widget');
    if (!widget) return;
    this.syncMetricsUI();
    this.renderStateUI();
    widget.style.display = 'block';
  },

  hideFloatingWidget() {
    const widget = document.getElementById('floating-ride-widget');
    if (widget) widget.style.display = 'none';
  },

  completeReturnFlow() {
    this.stopRideTelemetry();
    this.isUnlocked = false;
    this.tripActive = false;
    this.hideFloatingWidget();
    this.renderStateUI();

    App.showToast('Submitting 4-Point Vehicle Return Inspection...', 'info');

    setTimeout(() => {
      this.closeHUD();
      if (this.activeBike) {
        this.activeBike.status = 'available';
      }
      this.rideSeconds = 0;
      this.tripKm = 0.0;
      this.currentSpeed = 0;

      if (window.AdminPortal) AdminPortal.refreshMetrics();

      App.showToast(`✅ Trip Complete! Security Deposit refunded to your PromptPay account.`, 'success');
    }, 1500);
  },

  bindEvents() {
    const ring = document.getElementById('hud-status-ring');
    const toggleBtn = document.getElementById('btn-hud-toggle-lock');
    const closeBtn = document.getElementById('hud-close-btn');
    const minimizeBtn = document.getElementById('hud-minimize-btn');
    const returnBtn = document.getElementById('btn-hud-return-bike');

    if (ring) ring.addEventListener('click', () => this.toggleLock());
    if (toggleBtn) toggleBtn.addEventListener('click', () => this.toggleLock());
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeHUD());
    if (minimizeBtn) minimizeBtn.addEventListener('click', () => this.closeHUD());
    if (returnBtn) returnBtn.addEventListener('click', () => this.completeReturnFlow());

    // Floating Widget event bindings
    const wExpandBtn = document.getElementById('widget-expand-btn');
    const wOpenHudBtn = document.getElementById('widget-open-hud-btn');
    const wQuickLockBtn = document.getElementById('widget-quick-lock-btn');
    const wHeader = document.querySelector('.ride-widget-header');

    if (wExpandBtn) wExpandBtn.addEventListener('click', () => this.openHUD());
    if (wOpenHudBtn) wOpenHudBtn.addEventListener('click', () => this.openHUD());
    if (wHeader) wHeader.addEventListener('click', (e) => {
      if (e.target !== wExpandBtn) this.openHUD();
    });
    if (wQuickLockBtn) wQuickLockBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleLock();
    });
  }
};
