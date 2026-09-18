#!/usr/bin/env python3
"""
BKK Motorbike Rental — Presentation Generator
Generates a 16-slide corporate deck modeled after Digital_Business_Project_FitBite.pptx
and incorporating data from PROJECT_ANALYSIS.md and the web application.
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette (Matched to website CSS variables)
# -----------------------------------------------------------------------------
NAVY_BG      = RGBColor(10, 17, 40)       # #0A1128 (Deep Navy background)
SURFACE_BG   = RGBColor(22, 32, 68)       # #162044 (Card surface)
CARD_BG      = RGBColor(30, 41, 59)       # #1E293B (Card elevated)
GOLD_ACCENT  = RGBColor(255, 183, 3)      # #FFB703 (Bangkok Gold)
AMBER_WARM   = RGBColor(251, 133, 0)      # #FB8500 (Electric Amber)
SKY_BLUE     = RGBColor(56, 189, 248)     # #38BDF8 (Sky Blue)
ROYAL_BLUE   = RGBColor(2, 132, 199)      # #0284C7 (Royal Blue)
EMERALD      = RGBColor(16, 185, 129)     # #10B981 (Success Green)
CORAL_RED    = RGBColor(239, 68, 68)      # #EF4444 (Danger/Alert)
TEXT_WHITE   = RGBColor(255, 255, 255)    # #FFFFFF (Heading text)
TEXT_MUTED   = RGBColor(148, 163, 184)    # #94A3B8 (Body text)
BORDER_COLOR = RGBColor(51, 65, 85)       # #334155 (Subtle border)

# Asset Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_IMG = os.path.join(BASE_DIR, "assets", "images", "hero.jpg")
CLICK_IMG = os.path.join(BASE_DIR, "assets", "images", "click160.jpg")
FORZA_IMG = os.path.join(BASE_DIR, "assets", "images", "forza350.jpg")
VESPA_IMG = os.path.join(BASE_DIR, "assets", "images", "vespa.jpg")

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_blank_slide(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY_BG
    bg.line.color.rgb = NAVY_BG
    return slide

def add_header(slide, title_text, subtitle_text="", tag_text="BKK MOTORBIKE RENTAL"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if tag_text:
        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = GOLD_ACCENT
        p_tag.space_after = Pt(4)
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_after = Pt(2)

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_card_text(slide, left, top, width, height, title, text_items, title_color=GOLD_ACCENT, bg_color=CARD_BG, border_color=BORDER_COLOR):
    add_card(slide, left, top, width, height, bg_color, border_color)
    tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(14)
    p_title.font.bold = True
    p_title.font.color.rgb = title_color
    p_title.space_after = Pt(8)

    for item in text_items:
        p = tf.add_paragraph()
        p.text = f"• {item}" if not item.startswith("—") else item
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE if item.startswith("—") else TEXT_MUTED
        p.space_after = Pt(4)

def add_footer(slide, current_page=None):
    ft = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.3))
    tf = ft.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "BKK Motorbike Rental — Digital Business Proposal  |  Confidential"
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(100, 116, 139)
    if current_page:
        p2 = tf.add_paragraph()
        p2.text = str(current_page)
        p2.alignment = PP_ALIGN.RIGHT
        p2.font.size = Pt(9)
        p2.font.color.rgb = RGBColor(100, 116, 139)

# -----------------------------------------------------------------------------
# SLIDE BUILDERS (16 SLIDES)
# -----------------------------------------------------------------------------

def build_slide_0_intro(prs):
    slide = add_blank_slide(prs)

    # Hero image on right side
    if os.path.exists(HERO_IMG):
        slide.shapes.add_picture(HERO_IMG, Inches(6.8), Inches(0.8), Inches(5.8), Inches(5.8))
        add_card(slide, Inches(6.8), Inches(0.8), Inches(5.8), Inches(5.8),
                 bg_color=RGBColor(10, 17, 40), border_color=GOLD_ACCENT)
        # Re-add picture with subtle framing
        slide.shapes.add_picture(HERO_IMG, Inches(6.9), Inches(0.9), Inches(5.6), Inches(5.6))

    # Left content box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(5.6), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "🛵 DIGITAL BUSINESS PROJECT"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = GOLD_ACCENT
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "BKK MOTORBIKE RENTAL"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Smart. Seamless. Keyless Mobility in Bangkok."
    p2.font.size = Pt(16)
    p2.font.color.rgb = SKY_BLUE
    p2.space_after = Pt(20)

    p3 = tf.add_paragraph()
    p3.text = "A modern e-business proposal for an IoT-enabled 20-bike fleet rental service solving urban congestion, manual paperwork, and passport withholding in Bangkok."
    p3.font.size = Pt(11)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_after = Pt(28)

    p4 = tf.add_paragraph()
    p4.text = "Course: Digital Business & Entrepreneurship\nInitial Fleet: 20 Units (10 Standard / 10 Premium)\nTarget Market: Bangkok (Students, Expats, Tourists)"
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = RGBColor(203, 213, 225)

    add_footer(slide)

def build_slide_1_objectives(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "1. Project Objective", "Evaluating an e-business through value creation, profitability, and operational feasibility.")

    # 3 Pillar Cards
    col_w = Inches(3.64)
    gap = Inches(0.38)
    top_pos = Inches(1.8)
    h = Inches(3.8)

    add_card_text(slide, Inches(0.8), top_pos, col_w, h,
                  "1. Create Customer Value",
                  ["Eliminate friction of visiting physical shops to rent motorbikes.",
                   "Provide 100% transparent pricing with no hidden charges or surprise insurance add-ons.",
                   "Zero passport hostage: digital KYC verification instead of withholding physical passports.",
                   "Instant keyless access via mobile app and IoT smart lock technology."],
                  title_color=SKY_BLUE)

    add_card_text(slide, Inches(0.8) + col_w + gap, top_pos, col_w, h,
                  "2. Sustainable Profit",
                  ["High contribution margins: 63% to 68% across all rental tiers.",
                   "Diversified revenue: daily, weekly, and high-retention monthly packages.",
                   "Controlled cost structure with ฿168,000/month fixed overheads.",
                   "Break-even achievable at 75% fleet utilization (15 active bikes)."],
                  title_color=GOLD_ACCENT)

    add_card_text(slide, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h,
                  "3. Operational Feasibility",
                  ["Market Feasibility: High demand near BTS/MRT, universities, and expat areas.",
                   "Technical Feasibility: Lightweight PWA, PromptPay QR gateway, 4G cellular IoT.",
                   "Operational Feasibility: Central hub in Sathorn with scheduled fleet maintenance.",
                   "Legal Compliance: Thailand PDPA data privacy and DLT licensing standards."],
                  title_color=EMERALD)

    # Key Principle bottom banner
    add_card_text(slide, Inches(0.8), Inches(5.8), Inches(11.7), Inches(0.9),
                  "Key Principle",
                  ["A successful digital business is not merely innovative—it must solve a genuine customer pain point, operate smoothly in the real world, and produce resilient, sustainable profit."],
                  title_color=GOLD_ACCENT, bg_color=SURFACE_BG)
    add_footer(slide)

def build_slide_2_business_concept(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "2. Business Concept: BKK Motorbike Rental", "A mobile-first, IoT-enabled motorbike rental platform for Greater Bangkok.")

    col_w = Inches(5.66)
    top_pos = Inches(1.8)
    h = Inches(3.8)

    # Problem Card (Left)
    add_card_text(slide, Inches(0.8), top_pos, col_w, h,
                  "The Traditional Problem",
                  ["Manual & Time-Consuming: Customers must travel physically to rental shops across traffic.",
                   "Opaque Pricing: Unclear rates, arbitrary insurance fees, and unpredictable deposit deductions.",
                   "Physical Passport Withholding: Shops routinely hold customer passports as collateral, creating severe security and travel anxiety.",
                   "Paper Contracts: Slow physical paperwork leads to delays, manual errors, and dispute friction.",
                   "No Fleet Visibility: Customers cannot check live bike availability or model specs before arriving."],
                  title_color=CORAL_RED)

    # Solution Card (Right)
    add_card_text(slide, Inches(6.84), top_pos, col_w, h,
                  "The BKK Rental Solution",
                  ["Instant Digital Platform: Search, compare, and reserve motorbikes online in under 2 minutes.",
                   "Transparent Tiered Pricing: Guaranteed transparent rates with clear damage waiver options.",
                   "Digital KYC Verification: Upload passport/Thai ID with automated encryption & watermarking—no physical passport holding.",
                   "Keyless Smart IoT Access: Instant digital key in-app; unlock the bike with your phone.",
                   "Live Fleet Management: Real-time GPS tracking, automated maintenance scheduling, and instant deposit returns."],
                  title_color=EMERALD)

    # Core E-Business Flow Pill
    add_card_text(slide, Inches(0.8), Inches(5.8), Inches(11.7), Inches(0.9),
                  "Core Digital Flow",
                  ["Search Catalog Online  →  Digital KYC Upload  →  PromptPay QR Payment  →  IoT Smart Unlock  →  GPS Monitored Ride  →  Return & Instant Refund"],
                  title_color=GOLD_ACCENT, bg_color=SURFACE_BG)
    add_footer(slide)

def build_slide_3_value_prop(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "3. Value Proposition & Differentiation", "Why customers choose BKK Motorbike Rental over traditional street rental shops.")

    # 4 Pillar Grid
    w = Inches(5.66)
    h = Inches(2.2)
    top1 = Inches(1.8)
    top2 = Inches(4.2)
    left1 = Inches(0.8)
    left2 = Inches(6.84)

    add_card_text(slide, left1, top1, w, h,
                  "Affordable & Flexible",
                  ["Competitive daily (฿300/฿450), weekly (฿1,900/฿2,800), and monthly rates.",
                   "Tiered duration discounts save up to 40% on 30-day rentals.",
                   "Special student discounts and ฿500 referral credits."],
                  title_color=GOLD_ACCENT)

    add_card_text(slide, left2, top1, w, h,
                  "Personalized Fleet Choice",
                  ["Standard Fleet: Zippy Honda Click 160cc & Scoopy for agile city commuting.",
                   "Premium Fleet: Luxury Honda Forza 350cc & Vespa Sprint for comfort and touring.",
                   "Custom add-ons: full-face Bluetooth helmets, damage waivers, delivery."],
                  title_color=SKY_BLUE)

    add_card_text(slide, left1, top2, w, h,
                  "Maximum Convenience",
                  ["100% digital booking via mobile web app with instant confirmation.",
                   "Keyless IoT smart access—unlock your motorbike directly from your phone.",
                   "5 prime Bangkok pickup stations or flat ฿200 doorstep hotel delivery."],
                  title_color=EMERALD)

    add_card_text(slide, left2, top2, w, h,
                  "Total Transparency & Security",
                  ["Clear rental terms with zero hidden fees or arbitrary damage charges.",
                   "Digital rental agreement and automated instant deposit refund.",
                   "Never hold physical passports; encrypted KYC compliant with PDPA."],
                  title_color=GOLD_ACCENT)

    # Competitive Advantage callout
    add_card_text(slide, Inches(0.8), Inches(6.55), Inches(11.7), Inches(0.55),
                  "Competitive Advantage",
                  ["Combining contactless IoT locks, PromptPay QR payments, and data-driven fleet telematics."],
                  title_color=TEXT_WHITE, bg_color=SURFACE_BG)
    add_footer(slide)

def build_slide_4_target_market(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "4. Target Market & Personas", "Targeting digitally savvy urban residents, university students, expats, and tourists (Age 18–40).")

    # 4 Metric Highlights
    box_w = Inches(2.7)
    gap = Inches(0.3)
    top_pos = Inches(1.8)
    h_box = Inches(1.1)

    stats = [
        ("18 – 40 Years", "Primary Target Age Group", GOLD_ACCENT),
        ("20 Motorbikes", "Initial Pilot Fleet Size", SKY_BLUE),
        ("5 Prime Hubs", "Sathorn, Asok, Khaosan, Thonglor, Ari", EMERALD),
        ("฿300 – ฿450", "Target Average Daily Rate", GOLD_ACCENT)
    ]
    for i, (val, lbl, col) in enumerate(stats):
        x = Inches(0.8) + i * (box_w + gap)
        add_card(slide, x, top_pos, box_w, h_box, bg_color=SURFACE_BG, border_color=col)
        tb = slide.shapes.add_textbox(x + Inches(0.1), top_pos + Inches(0.15), box_w - Inches(0.2), h_box - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # 4 Customer Segment Cards
    seg_top = Inches(3.15)
    seg_w = Inches(2.7)
    seg_h = Inches(3.5)

    segments = [
        ("University Students", SKY_BLUE, [
            "Chula, ABAC, Bangkok Univ.",
            "Need cheap, daily transit between condo and campus.",
            "Prefer 7-day to 30-day Standard rentals (Click/Scoopy).",
            "Highly price-sensitive; responsive to student promo codes."
        ]),
        ("Expats & Digital Nomads", GOLD_ACCENT, [
            "Tech, finance, and English teachers living in Bangkok.",
            "Need reliable daily transport to bypass severe BTS rush hours.",
            "Prefer 30-day Premium rentals (Forza 350 / XMAX).",
            "Value transparent contracts and cashless digital payments."
        ]),
        ("Tourists & Visitors", EMERALD, [
            "Short-term vacationers and backpackers (Khaosan/Sukhumvit).",
            "Need quick 1-day to 7-day rentals for city sightseeing.",
            "Refuse physical passport confiscation.",
            "Value included safety helmets and GPS roadside assistance."
        ]),
        ("Urban Commuters", SKY_BLUE, [
            "Bangkok professionals and gig workers.",
            "Need temporary vehicle while personal car is serviced.",
            "Value rapid doorstep delivery to hotel or condo.",
            "Demand fuel-efficient, well-maintained automatic scooters."
        ])
    ]

    for i, (title, color, bullets) in enumerate(segments):
        x = Inches(0.8) + i * (seg_w + gap)
        add_card_text(slide, x, seg_top, seg_w, seg_h, title, bullets, title_color=color)

    add_footer(slide)

def build_slide_5_ebusiness_model(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "5. E-Business Model & Infrastructure", "A direct-to-consumer (B2C) digital rental model integrated with IoT smart telematics.")

    # 6-Step Process Flow
    flow_top = Inches(1.8)
    step_w = Inches(1.8)
    step_gap = Inches(0.18)
    step_h = Inches(2.1)

    steps = [
        ("1. Discover", "Google Search, Local SEO, TikTok & IG Reels, travel forums.", GOLD_ACCENT),
        ("2. Book", "Select model, rental dates, pickup hub & protection add-ons.", SKY_BLUE),
        ("3. Pay", "Instant PromptPay QR code or Credit/Debit Card checkout.", EMERALD),
        ("4. Verify", "Digital KYC: upload passport/Thai ID & driver's license.", GOLD_ACCENT),
        ("5. Unlock", "Receive Digital Key in app; tap to unlock via 4G IoT lock.", SKY_BLUE),
        ("6. Return", "Return to station, upload 4-point condition photo, deposit released.", EMERALD)
    ]

    for i, (st, desc, col) in enumerate(steps):
        x = Inches(0.8) + i * (step_w + step_gap)
        add_card(slide, x, flow_top, step_w, step_h, bg_color=SURFACE_BG, border_color=col)
        tb = slide.shapes.add_textbox(x + Inches(0.12), flow_top + Inches(0.15), step_w - Inches(0.24), step_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = st
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED

    # Digital Infrastructure Breakdown (Bottom 3 Blocks)
    infra_top = Inches(4.15)
    infra_w = Inches(3.64)
    infra_gap = Inches(0.38)
    infra_h = Inches(2.6)

    add_card_text(slide, Inches(0.8), infra_top, infra_w, infra_h,
                  "Customer Mobile App (PWA)",
                  ["Interactive vehicle catalog with live real-time inventory.",
                   "Dynamic price quote engine with duration discounts.",
                   "Digital KYC dropzone with automated image watermarking.",
                   "Smart Key HUD controller with live trip speedometer."],
                  title_color=SKY_BLUE)

    add_card_text(slide, Inches(0.8) + infra_w + infra_gap, infra_top, infra_w, infra_h,
                  "IoT Telematics Network",
                  ["4G cellular GPS trackers on all 20 motorbikes.",
                   "Encrypted MQTT broker commands for remote immobilizer.",
                   "Geofencing boundary alerts for Greater Bangkok perimeter.",
                   "Automated battery voltage and mileage telemetry logs."],
                  title_color=GOLD_ACCENT)

    add_card_text(slide, Inches(0.8) + (infra_w + infra_gap)*2, infra_top, infra_w, infra_h,
                  "Admin Operations Hub",
                  ["Live Leaflet GPS map tracking all active and parked bikes.",
                   "Financial analytics tracking ฿168,000 break-even target.",
                   "Automated maintenance triggers every 3,000 km.",
                   "Omnichannel customer support (LINE OA & WhatsApp)."],
                  title_color=EMERALD)

    add_footer(slide)

def build_slide_6_products_pricing(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "6. Products & Tiered Pricing", "Balancing customer affordability, fleet utilization, and healthy contribution margins.")

    # Pricing Table on Left
    table_left = Inches(0.8)
    table_top = Inches(1.8)
    table_w = Inches(6.8)
    table_h = Inches(3.6)

    rows = 7
    cols = 5
    table_shape = slide.shapes.add_table(rows, cols, table_left, table_top, table_w, table_h)
    table = table_shape.table

    col_widths = [Inches(1.7), Inches(1.25), Inches(1.25), Inches(1.3), Inches(1.3)]
    for idx, w in enumerate(col_widths):
        table.columns[idx].width = w

    headers = ["Product / Plan", "Customer Price", "Variable Cost", "Contribution", "Margin %"]
    data = [
        ["Standard – 1 Day", "฿300", "฿100", "฿200", "66.7%"],
        ["Standard – 7 Days", "฿1,900", "฿600", "฿1,300", "68.4%"],
        ["Standard – 30 Days", "฿5,500", "฿2,000", "฿3,500", "63.6%"],
        ["Premium – 1 Day", "฿450", "฿150", "฿300", "66.7%"],
        ["Premium – 7 Days", "฿2,800", "฿900", "฿1,900", "67.8%"],
        ["Premium – 30 Days", "฿9,500", "฿3,500", "฿6,000", "63.1%"]
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = GOLD_ACCENT
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else SURFACE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.bold = (col_idx == 0 or col_idx == 3)
            p.font.color.rgb = TEXT_WHITE if col_idx < 3 else (GOLD_ACCENT if col_idx == 3 else EMERALD)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Right Side Cards (Vehicles & Embedded Photos)
    right_w = Inches(4.7)
    right_left = Inches(7.8)

    # Standard Card with photo
    add_card(slide, right_left, Inches(1.8), right_w, Inches(2.3), bg_color=CARD_BG, border_color=BORDER_COLOR)
    if os.path.exists(CLICK_IMG):
        slide.shapes.add_picture(CLICK_IMG, right_left + Inches(0.15), Inches(1.95), Inches(1.8), Inches(1.35))
    tb_std = slide.shapes.add_textbox(right_left + Inches(2.1), Inches(1.85), Inches(2.45), Inches(2.1))
    tf_std = tb_std.text_frame
    tf_std.word_wrap = True
    p = tf_std.paragraphs[0]; p.text = "Standard Fleet (10 Units)"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = SKY_BLUE
    for bullet in ["Honda Click 160 & Scoopy-i", "15–37L underseat storage", "Deposit: ฿1k Thai / ฿2k Passport", "Ideal for: Students & commuters"]:
        p = tf_std.add_paragraph(); p.text = f"• {bullet}"; p.font.size = Pt(9); p.font.color.rgb = TEXT_MUTED

    # Premium Card with photo
    add_card(slide, right_left, Inches(4.25), right_w, Inches(2.45), bg_color=CARD_BG, border_color=BORDER_COLOR)
    if os.path.exists(FORZA_IMG):
        slide.shapes.add_picture(FORZA_IMG, right_left + Inches(0.15), Inches(4.4), Inches(1.8), Inches(1.35))
    tb_prm = slide.shapes.add_textbox(right_left + Inches(2.1), Inches(4.3), Inches(2.45), Inches(2.2))
    tf_prm = tb_prm.text_frame
    tf_prm.word_wrap = True
    p = tf_prm.paragraphs[0]; p.text = "Premium Fleet (10 Units)"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = GOLD_ACCENT
    for bullet in ["Honda Forza 350 & Vespa Sprint", "HSTC Traction control & Dual ABS", "Deposit: ฿3k Thai / ฿5k Passport", "Ideal for: Expats & highway touring"]:
        p = tf_prm.add_paragraph(); p.text = f"• {bullet}"; p.font.size = Pt(9); p.font.color.rgb = TEXT_MUTED

    # Strategy Footer Card
    add_card_text(slide, Inches(0.8), Inches(5.6), Inches(6.8), Inches(1.1),
                  "Pricing & Promotion Strategy",
                  ["Duration-based discounting protects unit contribution while incentivizing 30-day lock-in.",
                   "Optional add-ons: Zero-Deductible Damage Waiver (+฿80–฿150/d) and Doorstep Delivery (+฿200)."],
                  title_color=EMERALD, bg_color=SURFACE_BG)

    add_footer(slide)

def build_slide_7_revenue_model(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "7. Revenue Model", "Diversified revenue streams combining recurring long-term packages with short-term rentals.")

    # 4 Revenue Share Blocks
    box_w = Inches(2.7)
    gap = Inches(0.3)
    top_pos = Inches(1.8)
    h_box = Inches(1.5)

    rev_streams = [
        ("50%", "Monthly Packages", "฿5,500 – ฿9,500/mo", "Steady recurring baseline cash flow from expats, digital nomads, and university students.", GOLD_ACCENT),
        ("35%", "Weekly & Daily Rentals", "฿300 – ฿2,800", "High-margin short-term tourist demand, weekend getaways, and interim commuters.", SKY_BLUE),
        ("10%", "Protection Add-ons", "+฿80 – ฿150 / day", "Zero-deductible damage waivers, Bluetooth intercom helmet upgrades.", EMERALD),
        ("5%", "Delivery & Services", "฿200 Flat Fee", "Doorstep hotel/condo delivery, airport pickup hub handover fees.", AMBER_WARM)
    ]

    for i, (pct, title, sub, desc, col) in enumerate(rev_streams):
        x = Inches(0.8) + i * (box_w + gap)
        add_card(slide, x, top_pos, box_w, h_box, bg_color=SURFACE_BG, border_color=col)
        tb = slide.shapes.add_textbox(x + Inches(0.12), top_pos + Inches(0.1), box_w - Inches(0.24), h_box - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{pct}  {title}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED

    # Strategic Revenue Logic (Bottom Card)
    add_card_text(slide, Inches(0.8), Inches(3.6), Inches(11.7), Inches(3.1),
                  "Strategic Revenue Logic & Financial Resiliency",
                  ["1. Predictable Anchor Cash Flow: By securing 50% of the 20-bike fleet on 30-day monthly contracts (approx. 10 bikes = ฿75,000/month), the business locks in 45% of its fixed cost coverage regardless of daily tourism fluctuations.",
                   "2. High Contribution Daily/Weekly Rentals: The remaining 10 bikes generate flexible daily and weekly rentals at ฿300–฿450/day. At an average 75% utilization, they contribute an additional ฿80,000–฿100,000 in monthly margin.",
                   "3. High Margin Ancillary Services: Optional Zero-Deductible Damage Waivers (฿80–฿150/day) carry over 75% gross margin after factoring actuarial repair incident reserves.",
                   "4. Deposit Float Management: Refundable security deposits (฿1,000 to ฿5,000 per vehicle) provide an interest-free operating reserve protecting against accidental damage, speeding citations, or vehicle abandonment."],
                  title_color=GOLD_ACCENT)

    add_footer(slide)

def build_slide_8_cost_structure(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "8. Cost Structure", "Lean variable operating costs per rental day and transparent monthly fixed overheads.")

    # Left: Variable Costs breakdown
    left_w = Inches(4.8)
    top_pos = Inches(1.8)
    h_left = Inches(4.9)

    add_card_text(slide, Inches(0.8), top_pos, left_w, h_left,
                  "Variable Costs (Per Rental Day)",
                  ["Maintenance & Lubricants: ฿35 / day\n   (Engine oil, filters, scheduled CVT belt replacements)",
                   "Vehicle Sanitization & Cleaning: ฿15 / day\n   (Disinfected helmets, washed body panels)",
                   "Wear & Tear Allowance: ฿25 / day\n   (Tire wear, brake pads, battery lifecycle amortization)",
                   "Commercial Insurance Allocation: ฿15 / day\n   (Per-rental liability & compulsory Por Ror Bor pool)",
                   "Payment Processing & Telematics: ฿10 / day\n   (PromptPay QR / card gateway fees & IoT data packets)",
                   "—— Total Variable Cost (Standard): ฿100 / day",
                   "—— Total Variable Cost (Premium): ฿150 / day",
                   "Cost Control Priority: Standardized preventative maintenance every 3,000 km lowers long-term repair costs by 35%."],
                  title_color=SKY_BLUE)

    # Right: Fixed Costs Table
    right_w = Inches(6.6)
    right_left = Inches(5.9)

    table_shape = slide.shapes.add_table(11, 2, right_left, top_pos, right_w, Inches(4.9))
    table = table_shape.table
    table.columns[0].width = Inches(4.5)
    table.columns[1].width = Inches(2.1)

    fixed_costs = [
        ("Fixed Cost Category", "Monthly (THB)"),
        ("Motorcycle Fleet Financing (20 bikes amortized)", "฿30,000"),
        ("Staff Salaries (Operations, Mechanic, Customer Support)", "฿80,000"),
        ("Office & Storage Yard Rent (Sathorn Depot)", "฿20,000"),
        ("Commercial Fleet Insurance Policy", "฿15,000"),
        ("Marketing, Social Ads & Influencers", "฿5,000"),
        ("Software / App Hosting / SaaS Cloud Services", "฿3,000"),
        ("4G GPS / IoT Telematics SIM Cards", "฿3,000"),
        ("Licensing, Permits & DLT Compliance", "฿3,000"),
        ("Administrative Expenses & Utilities", "฿4,000"),
        ("Emergency Contingency Reserve", "฿5,000")
    ]

    for row_idx, (cat, amt) in enumerate(fixed_costs):
        c0 = table.cell(row_idx, 0)
        c1 = table.cell(row_idx, 1)
        is_header = (row_idx == 0)
        bg = SURFACE_BG if is_header else (CARD_BG if row_idx % 2 == 1 else SURFACE_BG)
        c0.fill.solid(); c0.fill.fore_color.rgb = bg
        c1.fill.solid(); c1.fill.fore_color.rgb = bg

        p0 = c0.text_frame.paragraphs[0]
        p0.text = cat
        p0.font.size = Pt(9.5)
        p0.font.bold = is_header
        p0.font.color.rgb = GOLD_ACCENT if is_header else TEXT_WHITE

        p1 = c1.text_frame.paragraphs[0]
        p1.text = amt
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = GOLD_ACCENT if is_header else SKY_BLUE
        p1.alignment = PP_ALIGN.RIGHT

    add_footer(slide)

def build_slide_9_monthly_profit(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "9. Monthly Profitability Projection", "Base-case forecast: 80% fleet utilization across 20 bikes (480 active rental days/month).")

    # 4 Highlight Cards
    box_w = Inches(2.7)
    gap = Inches(0.3)
    top_pos = Inches(1.8)
    h_box = Inches(1.3)

    highlights = [
        ("฿285,000", "Monthly Revenue", "Based on 80% blended utilization", GOLD_ACCENT),
        ("฿60,000", "Total Variable Costs", "฿125 avg VC × 480 rental days", SKY_BLUE),
        ("฿168,000", "Total Fixed Costs", "All overheads, salaries & rent", AMBER_WARM),
        ("฿57,000", "Net Operating Profit", "+20.0% Net Operating Margin", EMERALD)
    ]

    for i, (val, lbl, sub, col) in enumerate(highlights):
        x = Inches(0.8) + i * (box_w + gap)
        add_card(slide, x, top_pos, box_w, h_box, bg_color=SURFACE_BG, border_color=col)
        tb = slide.shapes.add_textbox(x + Inches(0.12), top_pos + Inches(0.1), box_w - Inches(0.24), h_box - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.alignment = PP_ALIGN.CENTER
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Sensitivity Table (Bottom)
    table_left = Inches(0.8)
    table_top = Inches(3.4)
    table_w = Inches(11.7)
    table_h = Inches(2.4)

    table_shape = slide.shapes.add_table(5, 5, table_left, table_top, table_w, table_h)
    table = table_shape.table

    for idx, w in enumerate([Inches(2.5), Inches(2.3), Inches(2.3), Inches(2.3), Inches(2.3)]):
        table.columns[idx].width = w

    scenarios = [
        ("Fleet Utilization Level", "Monthly Revenue", "Variable Costs", "Fixed Costs", "Net Operating Profit"),
        ("60% Low Season", "฿185,000", "฿45,000", "฿168,000", "-฿28,000 (Loss)"),
        ("75% Break-Even", "฿255,000", "฿60,000", "฿168,000", "+฿2,000 (Break-Even)"),
        ("80% Base Case", "฿285,000", "฿60,000", "฿168,000", "+฿57,000 (Healthy)"),
        ("95% Peak Tourist Season", "฿380,000", "฿85,000", "฿168,000", "+฿127,000 (High Profit)")
    ]

    for r_idx, r_data in enumerate(scenarios):
        for c_idx, val in enumerate(r_data):
            cell = table.cell(r_idx, c_idx)
            is_hdr = (r_idx == 0)
            cell.fill.solid()
            cell.fill.fore_color.rgb = SURFACE_BG if is_hdr else (CARD_BG if r_idx % 2 == 1 else SURFACE_BG)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.bold = (is_hdr or c_idx == 4 or c_idx == 0)
            if is_hdr:
                p.font.color.rgb = GOLD_ACCENT
            elif c_idx == 4:
                p.font.color.rgb = CORAL_RED if "Loss" in val else EMERALD
            else:
                p.font.color.rgb = TEXT_WHITE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Annualized note
    add_card_text(slide, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.85),
                  "Annualized Outlook",
                  ["At the base case (80% utilization): Projected Annual Gross Revenue = ฿3,420,000  |  Projected Annual Net Operating Profit = ฿684,000."],
                  title_color=GOLD_ACCENT, bg_color=SURFACE_BG)

    add_footer(slide)

def build_slide_10_breakeven(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "10. Break-Even Analysis", "Determining the sales volume and fleet utilization required to cover all monthly overheads.")

    # Top 3 Break-Even Metric Callouts
    top_pos = Inches(1.8)
    w_box = Inches(3.64)
    gap = Inches(0.38)
    h_box = Inches(1.6)

    be_metrics = [
        ("฿252,631", "Break-Even Revenue / Month", "Total sales required to cover ฿168,000 fixed costs.", GOLD_ACCENT),
        ("75% Utilization", "Break-Even Fleet Utilization", "15 of 20 motorbikes rented across the month.", SKY_BLUE),
        ("66.5%", "Average Contribution Margin", "Blended ratio across Standard & Premium packages.", EMERALD)
    ]

    for i, (val, title, desc, col) in enumerate(be_metrics):
        x = Inches(0.8) + i * (w_box + gap)
        add_card(slide, x, top_pos, w_box, h_box, bg_color=SURFACE_BG, border_color=col)
        tb = slide.shapes.add_textbox(x + Inches(0.15), top_pos + Inches(0.15), w_box - Inches(0.3), h_box - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.alignment = PP_ALIGN.CENTER
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Formula Card & Management Insights (Bottom Split)
    split_top = Inches(3.65)
    split_w = Inches(5.66)
    split_h = Inches(3.1)

    add_card_text(slide, Inches(0.8), split_top, split_w, split_h,
                  "Mathematical Break-Even Model",
                  ["Break-Even Revenue Formula:\n   BEP (Revenue) = Fixed Costs ÷ Contribution Margin Ratio",
                   "Calculation:\n   BEP = ฿168,000 ÷ 0.665 ≈ ฿252,631 per month",
                   "Break-Even Rental Days (Daily equivalent):\n   ฿168,000 ÷ ฿250 (avg contribution/day) ≈ 672 bike-days",
                   "Fleet Capacity Reality Check:\n   20 bikes × 30 days = 600 available days on pure daily rentals.\n   Therefore, long-term monthly & weekly contracts are essential to bridge the gap and achieve break-even at 75% utilization."],
                  title_color=GOLD_ACCENT)

    add_card_text(slide, Inches(6.84), split_top, split_w, split_h,
                  "Operational Management Takeaways",
                  ["1. The 15-Bike Rule: Operations must always maintain a baseline of at least 15 active rental contracts to prevent operating losses.",
                   "2. Lock in Long-Term Baseline: Target 10 monthly expat/student contracts (50% fleet) to immediately secure ฿75,000 towards fixed costs.",
                   "3. Protect High Margins on Remainder: The remaining 10 bikes capture premium tourist daily and weekly rentals (67%+ margin).",
                   "4. Buffer Margin: The 80% target utilization (16 active bikes) provides a comfortable ฿57,000 monthly safety buffer above break-even."],
                  title_color=EMERALD)

    add_footer(slide)

def build_slide_11_marketing(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "11. Digital Marketing Strategy", "Prioritizing digital discovery channels where Bangkok expats, students, and tourists look for mobility.")

    # 5 Funnel Stages Cards
    col_w = Inches(2.2)
    gap = Inches(0.17)
    top_pos = Inches(1.8)
    h = Inches(3.6)

    channels = [
        ("1. Google & Local SEO", SKY_BLUE, [
            "High-intent search capture.",
            "'Motorbike rental Bangkok', 'Rent scooter Sathorn / Asok'.",
            "Optimized Google Business Profile with 5-star verified reviews.",
            "Rank #1 on Google Maps for BTS/MRT commuter keywords."
        ]),
        ("2. TikTok & IG Reels", GOLD_ACCENT, [
            "Visual discovery & lifestyle.",
            "Short videos: 'How to rent a bike in Bangkok with your phone'.",
            "Hidden Bangkok scooter riding routes and food tour guides.",
            "Micro-influencer collaborations with local expat creators."
        ]),
        ("3. LINE Official Account", EMERALD, [
            "Retention & quick support.",
            "Automated extension reminders and instant rental renewal.",
            "Live chat customer service & emergency SOS hotline.",
            "Exclusive subscriber discounts for recurring renters."
        ]),
        ("4. Strategic Hubs", AMBER_WARM, [
            "Physical-to-digital partnerships.",
            "Coworking spaces in Thonglor (WeWork, The Hive).",
            "Hostels in Khaosan & Sukhumvit with QR booking stands.",
            "Direct referral commissions for hostel receptionists."
        ]),
        ("5. Referral Program", GOLD_ACCENT, [
            "Viral organic growth.",
            "'Refer a Friend': ฿500 rental discount for the new rider.",
            "฿500 credit for the referring customer on their next month.",
            "Lowers Customer Acquisition Cost (CAC) below ฿200."
        ])
    ]

    for i, (title, color, bullets) in enumerate(channels):
        x = Inches(0.8) + i * (col_w + gap)
        add_card_text(slide, x, top_pos, col_w, h, title, bullets, title_color=color)

    # Conversion Funnel Strip
    add_card_text(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.15),
                  "Priority Acquisition Funnel",
                  ["Discover (SEO / TikTok)  →  Trust (Reviews / Zero Passport Hold)  →  Trial (Instant PromptPay QR)  →  Repeat (Monthly Package)  →  Refer (฿500 Credit)"],
                  title_color=GOLD_ACCENT, bg_color=SURFACE_BG)

    add_footer(slide)

def build_slide_12_competitor_analysis(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "12. Competitor Analysis", "Benchmarking BKK Motorbike Rental against key market competitors in Bangkok.")

    # Comparison Table
    table_left = Inches(0.8)
    table_top = Inches(1.8)
    table_w = Inches(11.7)
    table_h = Inches(3.6)

    table_shape = slide.shapes.add_table(7, 5, table_left, table_top, table_w, table_h)
    table = table_shape.table

    col_widths = [Inches(2.2), Inches(2.4), Inches(2.4), Inches(2.4), Inches(2.3)]
    for idx, w in enumerate(col_widths):
        table.columns[idx].width = w

    headers = ["Feature / Factor", "BKK Motorbike Rental", "MadBike.co", "Fatboy's Motorbike", "Traditional Street Shops"]
    comp_data = [
        ["Positioning", "Smart IoT + Transparent", "Multi-station + Western", "Established Expat Brand", "Informal Local Shops"],
        ["Daily Price (Standard)", "฿300 / day", "฿300 – ฿350 / day", "฿300 – ฿350 / day", "฿200 – ฿300 / day"],
        ["Booking Experience", "100% Instant Digital PWA", "Static Form / WhatsApp", "WhatsApp / In-person", "Physical Walk-in Only"],
        ["Payment Methods", "PromptPay QR, Card, App", "Cash, Card, Transfer", "Cash, Card, Transfer", "Cash Only"],
        ["Passport Policy", "Digital KYC (No Holding)", "Passport Photocopy", "Original Passport Hold", "Hold Original Passport"],
        ["Key Access & Security", "Smart Key IoT Unlock + GPS", "Physical Key Only", "Physical Key Only", "Physical Key (No GPS)"]
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = GOLD_ACCENT if col_idx == 1 else TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    for row_idx, row_data in enumerate(comp_data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else SURFACE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.bold = (col_idx == 1)
            p.font.color.rgb = GOLD_ACCENT if col_idx == 1 else (TEXT_WHITE if col_idx == 0 else TEXT_MUTED)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Competitive Gap Banner
    add_card_text(slide, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1),
                  "The BKK Motorbike Rental Competitive Gap",
                  ["Win by eliminating traditional rental friction: 100% digital instant checkout + keyless IoT unlock + zero physical passport withholding, while matching or beating market pricing."],
                  title_color=EMERALD, bg_color=SURFACE_BG)

    add_footer(slide)

def build_slide_13_feasibility(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "13. Feasibility Analysis", "Evaluating the proposal across the 5 standard e-business feasibility dimensions.")

    # 5 Feasibility Dimensions
    w_card = Inches(2.2)
    gap = Inches(0.17)
    top_pos = Inches(1.8)
    h_card = Inches(3.6)

    dims = [
        ("Market Feasibility", SKY_BLUE, [
            "Plausible & Growing Demand.",
            "Bangkok traffic congestion creates heavy preference for scooters.",
            "Growing digital nomad population and international tourism recovery.",
            "Strong user preference for contactless mobile ordering."
        ]),
        ("Technical Feasibility", GOLD_ACCENT, [
            "Low Engineering Risk.",
            "Progressive Web App (PWA) requires no App Store submission friction.",
            "Cellular 4G IoT telematics and smart locks are off-the-shelf hardware.",
            "Thai PromptPay QR payment gateways are mature and standardized."
        ]),
        ("Operational Feasibility", EMERALD, [
            "Controlled & Repeatable.",
            "Central Sathorn maintenance depot handles fleet repairs and storage.",
            "Standardized 4-point return inspection SOP.",
            "Doorstep delivery managed within 15km zone to avoid logistics drag."
        ]),
        ("Financial Feasibility", GOLD_ACCENT, [
            "Positive Unit Economics.",
            "63%–68% contribution margin covers variable operations comfortably.",
            "Break-even achievable at 75% fleet utilization (15 active bikes).",
            "Base case yields ฿57,000 monthly net profit (20% net margin)."
        ]),
        ("Legal & Ethical", SKY_BLUE, [
            "Full Regulatory Compliance.",
            "Compliant with Thailand PDPA (encrypted KYC storage).",
            "Mandatory DLT-compliant driver license / IDP validation.",
            "Every vehicle backed by Compulsory Motor Insurance (Por Ror Bor)."
        ])
    ]

    for i, (title, color, bullets) in enumerate(dims):
        x = Inches(0.8) + i * (w_card + gap)
        add_card_text(slide, x, top_pos, w_card, h_card, title, bullets, title_color=color)

    # Pilot First Recommendation
    add_card_text(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.15),
                  "Strategic Pilot-First Execution",
                  ["Start with 20 motorbikes in central Bangkok (Sathorn & Sukhumvit). Validate real customer acquisition cost (CAC), maintenance wear, and repeat retention before scaling to 50+ bikes."],
                  title_color=EMERALD, bg_color=SURFACE_BG)

    add_footer(slide)

def build_slide_14_risk_analysis(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "14. Risk Analysis & Mitigation Matrix", "Identifying potential business risks and management mitigation strategies.")

    table_left = Inches(0.8)
    table_top = Inches(1.8)
    table_w = Inches(11.7)
    table_h = Inches(4.8)

    table_shape = slide.shapes.add_table(7, 3, table_left, table_top, table_w, table_h)
    table = table_shape.table

    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(3.6)
    table.columns[2].width = Inches(5.5)

    headers = ["Risk Identified", "Potential Business Impact", "Management Mitigation Strategy"]
    risks_data = [
        ("Motorbike Theft / Unauthorized Cross-Border Travel",
         "Asset loss, police reporting overhead, fleet shrinkage.",
         "4G cellular GPS trackers with real-time Bangkok geofencing. Automatic remote engine immobilization if exiting perimeter; police integration."),
        ("Traffic Accidents & Body Damage",
         "Repair expense, customer conflict, bike out-of-service downtime.",
         "Compulsory Por Ror Bor insurance pool; optional Zero-Deductible Damage Waiver (+฿80/d); mandatory pre/post 4-angle photo audit in-app."),
        ("Low Off-Peak Tourist Demand",
         "Fleet utilization drops below 75% break-even threshold.",
         "Shift fleet focus to 30-day student and expat corporate commuter packages; offer seasonal promotional discounts."),
        ("Unlicensed Tourist Drivers & Police Fines",
         "Customer impoundment, legal liability, reputational blow.",
         "Mandatory digital KYC checking for valid Thai license or International Driving Permit (IDP 1949/1968); digital helmet checks."),
        ("IoT Lock / Cellular Telematics Failure",
         "Customer locked out or unable to start active trip.",
         "Dual-SIM fallback on telematics unit; manual physical master key backup in tamper-evident sealed compartment on each bike."),
        ("Deposit Withholding Disputes",
         "Negative reviews on Google Maps / Trustpilot.",
         "100% transparent automated photo comparison at check-out vs return. Instant automated PromptPay deposit refund release within 1 hour.")
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SURFACE_BG
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = GOLD_ACCENT
        p.alignment = PP_ALIGN.LEFT

    for row_idx, (r_name, r_imp, r_mit) in enumerate(risks_data, start=1):
        for col_idx, text in enumerate([r_name, r_imp, r_mit]):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else SURFACE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = CORAL_RED
            elif col_idx == 1:
                p.font.color.rgb = TEXT_MUTED
            else:
                p.font.color.rgb = TEXT_WHITE
            p.alignment = PP_ALIGN.LEFT

    add_footer(slide)

def build_slide_15_conclusion(prs):
    slide = add_blank_slide(prs)

    # Header
    add_header(slide, "Conclusion & Recommendation", "Executive decision and final business viability assessment.")

    left_w = Inches(6.8)
    top_pos = Inches(1.8)
    h_left = Inches(4.8)

    # Left Recommendation Card
    add_card_text(slide, Inches(0.8), top_pos, left_w, h_left,
                  "Should BKK Motorbike Rental Be Launched? YES.",
                  ["1. Clear Customer Problem & Market Fit: Bangkok commuters and tourists face extreme traffic yet endure opaque, untrustworthy, paper-heavy motorbike rental services. The demand for digital transparency is high.",
                   "2. Mature & Accessible Technology: Lightweight mobile web app, PromptPay QR integration, and 4G IoT smart locks can be implemented without expensive custom hardware development.",
                   "3. Financially Sound Base Case: Operating at 80% fleet utilization yields an estimated net profit of ฿57,000/month (฿684,000 annualized) on a lean 20-bike fleet.",
                   "4. Measurable Break-Even Target: A distinct break-even target of 75% utilization (15 active bikes) gives management clear operational focus.",
                   "5. Decisive Advantage over Street Shops: Zero passport confiscation + instant keyless IoT unlock creates overwhelming consumer trust."],
                  title_color=GOLD_ACCENT)

    # Right Box: Decision Rule & Thank You with Vespa visual
    right_w = Inches(4.6)
    right_left = Inches(7.9)

    add_card_text(slide, right_left, top_pos, right_w, Inches(1.8),
                  "Executive Decision Rule",
                  ["Launch a 3-month controlled pilot (20 bikes in Sathorn/Sukhumvit).",
                   "Scale fleet to 50+ bikes only when customer retention, unit maintenance costs, and 80%+ utilization are proven."],
                  title_color=EMERALD, bg_color=SURFACE_BG)

    # Thank you card with embedded photo
    add_card(slide, right_left, Inches(3.8), right_w, Inches(2.8), bg_color=CARD_BG, border_color=GOLD_ACCENT)
    if os.path.exists(VESPA_IMG):
        slide.shapes.add_picture(VESPA_IMG, right_left + Inches(0.2), Inches(3.95), Inches(2.0), Inches(1.5))
    tb_ty = slide.shapes.add_textbox(right_left + Inches(2.3), Inches(3.9), Inches(2.1), Inches(2.5))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True
    p = tf_ty.paragraphs[0]; p.text = "🛵 BKK RENTAL"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = GOLD_ACCENT; p.space_after = Pt(4)
    p = tf_ty.add_paragraph(); p.text = "Smart. Seamless. Keyless Mobility."; p.font.size = Pt(10); p.font.color.rgb = SKY_BLUE; p.space_after = Pt(8)
    p = tf_ty.add_paragraph(); p.text = "Thank You!\nReady for questions & discussion."; p.font.size = Pt(10); p.font.color.rgb = TEXT_WHITE

    add_footer(slide)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    prs = create_deck()
    print("Building 16-slide BKK Motorbike Rental Presentation...")

    build_slide_0_intro(prs)
    build_slide_1_objectives(prs)
    build_slide_2_business_concept(prs)
    build_slide_3_value_prop(prs)
    build_slide_4_target_market(prs)
    build_slide_5_ebusiness_model(prs)
    build_slide_6_products_pricing(prs)
    build_slide_7_revenue_model(prs)
    build_slide_8_cost_structure(prs)
    build_slide_9_monthly_profit(prs)
    build_slide_10_breakeven(prs)
    build_slide_11_marketing(prs)
    build_slide_12_competitor_analysis(prs)
    build_slide_13_feasibility(prs)
    build_slide_14_risk_analysis(prs)
    build_slide_15_conclusion(prs)

    output_path = os.path.join(BASE_DIR, "BKK_Motorbike_Rental_Presentation.pptx")
    prs.save(output_path)
    print(f"✅ Successfully saved presentation to: {output_path}")

if __name__ == "__main__":
    main()
