/* ==========================================================================
   BKK Motorbike Rental - IoT Smart Key & Active Ride Telemetry HUD
   ========================================================================== */

const SmartKeyHUD = {
  isUnlocked: false,
  activeBike: null,
  activeBookingId: null,
  rideTimerInterval: null,
  simulatedSpeedInterval: null,
  rideSeconds: 0,
  currentSpeed: 0,
  tripKm: 0.0,

  init() {
    this.bindEvents();
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
    this.activeBike = bike || FLEET_DATA[0];
    this.activeBookingId = bookingId || 'BK-DEMO-8821';
    this.isUnlocked = false;
    this.rideSeconds = 0;
    this.tripKm = 0.0;

    const modal = document.getElementById('smart-key-modal-overlay');
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

    this.renderStateUI();
    if (modal) modal.classList.add('active');
  },

  closeHUD() {
    const modal = document.getElementById('smart-key-modal-overlay');
    if (modal) modal.classList.remove('active');
    if (this.rideTimerInterval) clearInterval(this.rideTimerInterval);
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);
  },

  toggleLock() {
    this.isUnlocked = !this.isUnlocked;

    if (this.isUnlocked) {
      this.playSound('unlock');
      App.showToast(`🔑 Signal Sent! ${this.activeBike.name} Unlocked & Immobilizer OFF`, 'success');
      this.startRideTelemetry();
    } else {
      this.playSound('lock');
      App.showToast(`🔒 Signal Sent! ${this.activeBike.name} Locked & Secured`, 'info');
      this.stopRideTelemetry();
    }

    this.renderStateUI();
  },

  renderStateUI() {
    const ring = document.getElementById('hud-status-ring');
    const stateText = document.getElementById('hud-state-text');
    const actionBtn = document.getElementById('btn-hud-toggle-lock');
    const icon = document.getElementById('hud-fob-icon');

    if (this.isUnlocked) {
      if (ring) { ring.className = 'smart-fob-status-ring unlocked'; }
      if (stateText) { stateText.textContent = 'SYSTEM UNLOCKED • ENGINE READY'; stateText.style.color = '#10B981'; }
      if (icon) { icon.textContent = '🔓'; }
      if (actionBtn) {
        actionBtn.innerHTML = '<span>🔒</span> Lock & Immobilize Motorbike';
        actionBtn.className = 'btn btn-secondary btn-block';
      }
    } else {
      if (ring) { ring.className = 'smart-fob-status-ring locked'; }
      if (stateText) { stateText.textContent = 'SYSTEM LOCKED • IMMOBILIZER ACTIVE'; stateText.style.color = '#EF4444'; }
      if (icon) { icon.textContent = '🔒'; }
      if (actionBtn) {
        actionBtn.innerHTML = '<span>🔑</span> Tap to Unlock Motorbike';
        actionBtn.className = 'btn btn-primary btn-block';
      }
    }
  },

  startRideTelemetry() {
    if (this.rideTimerInterval) clearInterval(this.rideTimerInterval);
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);

    const speedEl = document.getElementById('hud-speed-gauge');
    const tripEl = document.getElementById('hud-trip-dist');
    const timeEl = document.getElementById('hud-trip-timer');

    this.simulatedSpeedInterval = setInterval(() => {
      // Simulate realistic city speed variation (0 to 55 km/h)
      const targetSpeed = Math.floor(25 + Math.random() * 32);
      this.currentSpeed = targetSpeed;
      if (speedEl) speedEl.textContent = `${this.currentSpeed} km/h`;
    }, 1500);

    this.rideTimerInterval = setInterval(() => {
      this.rideSeconds++;
      this.tripKm += 0.012; // simulated distance increment

      if (timeEl) {
        const m = Math.floor(this.rideSeconds / 60).toString().padStart(2, '0');
        const s = (this.rideSeconds % 60).toString().padStart(2, '0');
        timeEl.textContent = `${m}:${s}`;
      }
      if (tripEl) tripEl.textContent = `${this.tripKm.toFixed(2)} km`;
    }, 1000);
  },

  stopRideTelemetry() {
    if (this.rideTimerInterval) clearInterval(this.rideTimerInterval);
    if (this.simulatedSpeedInterval) clearInterval(this.simulatedSpeedInterval);
    const speedEl = document.getElementById('hud-speed-gauge');
    if (speedEl) speedEl.textContent = '0 km/h (Parked)';
  },

  completeReturnFlow() {
    this.stopRideTelemetry();
    this.isUnlocked = false;
    this.renderStateUI();

    App.showToast('Submitting 4-Point Vehicle Return Inspection...', 'info');

    setTimeout(() => {
      this.closeHUD();
      this.activeBike.status = 'available';
      if (window.AdminPortal) AdminPortal.refreshMetrics();

      App.showToast(`✅ Trip Complete! Security Deposit refunded to your account.`, 'success');
    }, 1500);
  },

  bindEvents() {
    const ring = document.getElementById('hud-status-ring');
    const toggleBtn = document.getElementById('btn-hud-toggle-lock');
    const closeBtn = document.getElementById('hud-close-btn');
    const returnBtn = document.getElementById('btn-hud-return-bike');

    if (ring) ring.addEventListener('click', () => this.toggleLock());
    if (toggleBtn) toggleBtn.addEventListener('click', () => this.toggleLock());
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeHUD());
    if (returnBtn) returnBtn.addEventListener('click', () => this.completeReturnFlow());
  }
};
