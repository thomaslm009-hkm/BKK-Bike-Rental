# 🛵 BKK Motorbike Rental

> **Next-Gen Smart Digital Motorbike Rental Platform in Bangkok**  
> Instant online booking, PromptPay QR checkout, and keyless IoT Smart Key access.

---

## 🌟 Overview

**BKK Motorbike Rental** solves the traditional frictions of renting a motorbike in Bangkok (physical shop visits, paper contracts, passport holding, and hidden fees) by delivering a modern, 100% digital mobility experience.

### ✨ Key Features
- 🚀 **Interactive 20-Bike Fleet**:
  - **Standard Tier (10 units)**: Honda Click 160cc, Yamaha Scoopy-i, Honda Lead 125cc (฿300/day, ฿1,900/wk, ฿5,500/mo).
  - **Premium Tier (10 units)**: Honda Forza 350cc, Yamaha XMAX 300cc, Vespa Sprint 150cc (฿450/day, ฿2,800/wk, ฿9,500/mo).
- 💳 **PromptPay QR Code Simulator**: Real-time canvas QR generation with 10-minute active payment timer & instant checkout confirmation.
- 🔑 **IoT Smart Key & Telemetry HUD**: Web Audio API vehicle unlock/lock chirps, interactive status ring, and live simulated Bangkok speedometer/odometer.
- 🗺️ **Admin Fleet Operations Portal**: Live Leaflet map plotting all 20 bikes with GPS markers, break-even progress tracker against the ฿168,000/mo fixed cost threshold, and remote vehicle immobilizers.
- 🌐 **Bilingual Localization**: Instant English (EN) and Thai (TH) toggle.
- 🛡️ **Zero Passport Seizure**: In-app digital KYC verification with automatic watermarking compliant with Thailand PDPA & DLT regulations.

---

## 📂 Project Structure

```
BKK Motorbike Rental/
├── index.html                  # Customer Storefront, Booking Flow & Smart HUD
├── admin.html                  # Admin Fleet Operations & Live Telemetry Dashboard
├── PROJECT_ANALYSIS.md         # Full Technical Blueprint & Business Analysis
├── css/
│   ├── variables.css           # Design Tokens & Palette
│   ├── style.css               # Main Stylesheet & Responsive Layouts
│   ├── components.css          # Modals, Booking Engine & Smart Key HUD
│   └── admin.css               # Admin Dashboard & Data Tables
├── js/
│   ├── data.js                 # 20-Bike Fleet Dataset & Hub Locations
│   ├── translations.js         # Bilingual EN / TH Localization Dictionary
│   ├── booking.js              # Multi-step Booking & PromptPay QR Simulator
│   ├── smart-key.js            # IoT Digital Key Fob & Web Audio Synthesizer
│   ├── admin.js                # Live Leaflet Map & Break-Even KPI Controller
│   └── app.js                  # Main Application Coordinator
├── assets/
│   └── images/                 # Vehicle photography & Bangkok skyline assets
└── Docs/
    ├── BKK Motorbike Rental.pdf
    └── Digital_Business_Project_FitBite.pptx
```

---

## 🚀 Quick Start (Local Run)

No backend or complex build pipeline required. Simply serve the directory with any local HTTP server:

```bash
# Using Python 3
python3 -m http.server 3000

# Or using Node npx serve
npx serve .
```

Then open:
- **Customer Storefront:** `http://localhost:3000/`
- **Admin Fleet Operations:** `http://localhost:3000/admin.html`

---

## 📜 License & Compliance
Compliant with Thailand **Personal Data Protection Act (PDPA)** and **Department of Land Transport (DLT)** regulations.  
© 2026 BKK Motorbike Rental Co., Ltd. All Rights Reserved.
