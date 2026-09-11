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

    // Calculate revenue based on rental active units + standard estimates
    // Standard rented (฿5,500/mo blended) + Premium rented (฿9,500/mo blended)
    let currentMonthlyRevenue = 0;
    FLEET_DATA.forEach(bike => {
      if (bike.status === 'rented') {
        currentMonthlyRevenue += bike.tier === 'premium' ? 9500 : 5500;
      }
    });

    // Add baseline day-rate transactions for demo
    currentMonthlyRevenue += 84500; // base accumulated this month

    const FIXED_COST_BREAKEVEN = 168000;
    const breakevenPct = Math.min(100, Math.round((currentMonthlyRevenue / FIXED_COST_BREAKEVEN) * 100));

    // Update DOM
    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setTxt('admin-kpi-utilization', `${utilizationPct}%`);
    setTxt('admin-kpi-active-rentals', `${rented} / ${totalBikes}`);
    setTxt('admin-kpi-revenue', `฿${currentMonthlyRevenue.toLocaleString()}`);
    setTxt('admin-kpi-maintenance', `${maintenance} Units`);
    setTxt('admin-breakeven-progress-text', `${breakevenPct}% of ฿168,000 Fixed Cost Target`);
    setTxt('admin-breakeven-current-rev', `฿${currentMonthlyRevenue.toLocaleString()}`);

    const fill = document.getElementById('admin-breakeven-fill');
    if (fill) fill.style.width = `${breakevenPct}%`;
  },

  renderFleetTable() {
    const tbody = document.getElementById('admin-fleet-tbody');
    if (!tbody) return;

    let filtered = FLEET_DATA.filter(b => {
      if (this.activeFilter !== 'all' && b.status !== this.activeFilter) return false;
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        return b.name.toLowerCase().includes(q) || b.plateNumber.toLowerCase().includes(q) || b.iotDeviceId.toLowerCase().includes(q);
      }
      return true;
    });

    tbody.innerHTML = filtered.map(b => {
      const statusClass = b.status === 'available' ? 'status-available' : (b.status === 'rented' ? 'status-rented' : 'status-maintenance');
      const statusLabel = b.status === 'available' ? '● Available' : (b.status === 'rented' ? '● Active Ride' : '● In Service');

      return `
        <tr>
          <td><strong>${b.id}</strong></td>
          <td>
            <div style="font-weight: 700;">${b.name}</div>
            <small style="color: var(--text-muted);">${b.plateNumber}</small>
          </td>
          <td>
            <span class="bike-tier-badge ${b.tier === 'premium' ? 'tier-premium' : 'tier-standard'}" style="position: static; font-size: 0.7rem;">
              ${b.tier.toUpperCase()}
            </span>
          </td>
          <td><span class="status-badge ${statusClass}">${statusLabel}</span></td>
          <td>
            <div style="font-size: 0.85rem;">${b.fuelLevel}% Fuel</div>
            <small style="color: var(--text-muted);">${b.batteryVoltage}V Battery</small>
          </td>
          <td><small>${b.currentLocation.name}</small></td>
          <td>
            <button class="btn btn-sm btn-secondary" onclick="AdminPortal.remoteTriggerAction('${b.id}')">
              ⚙️ Manage
            </button>
          </td>
        </tr>
      `;
    }).join('');
  },

  initMap() {
    const mapContainer = document.getElementById('admin-leaflet-map');
    if (!mapContainer) return;

    // Check if Leaflet L exists
    if (typeof L !== 'undefined') {
      try {
        if (!this.leafletMap) {
          this.leafletMap = L.map('admin-leaflet-map').setView([13.7462, 100.5347], 12);
          L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            maxZoom: 18
          }).addTo(this.leafletMap);
        }

        // Clear existing markers
        this.mapMarkers.forEach(m => this.leafletMap.removeLayer(m));
        this.mapMarkers = [];

        // Plot all 20 bikes
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
              <strong>${bike.name}</strong> (${bike.tier.toUpperCase()})<br>
              Plate: ${bike.plateNumber}<br>
              Status: <b>${bike.status.toUpperCase()}</b><br>
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

    const action = prompt(`[Admin Telemetry Control]\nMotorbike: ${bike.name} (${bike.plateNumber})\nIoT Device: ${bike.iotDeviceId}\n\nEnter command:\n1 = Lock / Immobilize\n2 = Unlock\n3 = Flag for Maintenance\n4 = Clear to Available`, '1');

    if (action === '1') {
      bike.status = 'available';
      App.showToast(`🔒 Immobilizer signal sent to ${bike.name}. Vehicle Secured.`, 'info');
    } else if (action === '2') {
      bike.status = 'rented';
      App.showToast(`🔓 Remote Unlock authorized for ${bike.name}.`, 'success');
    } else if (action === '3') {
      bike.status = 'maintenance';
      App.showToast(`⚠️ ${bike.name} flagged for mechanic scheduled inspection.`, 'danger');
    } else if (action === '4') {
      bike.status = 'available';
      App.showToast(`✅ ${bike.name} cleared to Available Fleet.`, 'success');
    }

    this.refreshMetrics();
    this.renderFleetTable();
    this.initMap();
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
