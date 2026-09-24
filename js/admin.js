/* ==========================================================================
   BKK Motorbike Rental - Admin Fleet Operations & Live Telemetry Portal
   ========================================================================== */

const AdminPortal = {
  activeFilter: 'all',
  searchQuery: '',
  leafletMap: null,
  mapMarkers: [],

  init() {
    this.refreshMetrics();
    this.renderStatusBoard();
    this.renderFleetTable();
    this.initMap();
    this.bindEvents();
  },

  refreshMetrics() {
    const totalBikes = FLEET_DATA.length; // 20
    const available = FLEET_DATA.filter(b => b.status === 'available').length;
    const rented = FLEET_DATA.filter(b => b.status === 'rented').length;
    const maintenance = FLEET_DATA.filter(b => b.status === 'maintenance').length;

    const utilizationPct = Math.round((rented / totalBikes) * 100);

    let currentMonthlyRevenue = 0;
    FLEET_DATA.forEach(bike => {
      if (bike.status === 'rented') {
        currentMonthlyRevenue += bike.tier === 'premium' ? 9500 : 5500;
      }
    });
    currentMonthlyRevenue += 84500; // baseline day-rate transactions for demo

    const FIXED_COST_BREAKEVEN = 168000;
    const breakevenPct = Math.min(100, Math.round((currentMonthlyRevenue / FIXED_COST_BREAKEVEN) * 100));

    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setTxt('admin-kpi-available', `${available} Units`);
    setTxt('admin-kpi-rented', `${rented} Units`);
    setTxt('admin-kpi-maintenance', `${maintenance} ${maintenance === 1 ? 'Unit' : 'Units'}`);
    setTxt('admin-kpi-revenue', `฿${currentMonthlyRevenue.toLocaleString()}`);
    setTxt('admin-kpi-utilization-text', `${utilizationPct}% Fleet Utilization (20 Total)`);
    setTxt('admin-breakeven-progress-text', `${breakevenPct}% of ฿168,000 Fixed Cost Target`);
    setTxt('admin-breakeven-current-rev', `฿${currentMonthlyRevenue.toLocaleString()}`);

    const fill = document.getElementById('admin-breakeven-fill');
    if (fill) fill.style.width = `${breakevenPct}%`;

    // Update filter buttons live counters
    setTxt('filter-btn-all', `All (${totalBikes})`);
    setTxt('filter-btn-available', `🟢 Available (${available})`);
    setTxt('filter-btn-rented', `🔵 Rented (${rented})`);
    setTxt('filter-btn-maintenance', `🟡 Maintenance (${maintenance})`);
  },

  renderStatusBoard() {
    const availableContainer = document.getElementById('status-cards-available');
    const rentedContainer = document.getElementById('status-cards-rented');
    const maintenanceContainer = document.getElementById('status-cards-maintenance');

    const availableBikes = FLEET_DATA.filter(b => b.status === 'available');
    const rentedBikes = FLEET_DATA.filter(b => b.status === 'rented');
    const maintenanceBikes = FLEET_DATA.filter(b => b.status === 'maintenance');

    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setTxt('badge-count-available', `${availableBikes.length} Bikes`);
    setTxt('badge-count-rented', `${rentedBikes.length} Bikes`);
    setTxt('badge-count-maintenance', `${maintenanceBikes.length} Bikes`);

    // 1. Available Column Cards
    if (availableContainer) {
      if (availableBikes.length === 0) {
        availableContainer.innerHTML = `<div class="status-empty-state">No motorbikes currently available.</div>`;
      } else {
        availableContainer.innerHTML = availableBikes.map(b => `
          <div class="bike-status-mini-card">
            <div class="mini-card-top">
              <span class="bike-id-pill">${b.id}</span>
              <span class="license-plate-tag">${b.plateNumber}</span>
            </div>
            <div class="mini-card-model">
              <span>${b.name}</span>
              <span class="bike-tier-badge ${b.tier === 'premium' ? 'tier-premium' : 'tier-standard'}">${b.tier.toUpperCase()}</span>
            </div>
            <div class="mini-card-details">
              <span>📍 ${b.currentLocation.name.split('(')[0].trim()}</span>
              <span>🔋 ${b.batteryVoltage}V • ⛽ ${b.fuelLevel}%</span>
            </div>
            <div class="mini-card-actions">
              <button class="btn btn-xs btn-primary" onclick="AdminPortal.changeBikeStatus('${b.id}', 'rented')">
                🔑 Dispatch / Rent
              </button>
              <button class="btn btn-xs btn-secondary" onclick="AdminPortal.changeBikeStatus('${b.id}', 'maintenance')">
                🔧 Service
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    // 2. Rented Column Cards
    if (rentedContainer) {
      if (rentedBikes.length === 0) {
        rentedContainer.innerHTML = `<div class="status-empty-state">No bikes currently rented out.</div>`;
      } else {
        rentedContainer.innerHTML = rentedBikes.map(b => `
          <div class="bike-status-mini-card rented">
            <div class="mini-card-top">
              <span class="bike-id-pill">${b.id}</span>
              <span class="license-plate-tag">${b.plateNumber}</span>
            </div>
            <div class="mini-card-model">
              <span>${b.name}</span>
              <span class="bike-tier-badge ${b.tier === 'premium' ? 'tier-premium' : 'tier-standard'}">${b.tier.toUpperCase()}</span>
            </div>
            <div class="mini-card-details">
              <span>📍 ${b.currentLocation.name.split('(')[0].trim()}</span>
              <span>⚡ Active Ride • 🔋 ${b.batteryVoltage}V</span>
            </div>
            <div class="mini-card-actions">
              <button class="btn btn-xs btn-success" onclick="AdminPortal.changeBikeStatus('${b.id}', 'available')">
                🏁 Complete Return
              </button>
              <button class="btn btn-xs btn-secondary" onclick="AdminPortal.changeBikeStatus('${b.id}', 'maintenance')">
                🔧 Send Service
              </button>
            </div>
          </div>
        `).join('');
      }
    }

    // 3. Maintenance Column Cards
    if (maintenanceContainer) {
      if (maintenanceBikes.length === 0) {
        maintenanceContainer.innerHTML = `<div class="status-empty-state">All bikes operational. Zero units in maintenance.</div>`;
      } else {
        maintenanceContainer.innerHTML = maintenanceBikes.map(b => `
          <div class="bike-status-mini-card maintenance">
            <div class="mini-card-top">
              <span class="bike-id-pill">${b.id}</span>
              <span class="license-plate-tag">${b.plateNumber}</span>
            </div>
            <div class="mini-card-model">
              <span>${b.name}</span>
              <span class="bike-tier-badge ${b.tier === 'premium' ? 'tier-premium' : 'tier-standard'}">${b.tier.toUpperCase()}</span>
            </div>
            <div class="mini-card-details">
              <span>🔧 Scheduled Inspection</span>
              <span>Depot Yard • ${b.odometerKm.toLocaleString()} km</span>
            </div>
            <div class="mini-card-actions">
              <button class="btn btn-xs btn-success" onclick="AdminPortal.changeBikeStatus('${b.id}', 'available')">
                ✅ Cleared & Ready
              </button>
            </div>
          </div>
        `).join('');
      }
    }
  },

  renderFleetTable() {
    const tbody = document.getElementById('admin-fleet-tbody');
    if (!tbody) return;

    let filtered = FLEET_DATA.filter(b => {
      if (this.activeFilter !== 'all' && b.status !== this.activeFilter) return false;
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        return b.id.toLowerCase().includes(q) ||
               b.name.toLowerCase().includes(q) ||
               b.plateNumber.toLowerCase().includes(q) ||
               b.iotDeviceId.toLowerCase().includes(q) ||
               b.currentLocation.name.toLowerCase().includes(q);
      }
      return true;
    });

    tbody.innerHTML = filtered.map(b => {
      const statusClass = b.status === 'available'
        ? 'status-available'
        : (b.status === 'rented' ? 'status-rented' : 'status-maintenance');
      const statusLabel = b.status === 'available'
        ? '● Available'
        : (b.status === 'rented' ? '● Rented (In Use)' : '● Maintenance');

      return `
        <tr>
          <td><span class="bike-id-pill">${b.id}</span></td>
          <td>
            <div class="bike-model-cell-title">${b.name}</div>
            <span class="bike-tier-badge ${b.tier === 'premium' ? 'tier-premium' : 'tier-standard'}" style="position: static; font-size: 0.68rem; margin-top: 2px;">
              ${b.tier.toUpperCase()}
            </span>
          </td>
          <td>
            <span class="license-plate-tag">${b.plateNumber}</span>
          </td>
          <td><span class="status-badge ${statusClass}">${statusLabel}</span></td>
          <td>
            <select class="status-quick-select" onchange="AdminPortal.changeBikeStatus('${b.id}', this.value)" aria-label="Change Status">
              <option value="available" ${b.status === 'available' ? 'selected' : ''}>🟢 Available</option>
              <option value="rented" ${b.status === 'rented' ? 'selected' : ''}>🔵 Rented</option>
              <option value="maintenance" ${b.status === 'maintenance' ? 'selected' : ''}>🟡 Maintenance</option>
            </select>
          </td>
          <td>
            <div style="font-weight: 700; font-size: 0.85rem;">${b.fuelLevel}% Fuel</div>
            <small style="color: var(--text-muted);">${b.batteryVoltage}V • ${b.odometerKm.toLocaleString()} km</small>
          </td>
          <td>
            <div style="font-size: 0.85rem; color: #fff;">${b.currentLocation.name}</div>
            <small style="color: var(--text-muted);">IoT: ${b.iotDeviceId}</small>
          </td>
          <td>
            <button class="btn btn-sm btn-secondary" onclick="AdminPortal.remoteTriggerAction('${b.id}')">
              ⚙️ IoT Cmd
            </button>
          </td>
        </tr>
      `;
    }).join('');
  },

  changeBikeStatus(bikeId, newStatus) {
    const bike = FLEET_DATA.find(b => b.id === bikeId);
    if (!bike) return;

    bike.status = newStatus;

    this.refreshMetrics();
    this.renderStatusBoard();
    this.renderFleetTable();
    this.initMap();

    const statusNames = {
      available: 'AVAILABLE 🟢',
      rented: 'RENTED / IN-USE 🔵',
      maintenance: 'UNDER MAINTENANCE 🟡'
    };

    if (window.App && App.showToast) {
      App.showToast(`Updated ${bike.id} [${bike.name}] (${bike.plateNumber}) status to ${statusNames[newStatus] || newStatus}`, 'success');
    }
  },

  initMap() {
    const mapContainer = document.getElementById('admin-leaflet-map');
    if (!mapContainer) return;

    if (typeof L !== 'undefined') {
      try {
        if (!this.leafletMap) {
          this.leafletMap = L.map('admin-leaflet-map').setView([13.7462, 100.5347], 12);
          L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            maxZoom: 18
          }).addTo(this.leafletMap);
        }

        this.mapMarkers.forEach(m => this.leafletMap.removeLayer(m));
        this.mapMarkers = [];

        FLEET_DATA.forEach(bike => {
          const color = bike.status === 'available' ? '#10B981' : (bike.status === 'rented' ? '#0284C7' : '#F59E0B');
          const marker = L.circleMarker([bike.currentLocation.lat, bike.currentLocation.lng], {
            radius: 8,
            fillColor: color,
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
          }).addTo(this.leafletMap);

          marker.bindPopup(`
            <div style="color: #0f172a; font-family: sans-serif; font-size: 13px;">
              <strong>${bike.name}</strong> [${bike.id}]<br>
              <strong>License Plate:</strong> ${bike.plateNumber}<br>
              <strong>Status:</strong> <span style="font-weight: 800; color: ${color};">${bike.status.toUpperCase()}</span><br>
              IoT Battery: ${bike.batteryVoltage}V | Fuel: ${bike.fuelLevel}%<br>
              Location: ${bike.currentLocation.name}
            </div>
          `);
          this.mapMarkers.push(marker);
        });
      } catch (err) {
        console.log('Leaflet initialization fallback:', err);
      }
    }
  },

  remoteTriggerAction(bikeId) {
    const bike = FLEET_DATA.find(b => b.id === bikeId);
    if (!bike) return;

    const action = prompt(`[Admin Telemetry Control]\nMotorbike: ${bike.name} (${bike.plateNumber})\nID: ${bike.id} | Device: ${bike.iotDeviceId}\nCurrent Status: ${bike.status.toUpperCase()}\n\nEnter command:\n1 = Mark Available (Parked & Ready)\n2 = Mark Rented (Dispatched)\n3 = Flag for Maintenance\n4 = Send Remote Alarm Chirp`, '1');

    if (action === '1') {
      this.changeBikeStatus(bikeId, 'available');
    } else if (action === '2') {
      this.changeBikeStatus(bikeId, 'rented');
    } else if (action === '3') {
      this.changeBikeStatus(bikeId, 'maintenance');
    } else if (action === '4') {
      if (window.App && App.showToast) {
        App.showToast(`🚨 Remote alarm chirp sent to ${bike.id} (${bike.plateNumber})!`, 'info');
      }
    }
  },

  bindEvents() {
    const filterButtons = document.querySelectorAll('.admin-filter-btn');
    const searchInput = document.getElementById('admin-fleet-search');

    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.activeFilter = btn.dataset.status;
        this.renderFleetTable();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.searchQuery = e.target.value;
        this.renderFleetTable();
      });
    }
  }
};

if (typeof window !== 'undefined') {
  window.AdminPortal = AdminPortal;
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => AdminPortal.init());
  } else {
    AdminPortal.init();
  }
}
