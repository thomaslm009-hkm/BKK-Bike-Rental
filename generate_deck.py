#!/usr/bin/env python3
"""
BKK Motorbike Rental — Presentation Generator (Clean White Visual Redesign)
Features:
- Clean white/off-white background with BKK Rental brand colors (Navy, Gold, Blue, Emerald).
- High visual appeal with concise, scannable text (less clutter).
- Native PowerPoint charts (Doughnut chart on Slide 7, Clustered Column chart on Slide 9).
- Embedded vehicle photography (Click 160, Forza 350, Vespa Sprint, Bangkok skyline).
"""

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

# -----------------------------------------------------------------------------
# Color Palette (BKK Motorbike Rental Design System)
# -----------------------------------------------------------------------------
BG_WHITE      = RGBColor(255, 255, 255)   # Clean White
BG_SLATE      = RGBColor(248, 250, 252)   # #F8FAFC (Subtle soft background)
CARD_BG       = RGBColor(241, 245, 249)   # #F1F5F9 (Light card background)
CARD_BORDER   = RGBColor(226, 232, 240)   # #E2E8F0 (Subtle border)

NAVY_PRIMARY  = RGBColor(10, 17, 40)      # #0A1128 (Brand Dark Navy)
NAVY_LIGHT    = RGBColor(22, 32, 68)      # #162044
GOLD_ACCENT   = RGBColor(245, 158, 11)    # #F59E0B / #FFB703 (Bangkok Gold)
AMBER_WARM    = RGBColor(234, 88, 12)     # #EA580C / #FB8500 (Warm Amber)
ROYAL_BLUE    = RGBColor(2, 132, 199)     # #0284C7 (Primary Blue)
SKY_BLUE      = RGBColor(14, 165, 233)    # #0EA5E9 (Accent Cyan/Blue)
EMERALD       = RGBColor(16, 185, 129)    # #10B981 (Success Green)
CORAL_RED     = RGBColor(239, 68, 68)     # #EF4444 (Alert/Risk)

TEXT_DARK     = RGBColor(15, 23, 42)      # #0F172A (Headings & Key text)
TEXT_BODY     = RGBColor(51, 65, 85)      # #334155 (Readable dark text)
TEXT_MUTED    = RGBColor(100, 116, 139)   # #64748B (Secondary text)
TEXT_WHITE    = RGBColor(255, 255, 255)

# Asset Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HERO_IMG = os.path.join(BASE_DIR, "assets", "images", "hero.jpg")
CLICK_IMG = os.path.join(BASE_DIR, "assets", "images", "click160.jpg")
FORZA_IMG = os.path.join(BASE_DIR, "assets", "images", "forza350.jpg")
VESPA_IMG = os.path.join(BASE_DIR, "assets", "images", "vespa.jpg")

# -----------------------------------------------------------------------------
# Base Helper Functions
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
    bg.fill.fore_color.rgb = BG_WHITE
    bg.line.color.rgb = BG_WHITE
    return slide

def add_header(slide, title_text, subtitle_text="", tag_text="BKK MOTORBIKE RENTAL"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if tag_text:
        p_tag = tf.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ROYAL_BLUE
        p_tag.space_after = Pt(2)
        p_title = tf.add_paragraph()
    else:
        p_title = tf.paragraphs[0]

    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_PRIMARY
    p_title.space_after = Pt(2)

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=BG_SLATE, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def add_card_box(slide, left, top, width, height, title, items, title_color=NAVY_PRIMARY, bg_color=BG_SLATE, border_color=CARD_BORDER, top_bar_color=None):
    add_card(slide, left, top, width, height, bg_color, border_color)
    
    # Optional top accent color line
    if top_bar_color:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = top_bar_color
        bar.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.32))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(13)
    p_title.font.bold = True
    p_title.font.color.rgb = title_color
    p_title.space_after = Pt(6)

    for item in items:
        p = tf.add_paragraph()
        if item.startswith("—"):
            p.text = item
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = NAVY_PRIMARY
        else:
            p.text = f"• {item}"
            p.font.size = Pt(9.8)
            p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(4)

def add_stat_box(slide, left, top, width, height, number_str, label_str, accent_color=ROYAL_BLUE):
    add_card(slide, left, top, width, height, bg_color=BG_SLATE, border_color=CARD_BORDER)
    # top accent strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent_color
    strip.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.12), width - Inches(0.2), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = number_str
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = accent_color
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = label_str
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

def add_footer(slide, current_page=None):
    ft = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
    tf = ft.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "BKK Motorbike Rental  |  Digital Business Project  |  Bangkok, Thailand"
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED
    if current_page:
        p2 = tf.add_paragraph()
        p2.text = str(current_page)
        p2.alignment = PP_ALIGN.RIGHT
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED

# -----------------------------------------------------------------------------
# SLIDE BUILDERS (16 SLIDES — CLEAN WHITE & VISUAL)
# -----------------------------------------------------------------------------

def build_slide_0_intro(prs):
    slide = add_blank_slide(prs)

    # Hero image framed on right
    if os.path.exists(HERO_IMG):
        slide.shapes.add_picture(HERO_IMG, Inches(6.8), Inches(0.9), Inches(5.7), Inches(5.6))
        # Subtle card framing
        add_card(slide, Inches(6.75), Inches(0.85), Inches(5.8), Inches(5.7), bg_color=BG_WHITE, border_color=CARD_BORDER)
        slide.shapes.add_picture(HERO_IMG, Inches(6.85), Inches(0.95), Inches(5.6), Inches(5.5))

    # Left content box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(5.6), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True

    # Brand pill badge
    p0 = tf.paragraphs[0]
    p0.text = "🛵  BKK MOTORBIKE RENTAL"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = ROYAL_BLUE
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "Smart. Seamless.\nKeyless Mobility."
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = NAVY_PRIMARY
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "A mobile-first, IoT-enabled motorbike rental platform designed to eliminate traditional rental friction across Greater Bangkok."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_BODY
    p2.space_after = Pt(28)

    # Highlights row
    p3 = tf.add_paragraph()
    p3.text = "• Initial Fleet: 20 Bikes (10 Standard / 10 Premium)\n• Key Edge: Contactless IoT Unlock & Zero Passport Hold\n• Target: Students, Expats, Tourists & Commuters"
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    add_footer(slide)

def build_slide_1_objectives(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "1. Project Objective", "Evaluating an e-business through value creation, profitability, and operational feasibility.")

    # 3 Structured Pillar Cards
    col_w = Inches(3.64)
    gap = Inches(0.38)
    top_pos = Inches(1.8)
    h = Inches(3.7)

    add_card_box(slide, Inches(0.8), top_pos, col_w, h,
                 "Create Customer Value",
                 ["Solve shop dependency: 100% online booking in under 2 minutes.",
                  "Zero passport holding: digital KYC verifies identity safely.",
                  "Transparent pricing: no surprise insurance or hidden fees.",
                  "Smart keyless access: unlock motorbike directly via smartphone."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    add_card_box(slide, Inches(0.8) + col_w + gap, top_pos, col_w, h,
                 "Generate Sustainable Profit",
                 ["High contribution margins: 63% to 68% across all tiers.",
                  "Balanced revenue mix: monthly contracts + daily tourists.",
                  "Lean fixed overhead: ฿168,000/month across 20-bike fleet.",
                  "Break-even target: 75% fleet utilization (15 active bikes)."],
                 title_color=GOLD_ACCENT, top_bar_color=GOLD_ACCENT)

    add_card_box(slide, Inches(0.8) + (col_w + gap)*2, top_pos, col_w, h,
                 "Operational Feasibility",
                 ["Market demand: high congestion near BTS/MRT & university hubs.",
                  "Proven tech stack: lightweight PWA + 4G cellular IoT locks.",
                  "Central operations: Sathorn maintenance depot with regular SOPs.",
                  "Full legal compliance: Thailand PDPA & DLT driver rules."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    # Key Principle banner
    add_card_box(slide, Inches(0.8), Inches(5.8), Inches(11.7), Inches(0.95),
                 "Core Guiding Principle",
                 ["A great digital business solves real user pain points, operates reliably in the physical world, and generates resilient, repeatable profit."],
                 title_color=NAVY_PRIMARY, bg_color=CARD_BG, top_bar_color=NAVY_PRIMARY)
    add_footer(slide)

def build_slide_2_business_concept(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "2. Business Concept: BKK Motorbike Rental", "A mobile-first, IoT-enabled motorbike rental platform for Greater Bangkok.")

    col_w = Inches(5.66)
    top_pos = Inches(1.8)
    h = Inches(3.7)

    # Problem Card (Left)
    add_card_box(slide, Inches(0.8), top_pos, col_w, h,
                 "The Traditional Rental Problem",
                 ["Manual & Inconvenient: Must visit physical rental shops in heavy traffic.",
                  "Opaque & Hidden Fees: Arbitrary damage claims and unlisted charges.",
                  "Passport Anxiety: Shops routinely hold original passports as collateral.",
                  "Paper Contract Delays: Slow paperwork, manual errors, and deposit friction.",
                  "Zero Fleet Visibility: Cannot verify real-time availability or bike condition."],
                 title_color=CORAL_RED, top_bar_color=CORAL_RED)

    # Solution Card (Right)
    add_card_box(slide, Inches(6.84), top_pos, col_w, h,
                 "The BKK Motorbike Rental Solution",
                 ["Instant Online Booking: Search, compare, and reserve in under 2 minutes.",
                  "Guaranteed Price Transparency: Clear rates with optional zero-deductible waiver.",
                  "Digital KYC: Automated encrypted passport verification—no physical holding.",
                  "Keyless Smart IoT: Unlock the vehicle instantly via mobile digital key.",
                  "Automated Operations: GPS telematics, scheduled servicing, instant deposit refund."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    # Flow Banner
    add_card_box(slide, Inches(0.8), Inches(5.8), Inches(11.7), Inches(0.95),
                 "Core Experience Flow",
                 ["Search Catalog Online  ➔  Digital KYC Upload  ➔  PromptPay QR Payment  ➔  Smart Key IoT Unlock  ➔  GPS Safe Ride  ➔  Instant Deposit Release"],
                 title_color=ROYAL_BLUE, bg_color=CARD_BG, top_bar_color=ROYAL_BLUE)
    add_footer(slide)

def build_slide_3_value_prop(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "3. Value Proposition & Differentiation", "Why customers choose BKK Motorbike Rental over traditional street shops.")

    # 4 Cards on Left
    w_card = Inches(3.9)
    gap = Inches(0.25)
    top1 = Inches(1.8)
    top2 = Inches(4.3)
    left1 = Inches(0.8)
    left2 = Inches(4.95)
    h_card = Inches(2.25)

    add_card_box(slide, left1, top1, w_card, h_card,
                 "Affordable & Flexible",
                 ["Competitive rates: ฿300/day Std, ฿450/day Premium.",
                  "Up to 40% duration discount on 30-day packages.",
                  "Special student offers & ฿500 referral credits."],
                 title_color=GOLD_ACCENT, top_bar_color=GOLD_ACCENT)

    add_card_box(slide, left2, top1, w_card, h_card,
                 "Personalized Choice",
                 ["Standard: Agile Honda Click 160 & Scoopy-i.",
                  "Premium: Luxury Honda Forza 350 & Vespa Sprint.",
                  "Custom add-ons: Full-face helmets, damage waivers."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    add_card_box(slide, left1, top2, w_card, h_card,
                 "Frictionless Convenience",
                 ["Instant booking via PWA mobile web app.",
                  "Keyless Smart IoT unlock with haptic feedback.",
                  "5 Bangkok hubs or flat ฿200 doorstep delivery."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_card_box(slide, left2, top2, w_card, h_card,
                 "Total Transparency",
                 ["Zero hidden fees; clear digital rental agreements.",
                  "No passport holding: encrypted digital KYC.",
                  "Automated prompt deposit refund upon return."],
                 title_color=AMBER_WARM, top_bar_color=AMBER_WARM)

    # Right side: Visual Hero Card with Forza photo
    right_w = Inches(3.8)
    right_left = Inches(9.1)
    add_card(slide, right_left, top1, right_w, Inches(4.75), bg_color=CARD_BG, border_color=CARD_BORDER)
    if os.path.exists(FORZA_IMG):
        slide.shapes.add_picture(FORZA_IMG, right_left + Inches(0.2), top1 + Inches(0.3), Inches(3.4), Inches(2.55))
    
    tb = slide.shapes.add_textbox(right_left + Inches(0.2), top1 + Inches(3.0), Inches(3.4), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Key Competitive Edge"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = NAVY_PRIMARY; p.space_after = Pt(4)
    p2 = tf.add_paragraph(); p2.text = "A smart digital rental experience combining keyless IoT access, PromptPay payments, and GPS fleet telematics."; p2.font.size = Pt(9.5); p2.font.color.rgb = TEXT_MUTED

    add_footer(slide)

def build_slide_4_target_market(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "4. Target Market & Personas", "Targeting digitally active urban residents, students, expats, and travelers (Age 18–40).")

    # 4 Stat Highlights
    top_pos = Inches(1.8)
    box_w = Inches(2.7)
    gap = Inches(0.3)
    h_box = Inches(1.1)

    add_stat_box(slide, Inches(0.8), top_pos, box_w, h_box, "18 – 40", "Target Age Group", ROYAL_BLUE)
    add_stat_box(slide, Inches(0.8) + (box_w+gap), top_pos, box_w, h_box, "20 Units", "Initial Pilot Fleet", GOLD_ACCENT)
    add_stat_box(slide, Inches(0.8) + (box_w+gap)*2, top_pos, box_w, h_box, "5 Stations", "Sathorn, Asok, Khaosan, Thonglor, Ari", EMERALD)
    add_stat_box(slide, Inches(0.8) + (box_w+gap)*3, top_pos, box_w, h_box, "฿300 – ฿450", "Target Daily Price", ROYAL_BLUE)

    # 4 Customer Personas (Concise & Scannable)
    seg_top = Inches(3.15)
    seg_w = Inches(2.7)
    seg_h = Inches(3.6)

    personas = [
        ("University Students", ROYAL_BLUE, [
            "Campuses: Chula, ABAC, Bangkok Univ.",
            "Need cheap daily transit to bypass traffic.",
            "Prefer 7 to 30-day Standard rentals (Click/Scoopy).",
            "Highly responsive to student discount codes."
        ]),
        ("Expats & Nomads", GOLD_ACCENT, [
            "Professionals living in Sukhumvit / Sathorn.",
            "Need reliable daily transport to bypass BTS rush.",
            "Prefer 30-day Premium rentals (Forza 350).",
            "Value cashless checkout & transparent terms."
        ]),
        ("Tourists & Visitors", EMERALD, [
            "Vacationers staying near Khaosan & Asok.",
            "Need 1-day to 7-day rentals for city exploration.",
            "Refuse passport withholding.",
            "Value included safety helmets & GPS assistance."
        ]),
        ("Urban Commuters", AMBER_WARM, [
            "Bangkok residents needing temporary wheels.",
            "Vehicle in shop or short-term work assignment.",
            "Value rapid doorstep hotel/condo delivery.",
            "Prefer modern, reliable automatic scooters."
        ])
    ]

    for i, (title, color, bullets) in enumerate(personas):
        x = Inches(0.8) + i * (seg_w + gap)
        add_card_box(slide, x, seg_top, seg_w, seg_h, title, bullets, title_color=color, top_bar_color=color)

    add_footer(slide)

def build_slide_5_ebusiness_model(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "5. E-Business Model & Flow", "A direct-to-consumer (B2C) digital rental model integrated with IoT telematics.")

    # 6-Step Visual Process (Clean Pill Cards)
    flow_top = Inches(1.8)
    step_w = Inches(1.8)
    step_gap = Inches(0.18)
    step_h = Inches(1.9)

    steps = [
        ("1. Discover", "Google SEO, TikTok & IG Reels, travel forums.", ROYAL_BLUE),
        ("2. Book", "Select model, rental dates, pickup hub & add-ons.", GOLD_ACCENT),
        ("3. Pay", "Instant PromptPay QR or Credit/Debit Card.", EMERALD),
        ("4. Verify", "Digital KYC: upload passport & driver license.", ROYAL_BLUE),
        ("5. Unlock", "Digital Key in app; tap to unlock via 4G IoT lock.", GOLD_ACCENT),
        ("6. Return", "4-angle photo check; automated deposit refund.", EMERALD)
    ]

    for i, (st, desc, col) in enumerate(steps):
        x = Inches(0.8) + i * (step_w + step_gap)
        add_card_box(slide, x, flow_top, step_w, step_h, st, [desc], title_color=col, top_bar_color=col)

    # 3 Digital Infrastructure Blocks
    infra_top = Inches(4.0)
    infra_w = Inches(3.64)
    infra_gap = Inches(0.38)
    infra_h = Inches(2.7)

    add_card_box(slide, Inches(0.8), infra_top, infra_w, infra_h,
                 "Customer Mobile App (PWA)",
                 ["Interactive catalog with real-time fleet availability.",
                  "Dynamic quotation engine with tiered duration discounts.",
                  "Digital KYC scanner with automated watermarking.",
                  "Smart Key HUD controller with live trip speedometer."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    add_card_box(slide, Inches(0.8) + infra_w + infra_gap, infra_top, infra_w, infra_h,
                 "IoT Telematics Network",
                 ["4G cellular GPS telematics trackers on all 20 bikes.",
                  "Encrypted MQTT broker for remote immobilizer commands.",
                  "Bangkok perimeter geofencing with anti-theft alarms.",
                  "Automated battery voltage and usage diagnostic alerts."],
                 title_color=GOLD_ACCENT, top_bar_color=GOLD_ACCENT)

    add_card_box(slide, Inches(0.8) + (infra_w + infra_gap)*2, infra_top, infra_w, infra_h,
                 "Admin Operations Hub",
                 ["Live Leaflet GPS map tracking all 20 fleet units.",
                  "Financial analytics tracking ฿168,000 break-even target.",
                  "Automated preventative maintenance alerts every 3,000 km.",
                  "Integrated customer support via LINE Official Account."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_6_products_pricing(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "6. Products & Tiered Pricing", "Balancing customer affordability, vehicle utilization, and healthy contribution margins.")

    # Left: Clean Pricing Table
    table_left = Inches(0.8)
    table_top = Inches(1.8)
    table_w = Inches(6.8)
    table_h = Inches(3.6)

    table_shape = slide.shapes.add_table(7, 5, table_left, table_top, table_w, table_h)
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
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_WHITE if row_idx % 2 == 1 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text; p.font.size = Pt(9.5); p.font.bold = (col_idx == 0 or col_idx == 3)
            p.font.color.rgb = NAVY_PRIMARY if col_idx < 3 else (ROYAL_BLUE if col_idx == 3 else EMERALD)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Right: Embedded Photos & Vehicle Cards
    right_w = Inches(4.7)
    right_left = Inches(7.8)

    # Standard Card
    add_card(slide, right_left, Inches(1.8), right_w, Inches(2.3), bg_color=BG_SLATE, border_color=CARD_BORDER)
    if os.path.exists(CLICK_IMG):
        slide.shapes.add_picture(CLICK_IMG, right_left + Inches(0.15), Inches(1.95), Inches(1.8), Inches(1.35))
    tb_std = slide.shapes.add_textbox(right_left + Inches(2.1), Inches(1.85), Inches(2.45), Inches(2.1))
    tf_std = tb_std.text_frame; tf_std.word_wrap = True
    p = tf_std.paragraphs[0]; p.text = "Standard Fleet (10 Units)"; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = ROYAL_BLUE
    for bullet in ["Honda Click 160 & Scoopy-i", "15–37L underseat storage", "Deposit: ฿1k Thai / ฿2k Passport", "Target: Students & daily commuters"]:
        p = tf_std.add_paragraph(); p.text = f"• {bullet}"; p.font.size = Pt(9); p.font.color.rgb = TEXT_BODY

    # Premium Card
    add_card(slide, right_left, Inches(4.25), right_w, Inches(2.45), bg_color=BG_SLATE, border_color=CARD_BORDER)
    if os.path.exists(FORZA_IMG):
        slide.shapes.add_picture(FORZA_IMG, right_left + Inches(0.15), Inches(4.4), Inches(1.8), Inches(1.35))
    tb_prm = slide.shapes.add_textbox(right_left + Inches(2.1), Inches(4.3), Inches(2.45), Inches(2.2))
    tf_prm = tb_prm.text_frame; tf_prm.word_wrap = True
    p = tf_prm.paragraphs[0]; p.text = "Premium Fleet (10 Units)"; p.font.size = Pt(11.5); p.font.bold = True; p.font.color.rgb = GOLD_ACCENT
    for bullet in ["Honda Forza 350 & Vespa Sprint", "Traction control & Dual ABS", "Deposit: ฿3k Thai / ฿5k Passport", "Target: Expats & highway touring"]:
        p = tf_prm.add_paragraph(); p.text = f"• {bullet}"; p.font.size = Pt(9); p.font.color.rgb = TEXT_BODY

    # Pricing Strategy Footer
    add_card_box(slide, Inches(0.8), Inches(5.6), Inches(6.8), Inches(1.1),
                 "Pricing Strategy",
                 ["Tiered duration pricing protects contribution margin while locking in long-term cash flow.",
                  "Add-ons: Zero-Deductible Damage Waiver (+฿80–฿150/d) & Doorstep Delivery (+฿200)."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_7_revenue_model(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "7. Revenue Model", "Diversified revenue streams combining recurring long-term packages with short-term rentals.")

    # Left: Native PowerPoint Doughnut Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Monthly Packages (50%)', 'Daily/Weekly (35%)', 'Damage Waivers (10%)', 'Delivery Fees (5%)']
    chart_data.add_series('Revenue Share', (50, 35, 10, 5))

    chart_x = Inches(0.8)
    chart_y = Inches(1.8)
    chart_w = Inches(5.2)
    chart_h = Inches(4.8)

    add_card(slide, chart_x, chart_y, chart_w, chart_h, bg_color=BG_SLATE, border_color=CARD_BORDER)
    chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, chart_x + Inches(0.2), chart_y + Inches(0.3), chart_w - Inches(0.4), chart_h - Inches(0.6), chart_data)
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.font.size = Pt(9)
    chart.legend.font.color.rgb = TEXT_BODY

    # Right: Revenue Strategy Cards
    right_w = Inches(6.2)
    right_left = Inches(6.3)
    top_pos = Inches(1.8)

    add_card_box(slide, right_left, top_pos, right_w, Inches(1.5),
                 "1. Monthly Recurring Anchor (50%)",
                 ["Secures ~10 bikes on 30-day contracts (฿5,500–฿9,500/mo).",
                  "Guarantees ~฿75,000/month baseline cash flow to cover 45% of fixed overheads."],
                 title_color=GOLD_ACCENT, top_bar_color=GOLD_ACCENT)

    add_card_box(slide, right_left, top_pos + Inches(1.65), right_w, Inches(1.5),
                 "2. High-Margin Short-Term Rentals (35%)",
                 ["Captures tourist and commuter daily/weekly demand at ฿300–฿450/day.",
                  "Delivers peak contribution margin (67%+) during high season and weekends."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    add_card_box(slide, right_left, top_pos + Inches(3.3), right_w, Inches(1.5),
                 "3. Add-ons & Ancillary Services (15%)",
                 ["Zero-Deductible Damage Waivers (+฿80–฿150/d) generate over 75% gross margin.",
                  "Doorstep delivery (฿200 flat) and Bluetooth helmet upgrades."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_8_cost_structure(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "8. Cost Structure", "Lean variable operating costs per rental day and controlled monthly fixed overheads.")

    # Left: Variable Cost breakdown
    left_w = Inches(4.6)
    top_pos = Inches(1.8)
    h_left = Inches(4.9)

    add_card_box(slide, Inches(0.8), top_pos, left_w, h_left,
                 "Variable Costs (Per Rental Day)",
                 ["Maintenance & Lubricants: ฿35 / day\n   Engine oil, CVT belts, standardized servicing.",
                  "Vehicle Sanitization: ฿15 / day\n   Disinfected helmets, washed bodywork.",
                  "Wear & Tear Amortization: ฿25 / day\n   Tires, brake pads, battery lifecycle.",
                  "Insurance Allocation: ฿15 / day\n   Compulsory Por Ror Bor liability pool.",
                  "Payment Gateway & IoT SIM: ฿10 / day\n   PromptPay transaction fee & 4G data packet.",
                  "—— Total Standard Variable Cost: ฿100 / day",
                  "—— Total Premium Variable Cost: ฿150 / day",
                  "Cost Control: Scheduled maintenance every 3,000 km reduces major breakdown expenses by 35%."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    # Right: Fixed Costs Table
    right_w = Inches(6.8)
    right_left = Inches(5.7)

    table_shape = slide.shapes.add_table(11, 2, right_left, top_pos, right_w, Inches(4.9))
    table = table_shape.table
    table.columns[0].width = Inches(4.8)
    table.columns[1].width = Inches(2.0)

    fixed_costs = [
        ("Fixed Cost Category", "Monthly (THB)"),
        ("Motorcycle Fleet Financing (20 bikes amortized)", "฿30,000"),
        ("Staff Salaries (Operations, Mechanic, Customer Support)", "฿80,000"),
        ("Office & Storage Yard Rent (Sathorn Central Depot)", "฿20,000"),
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
        bg = NAVY_PRIMARY if is_header else (BG_WHITE if row_idx % 2 == 1 else CARD_BG)
        c0.fill.solid(); c0.fill.fore_color.rgb = bg
        c1.fill.solid(); c1.fill.fore_color.rgb = bg

        p0 = c0.text_frame.paragraphs[0]; p0.text = cat; p0.font.size = Pt(9.5)
        p0.font.bold = is_header; p0.font.color.rgb = TEXT_WHITE if is_header else TEXT_BODY

        p1 = c1.text_frame.paragraphs[0]; p1.text = amt; p1.font.size = Pt(9.5)
        p1.font.bold = True; p1.font.color.rgb = GOLD_ACCENT if is_header else ROYAL_BLUE
        p1.alignment = PP_ALIGN.RIGHT

    add_footer(slide)

def build_slide_9_monthly_profit(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "9. Monthly Profitability Projection", "Base-case forecast: 80% fleet utilization across 20 bikes (480 active rental days/month).")

    # Top 4 Stat Highlights
    top_pos = Inches(1.8)
    box_w = Inches(2.7)
    gap = Inches(0.3)
    h_box = Inches(1.2)

    add_stat_box(slide, Inches(0.8), top_pos, box_w, h_box, "฿285,000", "Monthly Revenue (80% Util.)", ROYAL_BLUE)
    add_stat_box(slide, Inches(0.8) + (box_w+gap), top_pos, box_w, h_box, "฿60,000", "Total Variable Costs", AMBER_WARM)
    add_stat_box(slide, Inches(0.8) + (box_w+gap)*2, top_pos, box_w, h_box, "฿168,000", "Total Fixed Costs", NAVY_PRIMARY)
    add_stat_box(slide, Inches(0.8) + (box_w+gap)*3, top_pos, box_w, h_box, "+฿57,000", "Net Operating Profit / Mo", EMERALD)

    # Native Clustered Column Chart for Scenarios
    chart_x = Inches(0.8)
    chart_y = Inches(3.25)
    chart_w = Inches(7.5)
    chart_h = Inches(3.5)

    add_card(slide, chart_x, chart_y, chart_w, chart_h, bg_color=BG_SLATE, border_color=CARD_BORDER)

    chart_data = CategoryChartData()
    chart_data.categories = ['60% Low Season', '75% Break-Even', '80% Base Case', '95% Peak Season']
    chart_data.add_series('Revenue (฿k)', (185, 255, 285, 380))
    chart_data.add_series('Total Costs (฿k)', (213, 228, 228, 253))
    chart_data.add_series('Net Profit (฿k)', (-28, 2, 57, 127))

    chart_shape = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, chart_x + Inches(0.2), chart_y + Inches(0.2), chart_w - Inches(0.4), chart_h - Inches(0.4), chart_data)
    chart = chart_shape.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.TOP
    chart.legend.font.size = Pt(8.5)

    # Right: Key Takeaways
    right_w = Inches(3.9)
    right_left = Inches(8.6)

    add_card_box(slide, right_left, chart_y, right_w, chart_h,
                 "Financial Takeaways",
                 ["Break-Even Threshold: Achieved at 75% fleet utilization (15 active bikes).",
                  "Base Case Profitability: 80% utilization produces ฿57,000 monthly profit (20% net margin).",
                  "Peak Upside: High tourist season (95% utilization) yields +฿127,000 net profit/month.",
                  "Annualized Run-Rate: Sustainable base case generates ฿684,000 in annual net operating profit."],
                 title_color=NAVY_PRIMARY, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_10_breakeven(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "10. Break-Even Analysis", "Determining sales volume and fleet utilization required to cover all monthly overheads.")

    # Top 3 Stat Highlights
    top_pos = Inches(1.8)
    w_box = Inches(3.64)
    gap = Inches(0.38)
    h_box = Inches(1.4)

    add_stat_box(slide, Inches(0.8), top_pos, w_box, h_box, "฿252,631", "Break-Even Revenue / Month", ROYAL_BLUE)
    add_stat_box(slide, Inches(0.8) + (w_box+gap), top_pos, w_box, h_box, "75% Utilization", "15 of 20 Active Bikes", GOLD_ACCENT)
    add_stat_box(slide, Inches(0.8) + (w_box+gap)*2, top_pos, w_box, h_box, "66.5%", "Average Contribution Margin", EMERALD)

    # Split Bottom Content
    split_top = Inches(3.45)
    split_w = Inches(5.66)
    split_h = Inches(3.3)

    add_card_box(slide, Inches(0.8), split_top, split_w, split_h,
                 "Break-Even Mathematical Model",
                 ["Formula:\n   BEP (Revenue) = Fixed Costs ÷ Contribution Margin Ratio",
                  "Calculation:\n   BEP = ฿168,000 ÷ 0.665 ≈ ฿252,631 per month",
                  "Daily Rental Equivalent:\n   ฿168,000 ÷ ฿250 (avg daily margin) ≈ 672 bike-days/month.",
                  "Fleet Capacity Insight:\n   20 bikes × 30 days = 600 available days on daily rentals.\n   Therefore, long-term monthly & weekly contracts are vital to reach break-even at 75% utilization."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    add_card_box(slide, Inches(6.84), split_top, split_w, split_h,
                 "Management Operational Rules",
                 ["1. The 15-Bike Rule: Operations must maintain at least 15 active contracts to prevent operating losses.",
                  "2. Anchor Contracts: Keep 10 bikes on 30-day packages (50% fleet) to cover ฿75,000 in fixed costs.",
                  "3. Margin Protection: Reserve 10 bikes for daily/weekly tourists at full rate (67%+ margin).",
                  "4. Safety Cushion: The 80% target provides a ฿57,000 monthly safety buffer above break-even."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_11_marketing(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "11. Digital Marketing Strategy", "Prioritizing high-intent search and visual channels where Bangkok commuters look for mobility.")

    # 5 Funnel Stage Cards
    col_w = Inches(2.2)
    gap = Inches(0.17)
    top_pos = Inches(1.8)
    h = Inches(3.7)

    channels = [
        ("1. Google & SEO", ROYAL_BLUE, [
            "Capture high-intent searches.",
            "'Motorbike rental Bangkok'.",
            "'Rent scooter Sathorn / Asok'.",
            "Top Google Maps local ranking with 5-star customer reviews."
        ]),
        ("2. TikTok & Reels", GOLD_ACCENT, [
            "Visual discovery & lifestyle.",
            "Quick videos: 'How to rent a bike with your phone in Bangkok'.",
            "Bangkok scenic scooter routes.",
            "Local expat influencer promos."
        ]),
        ("3. LINE Official", EMERALD, [
            "Retention & fast support.",
            "Automated extension reminders.",
            "1-tap rental renewals.",
            "Live chat support & roadside SOS hotline."
        ]),
        ("4. Strategic Hubs", AMBER_WARM, [
            "Physical-to-digital partners.",
            "Coworking spaces in Thonglor.",
            "Hostels in Khaosan & Sukhumvit with QR booking displays.",
            "Receptionist referral incentives."
        ]),
        ("5. Referral Credits", ROYAL_BLUE, [
            "Viral organic word-of-mouth.",
            "฿500 rental voucher for friend.",
            "฿500 credit for referrer.",
            "Keeps Customer Acquisition Cost (CAC) under ฿200."
        ])
    ]

    for i, (title, color, bullets) in enumerate(channels):
        x = Inches(0.8) + i * (col_w + gap)
        add_card_box(slide, x, top_pos, col_w, h, title, bullets, title_color=color, top_bar_color=color)

    # Conversion Funnel Strip
    add_card_box(slide, Inches(0.8), Inches(5.75), Inches(11.7), Inches(1.0),
                 "Customer Acquisition Funnel",
                 ["Discover (SEO / TikTok)  ➔  Trust (Verified Reviews & Zero Passport Hold)  ➔  Trial (PromptPay QR)  ➔  Repeat (Monthly Contract)  ➔  Refer (฿500 Credit)"],
                 title_color=NAVY_PRIMARY, bg_color=CARD_BG, top_bar_color=NAVY_PRIMARY)

    add_footer(slide)

def build_slide_12_competitor_analysis(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "12. Competitor Analysis", "Benchmarking BKK Motorbike Rental against key market competitors in Bangkok.")

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
        cell.fill.fore_color.rgb = ROYAL_BLUE if col_idx == 1 else NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.size = Pt(9.5); p.font.bold = True; p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    for row_idx, row_data in enumerate(comp_data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else BG_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text; p.font.size = Pt(9.5); p.font.bold = (col_idx == 1)
            p.font.color.rgb = ROYAL_BLUE if col_idx == 1 else (NAVY_PRIMARY if col_idx == 0 else TEXT_BODY)
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

    # Competitive Edge Banner
    add_card_box(slide, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1),
                 "Competitive Differentiation",
                 ["We win by removing the biggest pain points in the market: instant digital checkout + contactless IoT smart key + zero physical passport holding, while matching competitive market rates."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    add_footer(slide)

def build_slide_13_feasibility(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "13. Feasibility Analysis", "Evaluating the proposal across the 5 standard e-business feasibility dimensions.")

    w_card = Inches(2.2)
    gap = Inches(0.17)
    top_pos = Inches(1.8)
    h_card = Inches(3.7)

    dims = [
        ("Market Feasibility", ROYAL_BLUE, [
            "Growing Urban Demand.",
            "Heavy Bangkok traffic drives consistent scooter reliance.",
            "Expanding digital nomad population and tourist rebound.",
            "Preference for cashless, app-based bookings."
        ]),
        ("Technical Feasibility", GOLD_ACCENT, [
            "Low Implementation Risk.",
            "Lightweight PWA: zero App Store installation friction.",
            "Off-the-shelf 4G cellular IoT smart locks and GPS trackers.",
            "Standardized Thai PromptPay QR payment gateways."
        ]),
        ("Operational Feasibility", EMERALD, [
            "Standardized Fleet SOPs.",
            "Central Sathorn maintenance yard handles storage & repairs.",
            "Strict 4-point return inspection protocols.",
            "15km controlled delivery zone avoids logistics bloat."
        ]),
        ("Financial Feasibility", AMBER_WARM, [
            "Solid Unit Economics.",
            "63%–68% contribution margins absorb variable costs.",
            "Break-even at 75% fleet utilization (15 active bikes).",
            "Base case delivers ฿57,000 monthly net operating profit."
        ]),
        ("Legal & Ethical", ROYAL_BLUE, [
            "Strict Compliance.",
            "Thailand PDPA compliant encrypted KYC document storage.",
            "Mandatory DLT & International Driving Permit (IDP) validation.",
            "Compulsory Por Ror Bor motor insurance included."
        ])
    ]

    for i, (title, color, bullets) in enumerate(dims):
        x = Inches(0.8) + i * (w_card + gap)
        add_card_box(slide, x, top_pos, w_card, h_card, title, bullets, title_color=color, top_bar_color=color)

    # Pilot First Recommendation
    add_card_box(slide, Inches(0.8), Inches(5.75), Inches(11.7), Inches(1.0),
                 "Controlled Pilot Execution",
                 ["Launch initially with 20 motorbikes in core central Bangkok hubs (Sathorn & Sukhumvit). Validate real customer acquisition cost (CAC), maintenance wear, and retention before scaling."],
                 title_color=NAVY_PRIMARY, bg_color=CARD_BG, top_bar_color=NAVY_PRIMARY)

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

    headers = ["Risk Identified", "Potential Impact", "Management Mitigation Strategy"]
    risks_data = [
        ("Motorbike Theft / Cross-Border Loss",
         "Asset loss, police overhead, fleet shrinkage.",
         "4G GPS trackers with real-time Bangkok geofencing. Automatic remote engine immobilization if exiting perimeter."),
        ("Traffic Accidents & Body Damage",
         "Repair expense, dispute friction, vehicle downtime.",
         "Compulsory Por Ror Bor insurance pool; optional Zero-Deductible Damage Waiver (+฿80/d); mandatory pre/post photo inspection."),
        ("Low Off-Peak Tourist Demand",
         "Utilization drops below 75% break-even mark.",
         "Shift fleet focus to 30-day student and expat commuter packages; offer seasonal promotional discounts."),
        ("Unlicensed Tourist Drivers",
         "Customer impoundment, legal liability.",
         "Mandatory digital KYC checking for valid Thai license or International Driving Permit (IDP 1949/1968) before key release."),
        ("IoT Lock / Cellular Failure",
         "Customer unable to unlock or start trip.",
         "Dual-SIM fallback on telematics unit; manual physical master key backup in tamper-evident sealed compartment."),
        ("Deposit Withholding Disputes",
         "Negative reviews on Google Maps.",
         "100% transparent automated photo comparison at check-out vs return. Instant automated PromptPay deposit refund release.")
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text; p.font.size = Pt(10); p.font.bold = True; p.font.color.rgb = TEXT_WHITE
        p.alignment = PP_ALIGN.LEFT

    for row_idx, (r_name, r_imp, r_mit) in enumerate(risks_data, start=1):
        for col_idx, text in enumerate([r_name, r_imp, r_mit]):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if row_idx % 2 == 1 else BG_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text; p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True; p.font.color.rgb = CORAL_RED
            elif col_idx == 1:
                p.font.color.rgb = TEXT_MUTED
            else:
                p.font.color.rgb = TEXT_BODY
            p.alignment = PP_ALIGN.LEFT

    add_footer(slide)

def build_slide_15_conclusion(prs):
    slide = add_blank_slide(prs)
    add_header(slide, "Conclusion & Recommendation", "Executive decision and final business viability assessment.")

    left_w = Inches(6.8)
    top_pos = Inches(1.8)
    h_left = Inches(4.8)

    # Left Recommendation Card
    add_card_box(slide, Inches(0.8), top_pos, left_w, h_left,
                 "Final Recommendation: YES — Launch 20-Bike Pilot",
                 ["1. Genuine Customer Need: Solves real urban friction (traffic gridlock, shop visits, paper contracts, passport withholding).",
                  "2. Accessible Technology: Built with lightweight PWA, PromptPay QR, and standard 4G IoT hardware without proprietary R&D drag.",
                  "3. Healthy Unit Economics: 63%–68% contribution margins deliver ฿57,000 monthly net profit (฿684,000 annualized) at 80% utilization.",
                  "4. Distinct Break-Even Focus: The 75% utilization rule (15 active bikes) gives management clear operational guidance.",
                  "5. Market Trust Advantage: Zero passport withholding + instant keyless IoT unlock creates an unmatched competitive moat."],
                 title_color=EMERALD, top_bar_color=EMERALD)

    # Right: Decision Rule & Visual Closing with Vespa
    right_w = Inches(4.6)
    right_left = Inches(7.9)

    add_card_box(slide, right_left, top_pos, right_w, Inches(1.8),
                 "Executive Decision Rule",
                 ["Launch a 3-month controlled pilot with 20 motorbikes in central Bangkok.",
                  "Scale fleet to 50+ units only when customer retention, unit maintenance costs, and 80%+ utilization are proven."],
                 title_color=ROYAL_BLUE, top_bar_color=ROYAL_BLUE)

    # Closing Visual Card with Vespa Photo
    add_card(slide, right_left, Inches(3.8), right_w, Inches(2.8), bg_color=BG_SLATE, border_color=CARD_BORDER)
    if os.path.exists(VESPA_IMG):
        slide.shapes.add_picture(VESPA_IMG, right_left + Inches(0.2), Inches(3.95), Inches(2.0), Inches(1.5))
    tb_ty = slide.shapes.add_textbox(right_left + Inches(2.3), Inches(3.9), Inches(2.1), Inches(2.5))
    tf_ty = tb_ty.text_frame; tf_ty.word_wrap = True
    p = tf_ty.paragraphs[0]; p.text = "🛵 BKK RENTAL"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ROYAL_BLUE; p.space_after = Pt(4)
    p = tf_ty.add_paragraph(); p.text = "Smart. Seamless. Keyless."; p.font.size = Pt(10); p.font.color.rgb = GOLD_ACCENT; p.space_after = Pt(8)
    p = tf_ty.add_paragraph(); p.text = "Thank You!\nReady for questions & defense."; p.font.size = Pt(10); p.font.color.rgb = TEXT_DARK

    add_footer(slide)

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
def main():
    prs = create_deck()
    print("Building 16-slide BKK Motorbike Rental Presentation (Clean White & Visual)...")

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
