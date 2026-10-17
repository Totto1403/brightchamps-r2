"""
Generates an Executive Presentation Deck for Yatharth Sahoo (Founder's Office)
BrightCHAMPS USA Q4 Growth & Expansion Strategy (Nov - Dec 2026)
Produces BrightCHAMPS_USA_Q4_Strategy_Deck.pptx and BrightCHAMPS_USA_Q4_Strategy_Deck.pdf

Fully incorporates all Phase 4 review requirements:
1. Single source of truth financials reconciled to unit_economics_financial_model.py
2. Executive 1-page canvas with top 2 risks and the ask
3. Compliant Meta proxy targeting (zip codes, academic proxies, lookalikes)
4. Tier conversion rates & CPLs explicitly labeled as hypotheses
5. Side-by-side scenarios (Base, Downside, Upside) & 1.82x break-even ROAS
6. Demo capacity by US timezone (EST/CST/PST) & 16-mentor requirement
7. Legal compliance (TCPA, COPPA, Meta minor policies)
8. Assumptions register, first-10-days test plan with kill criteria, pre-launch checklist, leadership asks
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PPTX_PATH = os.path.join(OUTPUT_DIR, "BrightCHAMPS_USA_Q4_Strategy_Deck.pptx")
PDF_PATH = os.path.join(OUTPUT_DIR, "BrightCHAMPS_USA_Q4_Strategy_Deck.pdf")

# Professional Color Palette
COLOR_NAVY = RGBColor(30, 27, 75)        # #1E1B4B
COLOR_INDIGO = RGBColor(67, 56, 202)     # #4338CA
COLOR_SLATE = RGBColor(15, 23, 42)       # #0F172A
COLOR_MUTED = RGBColor(100, 116, 139)    # #64748B
COLOR_AMBER = RGBColor(245, 158, 11)     # #F59E0B
COLOR_GREEN = RGBColor(22, 101, 52)      # #166534
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_CARD_BG = RGBColor(248, 250, 252)  # #F8FAFC
COLOR_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
COLOR_LIGHT_INDIGO = RGBColor(238, 242, 255) # #EEF2FF
COLOR_LIGHT_RED = RGBColor(254, 242, 242)

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="BRIGHTCHAMPS USA • FOUNDER'S OFFICE STRATEGY DECK"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_INDIGO

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY

    def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    def append_run(paragraph, text, bold=False, italic=False, size_pt=10, color=COLOR_SLATE):
        run = paragraph.add_run()
        run.text = text
        run.font.bold = bold
        run.font.italic = italic
        run.font.size = Pt(size_pt)
        run.font.color.rgb = color
        return run

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Navy)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BRIGHTCHAMPS USA • Q4 2026 EXPANSION MANDATE"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_AMBER
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "Scaling Inbound Volume to 5,500 Leads\nat $29.85 CPL via Geo-Marketing & Product-Tech"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(18)

    p2 = tf1.add_paragraph()
    p2.text = "A Dual-Pillar Framework Combining Mutually Exclusive Geo-Targeting with Monotonic Meta CAPI & Instant Calendar Booking"
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = RGBColor(199, 210, 254)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Stakeholder: Yatharth Sahoo (Senior Lead, Founder's Office) | Author: Bharanee B (AI Associate, Founder's Office)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: Executive Summary & Strategy Canvas (One-Page Memo Up Front)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Strategy Canvas: Single-Source-of-Truth Scorecard", "FOUNDER'S OFFICE EXECUTIVE CANVAS")

    # Left: Scorecard Card
    add_card(s2, Inches(0.8), Inches(1.5), Inches(7.8), Inches(5.4), bg_color=COLOR_WHITE)
    tb_sc = s2.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(7.4), Inches(5.1))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True

    p = tf_sc.paragraphs[0]
    p.text = "RECONCILED CORE SCORECARD (MODEL SINGLE SOURCE OF TRUTH)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(10)

    scorecard_rows = [
        ("Inbound Leads: ", "5,500 Leads (Nov: 2,500 | Dec: 3,000)"),
        ("Blended CPL: ", "$29.85 USD (Under $30.00 ceiling by -$0.15 buffer)"),
        ("Total Media Spend: ", "$164,175.00 USD (Under $165,000.00 ceiling by -$825.00)"),
        ("Demos Scheduled: ", "3,723 Demos (67.7% booking rate via dynamic intake)"),
        ("Demos Attended: ", "2,643 Demos (71.0% show rate via instant calendar lock)"),
        ("Paid Students: ", "473 Students (17.9% demo close | 8.60% full funnel)"),
        ("Net Booked Revenue: ", "$367,550.00 USD (Exact sum of 3 tiers)"),
        ("Revenue Less Spend: ", "$203,375.00 USD (Net margin after digital media)"),
        ("Assumed Gross Margin: ", "55.0% (Assumed: 40% mentor payout + 5% platform infra)"),
        ("Contribution Margin: ", "$37,977.50 USD (Profit after media & instructional delivery)"),
        ("First-Order ROAS: ", "2.24x (Substantially exceeds 1.82x break-even ROAS)"),
        ("Blended CAC: ", "$347.09 USD per enrolled student")
    ]
    for lbl, val in scorecard_rows:
        p = tf_sc.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=9.5, color=COLOR_NAVY)
        append_run(p, val, bold=False, size_pt=9.5, color=COLOR_SLATE)
        p.space_after = Pt(4)

    # Right Top Card: Top 2 Risks
    add_card(s2, Inches(8.8), Inches(1.5), Inches(3.7), Inches(2.5), bg_color=COLOR_WHITE)
    tb_rk = s2.shapes.add_textbox(Inches(8.95), Inches(1.65), Inches(3.4), Inches(2.2))
    tf_rk = tb_rk.text_frame
    tf_rk.word_wrap = True

    p = tf_rk.paragraphs[0]
    p.text = "TOP 2 STRATEGIC RISKS & MITIGATIONS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMBER
    p.space_after = Pt(6)

    p1 = tf_rk.add_paragraph()
    append_run(p1, "1. Q4 Ad Auction Inflation: ", bold=True, size_pt=8.5, color=COLOR_NAVY)
    append_run(p1, "Retail CPMs surge 25%+ during BFCM. Mitigate via front-loaded Nov 1-18 pacing, strict $42 bid caps, and gift positioning.", size_pt=8.5, color=COLOR_SLATE)
    p1.space_after = Pt(4)

    p2 = tf_rk.add_paragraph()
    append_run(p2, "2. Demo Timezone Bottlenecks: ", bold=True, size_pt=8.5, color=COLOR_NAVY)
    append_run(p2, "62 demos/day clustered in 4:30-8:30 PM local slots. Mitigate with dedicated 16-mentor US pod across EST/CST/PST.", size_pt=8.5, color=COLOR_SLATE)

    # Right Bottom Card: The Immediate Ask
    add_card(s2, Inches(8.8), Inches(4.2), Inches(3.7), Inches(2.7), bg_color=COLOR_LIGHT_INDIGO, border_color=COLOR_INDIGO)
    tb_ask = s2.shapes.add_textbox(Inches(8.95), Inches(4.35), Inches(3.4), Inches(2.4))
    tf_ask = tb_ask.text_frame
    tf_ask.word_wrap = True

    p = tf_ask.paragraphs[0]
    p.text = "THE IMMEDIATE ASK FOR LEADERSHIP"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)

    asks = [
        "1. Budget Approval: Authorize $164,175 media pacing ($74.6k Nov / $89.5k Dec).",
        "2. Counselor Pod: Roster 16 dedicated US-shift mentors for peak 4:30-8:30 PM slots.",
        "3. Holiday Voucher: Authorize $150 Black Friday/Holiday scholarship grant."
    ]
    for a in asks:
        p = tf_ask.add_paragraph()
        append_run(p, a, bold=True, size_pt=8.5, color=COLOR_NAVY)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 3: The Volume vs Quality vs Cost Trilemma
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1. The Core Challenge: The Volume vs. Quality vs. Cost Trilemma")

    trilemma_cards = [
        ("TRAP 1: THE CHEAP LEAD TRAP", "$15 - $20 CPL",
         "Meta lead forms optimized on volume attract low-intent clickers, grandparents with wrong numbers, or kids without laptops.\n\nResult: Demo show rate collapses to <30%, burning sales counselor payroll and producing zero enrolled revenue.",
         COLOR_LIGHT_RED, COLOR_MUTED),
        ("TRAP 2: THE BOUTIQUE TRAP", "$45 - $60 CPL",
         "Hyper-narrow targeting on Silicon Valley engineers exhausts audience frequency rapidly and inflates auction CPMs.\n\nResult: High trial conversion (25%+), but volume caps at <800 leads and blows past the $30 CPL mandate ceiling.",
         COLOR_LIGHT_RED, COLOR_MUTED),
        ("THE FOUNDER'S OFFICE SOLUTION", "$29.85 BLENDED CPL",
         "A Dual-Pillar Architecture:\n• Mutually Exclusive 3-Tier Geo Matrix balancing $36 tech hubs with $24 heartland volume.\n• Server-Side Meta CAPI with monotonic expected values + instant calendar booking (<=48h lag).",
         COLOR_LIGHT_INDIGO, COLOR_INDIGO)
    ]
    for i, (title, stat, body, bg_c, bdr_c) in enumerate(trilemma_cards):
        left = Inches(0.8 + i * 4.0)
        add_card(s3, left, Inches(1.6), Inches(3.7), Inches(5.2), bg_color=bg_c, border_color=bdr_c)
        tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = stat
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_INDIGO if i == 2 else COLOR_NAVY
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_SLATE

    # =========================================================================
    # SLIDE 4: Pillar 1: Compliant Meta Proxy Targeting & Mutually Exclusive Geos
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "2. Pillar 1: Compliant Meta Targeting & Mutually Exclusive Geos")

    # Card Left: Compliant Mechanism
    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), bg_color=COLOR_WHITE)
    tb_m = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(5.1))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "HOW DIASPORA & STEM TARGETING IS ACHIEVED ON META"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    p_note = tf_m.add_paragraph()
    p_note.text = "Important: Ethnic affinity targeting is prohibited and unavailable on Meta. We achieve precision targeting via 3 compliant operational proxies:"
    p_note.font.size = Pt(9)
    p_note.font.italic = True
    p_note.font.color.rgb = COLOR_MUTED
    p_note.space_after = Pt(10)

    proxies = [
        ("1. High-Density Zip-Code Geo Clusters: ", "Targeting premier STEM school districts with high concentrations of engineering families (Fremont 94539, Sunnyvale 94087, Frisco 75034, Edison 08820, Bellevue 98052)."),
        ("2. Academic & Cultural Interest Proxies: ", "Parents (30-55) indexing heavily on Kumon, Russian School of Math (RSM), Mathnasium, Singapore Math, USACO, First Robotics, and Chess.com."),
        ("3. 1% Lookalikes from US Customer Lists: ", "Ingesting historical US paid customer seed lists (SHA-256 hashed parent emails/phones) to train Meta lookalikes.")
    ]
    for pref, desc in proxies:
        p = tf_m.add_paragraph()
        append_run(p, pref, bold=True, size_pt=9.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=9.5, color=COLOR_SLATE)
        p.space_after = Pt(8)

    # Card Right: Mutually Exclusive Geos
    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), bg_color=COLOR_WHITE)
    tb_g = s4.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.1))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True

    p = tf_g.paragraphs[0]
    p.text = "MUTUALLY EXCLUSIVE 3-TIER GEOGRAPHIC MATRIX"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    tiers = [
        ("Tier 1: Core Tech & Primary Metros (30% Vol | $36 CPL)",
         "• SF Bay Area: Fremont, Sunnyvale, Cupertino, Dublin, San Jose\n"
         "• Seattle Belt: Bellevue, Redmond, Kirkland\n"
         "• DFW Tech Wedge: Frisco, Plano, Irving/Coppell\n"
         "• NJ/NYC Metro: Edison, Iselin, Jersey City\n"
         "• Austin Hub: Austin, Round Rock"),
        ("Tier 2: Affluent Suburban Corridors (45% Vol | $29 CPL)",
         "• North Atlanta: Alpharetta, Johns Creek, Milton\n"
         "• RTP NC: Cary, Morrisville, Apex\n"
         "• Chicago Suburbs: Naperville, Aurora, Schaumburg\n"
         "• Northern VA: Fairfax, Ashburn, McLean\n"
         "• Orange County CA: Irvine, San Diego North\n"
         "• Houston Suburbs: Sugar Land, Katy | Boston: Lexington, Newton"),
        ("Tier 3: Inland & Heartland America (25% Vol | $24 CPL)",
         "• Non-metro Sunbelt, Ohio, Indiana, Michigan, Missouri, Kansas, Iowa, Wisconsin, Inland Pennsylvania.")
    ]
    for t_title, t_body in tiers:
        p = tf_g.add_paragraph()
        append_run(p, t_title, bold=True, size_pt=9.5, color=COLOR_NAVY)
        p.space_after = Pt(2)
        p2 = tf_g.add_paragraph()
        append_run(p2, t_body, size_pt=8.5, color=COLOR_SLATE)
        p2.space_after = Pt(6)

    # =========================================================================
    # SLIDE 5: Funnel Hypotheses & Tier Economics
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "3. Funnel Hypotheses to Validate: Operational Tier Economics")

    # Disclaimer banner
    add_card(s5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.6), bg_color=COLOR_LIGHT_INDIGO, border_color=COLOR_INDIGO)
    tb_disc = s5.shapes.add_textbox(Inches(0.9), Inches(1.45), Inches(11.5), Inches(0.5))
    p_d = tb_disc.text_frame.paragraphs[0]
    p_d.text = "EMPIRICAL HYPOTHESES TO VALIDATE: All tier CPLs and conversion rates represent testable operational hypotheses monitored during Days 1-10."
    p_d.font.size = Pt(9)
    p_d.font.bold = True
    p_d.font.color.rgb = COLOR_NAVY

    # Table of Tiers
    table_shape = s5.shapes.add_table(5, 8, Inches(0.8), Inches(2.2), Inches(11.7), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.4)
    for c_i in range(1, 8):
        table.columns[c_i].width = Inches(1.32)

    headers = ["Cohort / Parameter", "Leads", "CPL ($)", "Spend ($)", "Sched Rate", "Show Rate", "Close Rate", "Net Revenue"]
    for c_i, h in enumerate(headers):
        cell = table.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    tier_rows = [
        ("Tier 1: Tech & Diaspora Metros", "1,650", "$36.00", "$59,400.00", "72.0% (1,188)", "76.0% (903)", "22.0% (199)", "$169,150.00"),
        ("Tier 2: Affluent Suburban Corridors", "2,475", "$29.00", "$71,775.00", "68.0% (1,683)", "71.0% (1,195)", "17.0% (203)", "$152,250.00"),
        ("Tier 3: Inland & Heartland America", "1,375", "$24.00", "$33,000.00", "62.0% (852)", "64.0% (545)", "13.0% (71)", "$46,150.00"),
        ("RECONCILED TOTAL / BLENDED", "5,500", "$29.85", "$164,175.00", "67.7% (3,723)", "71.0% (2,643)", "17.9% (473)", "$367,550.00")
    ]
    for r_i, r_vals in enumerate(tier_rows, start=1):
        bg = COLOR_LIGHT_INDIGO if r_i == 4 else (COLOR_WHITE if r_i % 2 == 1 else COLOR_CARD_BG)
        for c_i, val in enumerate(r_vals):
            cell = table.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_NAVY if r_i == 4 else COLOR_SLATE
            if r_i == 4:
                p.font.bold = True

    # Bottom Callout Box
    add_card(s5, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3), bg_color=COLOR_WHITE)
    tb_b = s5.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.1))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "MATHEMATICAL PROOF OF MANDATE RECONCILIATION:"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p2 = tf_b.add_paragraph()
    p2.text = "• Blended CPL = (0.30 x $36.00) + (0.45 x $29.00) + (0.25 x $24.00) = $10.80 + $13.05 + $6.00 = $29.85 USD (Under $30.00 mandate).\n" \
              "• Exact Net Revenue Sum = $169,150 + $152,250 + $46,150 = $367,550.00 USD (Gross list $414,850 - $47,300 promo voucher dilution).\n" \
              "• Revenue Less Media Spend = $367,550 - $164,175 = $203,375.00 USD | Blended CAC = $347.09 per paid student."
    p2.font.size = Pt(9)
    p2.font.color.rgb = COLOR_SLATE

    # =========================================================================
    # SLIDE 6: Scenarios, Sensitivity & Break-Even Analysis
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "4. Scenario Planning, Sensitivity & Break-Even ROAS Proof")

    # Scenarios Table on Left
    table_shape6 = s6.shapes.add_table(9, 4, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.2))
    table6 = table_shape6.table
    table6.columns[0].width = Inches(2.7)
    table6.columns[1].width = Inches(1.6)
    table6.columns[2].width = Inches(1.6)
    table6.columns[3].width = Inches(1.6)

    h6 = ["Metric / Parameter", "Downside (Stress)", "Base Case (Target)", "Upside (Outperform)"]
    for c_i, h in enumerate(h6):
        cell = table6.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    s_rows = [
        ("Blended CPL ($)", "$34.33 (+15%)", "$29.85", "$26.87 (-10%)"),
        ("Media Spend ($)", "$188,801.25", "$164,175.00", "$147,757.50"),
        ("Show Rate (%)", "55.0% (Ghosting)", "71.0%", "76.0%"),
        ("Enrolled Students", "262", "473", "585"),
        ("Blended CAC ($)", "$720.62", "$347.09", "$252.58"),
        ("Net Revenue ($)", "$193,880.00", "$367,550.00", "$447,525.00"),
        ("First-Order ROAS", "1.03x", "2.24x", "3.03x"),
        ("Contrib Margin ($)", "-$82,167.25", "+$37,977.50", "+$98,381.25")
    ]
    for r_i, r_vals in enumerate(s_rows, start=1):
        bg = COLOR_LIGHT_RED if (r_i == 8 and "-" in r_vals[1]) else (COLOR_WHITE if r_i % 2 == 1 else COLOR_CARD_BG)
        for c_i, val in enumerate(r_vals):
            cell = table6.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.font.color.rgb = COLOR_NAVY if c_i == 2 else COLOR_SLATE
            if c_i == 2:
                p.font.bold = True

    # Right Card: Break-Even Proof & Sensitivity
    add_card(s6, Inches(8.6), Inches(1.5), Inches(3.9), Inches(5.2), bg_color=COLOR_WHITE)
    tb_be = s6.shapes.add_textbox(Inches(8.8), Inches(1.65), Inches(3.5), Inches(4.9))
    tf_be = tb_be.text_frame
    tf_be.word_wrap = True

    p = tf_be.paragraphs[0]
    p.text = "BREAK-EVEN ROAS AT 55% GROSS MARGIN"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)

    p1 = tf_be.add_paragraph()
    p1.text = "Assumed Gross Margin: 55.0%\n(40% mentor payout + 5% platform SaaS)\n\nBreak-Even Formula:\nROAS = 1 / Gross Margin = 1 / 0.55 = 1.82x\n\nBase Case Delivers 2.24x ROAS, securing $37,977.50 in net contribution profit from Day 1."
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = COLOR_SLATE
    p1.space_after = Pt(10)

    p_sen = tf_be.add_paragraph()
    p_sen.text = "VOLUME ALLOCATION SENSITIVITY"
    p_sen.font.size = Pt(10)
    p_sen.font.bold = True
    p_sen.font.color.rgb = COLOR_INDIGO
    p_sen.space_after = Pt(4)

    sen_items = [
        ("Tech Heavy (40/40/20): ", "CPL $30.80 | Paid: 503 | Net Rev: $398k | ROAS 2.35x"),
        ("Balanced Base (30/45/25): ", "CPL $29.85 | Paid: 473 | Net Rev: $368k | ROAS 2.24x"),
        ("Heartland Heavy (20/45/35): ", "CPL $28.65 | Paid: 434 | Net Rev: $329k | ROAS 2.09x")
    ]
    for lbl, desc in sen_items:
        p = tf_be.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8, color=COLOR_SLATE)
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 7: Pillar 2: Data Engine & Meta CAPI Pipeline
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "5. Pillar 2: Meta CAPI & Monotonic Expected Values P(Paid)*ARPU")

    # Left Card: Monotonic Table
    add_card(s7, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.4), bg_color=COLOR_WHITE)
    tb_c7 = s7.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(6.4), Inches(5.1))
    tf_c7 = tb_c7.text_frame
    tf_c7.word_wrap = True

    p = tf_c7.paragraphs[0]
    p.text = "STRICTLY MONOTONIC CONVERSION VALUE CALIBRATION"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    p_exp = tf_c7.add_paragraph()
    p_exp.text = "Values represent mathematically expected downstream revenue P(Paid | Stage) x ARPU. Values strictly ascend down the funnel: Lead < Schedule < DemoAttended < Purchase."
    p_exp.font.size = Pt(8.5)
    p_exp.font.color.rgb = COLOR_MUTED
    p_exp.space_after = Pt(10)

    # Mini Table for Monotonic Values
    t_v = s7.shapes.add_table(5, 5, Inches(1.0), Inches(2.7), Inches(6.4), Inches(2.2)).table
    t_v.columns[0].width = Inches(2.0)
    for i in range(1, 5):
        t_v.columns[i].width = Inches(1.1)
    
    vh = ["Geo Cohort", "Lead", "Schedule", "DemoJoined", "Purchase"]
    for i, h in enumerate(vh):
        c = t_v.cell(0, i)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_NAVY
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    vr = [
        ("Tier 1: Tech/Diaspora", "$102.33", "$142.12", "$187.00", "$850.00"),
        ("Tier 2: Suburban", "$61.56", "$90.53", "$127.50", "$750.00"),
        ("Tier 3: Heartland", "$33.53", "$54.08", "$84.50", "$650.00"),
        ("Blended Average", "$66.83", "$98.72", "$139.07", "$777.06")
    ]
    for r_i, vals in enumerate(vr, start=1):
        for c_i, v in enumerate(vals):
            c = t_v.cell(r_i, c_i)
            c.fill.solid()
            c.fill.fore_color.rgb = COLOR_LIGHT_INDIGO if r_i == 4 else (COLOR_WHITE if r_i % 2 == 1 else COLOR_CARD_BG)
            p = c.text_frame.paragraphs[0]
            p.text = v
            p.font.size = Pt(8)
            p.font.color.rgb = COLOR_NAVY if r_i == 4 else COLOR_SLATE
            if r_i == 4:
                p.font.bold = True

    # Right Card: Campaign Optimization Config
    add_card(s7, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.4), bg_color=COLOR_WHITE)
    tb_cfg = s7.shapes.add_textbox(Inches(8.1), Inches(1.65), Inches(4.2), Inches(5.1))
    tf_cfg = tb_cfg.text_frame
    tf_cfg.word_wrap = True

    p = tf_cfg.paragraphs[0]
    p.text = "CAMPAIGN OPTIMIZATION CONFIGURATION"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    cfg_items = [
        ("Primary Target: 'Schedule': ", "Meta delivers optimal machine learning performance with >50 events/week/ad-set. 'Schedule' generates ~3,723 events (~108/week/ad-set), comfortably exiting learning."),
        ("Why Not 'Purchase'? ", "473 purchases over 60 days across 4 ad sets yields only ~3.5 purchases/week/ad-set—too sparse for Meta ML."),
        ("Value Signals: ", "'DemoAttended' and 'Purchase' stream via CAPI as offline conversion value signals to guide Target ROAS / Value-Based Bidding."),
        ("COPPA Privacy Guard: ", "Zero minor data sent to Meta. Only SHA-256 hashed parent contact records (email, phone, state, zip) transmitted.")
    ]
    for lbl, desc in cfg_items:
        p = tf_cfg.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 8: Landing Page & Attendance Assurance
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "6. Dynamic Landing Page, SMS Verification & Reminder Cadence")

    lp_features = [
        ("SELF-REPORTED LAPTOP READINESS", "Eliminates Device Penalty",
         "Replaces mobile form penalty with self-reported field:\n\n'Does your child have access to a laptop or desktop computer for the trial?'\n\nParents fill forms on smartphones while retaining home PC access.",
         COLOR_WHITE),
        ("MOCK TWILIO SMS OTP", "Contact Integrity Gate",
         "Parent phone numbers are verified via 6-digit SMS OTP (sandbox code 123456).\n\nStructure mirrors Twilio Verify API for drop-in live deployment, eliminating fake VOIP entries.",
         COLOR_WHITE),
        ("TCPA CONSENT CHECKBOX", "Legal Telephony Compliance",
         "Explicit opt-in checkbox consenting to reminder calls, SMS, and WhatsApp alerts.\n\nClear disclosure that consent is not required for purchase, with opt-out mechanisms.",
         COLOR_WHITE),
        ("ATTENDANCE ASSURANCE", "Multi-Channel Cadence",
         "Confirmation screen establishes automated reminder schedule:\n• T-24h: Calendar Invite via Email\n• T-2h: 1-Click Zoom Link via SMS\n• T-15m: Room Open Alert via WhatsApp\n• Reschedule button eliminates ghosts.",
         COLOR_LIGHT_INDIGO)
    ]
    for i, (title, sub, body, bg_c) in enumerate(lp_features):
        left = Inches(0.8 + i * 2.95)
        add_card(s8, left, Inches(1.6), Inches(2.8), Inches(5.2), bg_color=bg_c)
        tb = s8.shapes.add_textbox(left + Inches(0.15), Inches(1.8), Inches(2.5), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_NAVY
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = sub
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_INDIGO
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_SLATE

    # =========================================================================
    # SLIDE 9: Operational Capacity by US Timezone
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "7. Operational Capacity: Demo Distribution by US Time Zone")

    # Table on Left
    table_shape9 = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.6), Inches(7.5), Inches(3.2))
    table9 = table_shape9.table
    table9.columns[0].width = Inches(2.1)
    table9.columns[1].width = Inches(1.35)
    table9.columns[2].width = Inches(1.35)
    table9.columns[3].width = Inches(1.35)
    table9.columns[4].width = Inches(1.35)

    h9 = ["Time Zone Region", "Volume Mix %", "Daily Demos", "Peak Local Hours", "FTE Mentors Req"]
    for c_i, h in enumerate(h9):
        cell = table9.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    tz_rows = [
        ("Eastern (EST)", "40%", "25 Demos/Day", "4:30 - 8:30 PM", "7 Mentors"),
        ("Central (CST)", "30%", "19 Demos/Day", "4:30 - 8:30 PM", "5 Mentors"),
        ("Pacific (PST)", "30%", "18 Demos/Day", "4:30 - 8:30 PM", "4 Mentors"),
        ("TOTAL DEDICATED POD", "100%", "62 Demos/Day", "School-day Evenings", "16 Mentors")
    ]
    for r_i, r_vals in enumerate(tz_rows, start=1):
        bg = COLOR_LIGHT_INDIGO if r_i == 4 else (COLOR_WHITE if r_i % 2 == 1 else COLOR_CARD_BG)
        for c_i, val in enumerate(r_vals):
            cell = table9.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_NAVY if r_i == 4 else COLOR_SLATE
            if r_i == 4:
                p.font.bold = True

    # Right Card: Capacity Logistics
    add_card(s9, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.1), bg_color=COLOR_WHITE)
    tb_tz = s9.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.5), Inches(4.7))
    tf_tz = tb_tz.text_frame
    tf_tz.word_wrap = True

    p = tf_tz.paragraphs[0]
    p.text = "SALES COUNSELOR ROSTER & LOGISTICS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    tz_logistics = [
        ("Daily Volume: ", "3,723 demos over 60 days requires conducting ~62 live 45-minute sessions daily."),
        ("Capacity Math: ", "At 4 demos per mentor per shift, 62 demos requires 15.5 educators. A 16-mentor roster provides full coverage with a 15% surge buffer."),
        ("Timezone Shift Routing: ", "Leads are routed dynamically based on parent phone area code and zip code to counselors in their matching timezone pod."),
        ("Weekend Morning Surge: ", "Saturdays and Sundays feature 10:00 AM - 2:00 PM family slots to capture high-converting weekend demand.")
    ]
    for lbl, desc in tz_logistics:
        p = tf_tz.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 10: Legal Compliance & Assumptions Register
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "8. Legal Compliance Architecture & Assumptions Register")

    # Left: Compliance Card
    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), bg_color=COLOR_WHITE)
    tb_comp = s10.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(5.0))
    tf_comp = tb_comp.text_frame
    tf_comp.word_wrap = True

    p = tf_comp.paragraphs[0]
    p.text = "REGULATORY & PRIVACY COMPLIANCE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    comp_items = [
        ("TCPA (Telephone Consumer Protection Act): ", "Mandatory explicit consent checkbox on Step 2. Clear disclosure that purchase is not conditional on consent, with one-click opt-out ('STOP')."),
        ("COPPA (Children's Online Privacy Protection): ", "Strict parent-facing intake gate. Zero child PII (name, age, grade) transmitted to Meta CAPI or ad networks; only SHA-256 hashed parent contact records."),
        ("Meta Minor Advertising Guidelines: ", "Ad targeting configured strictly for Parents Age 30-55. Creative messaging emphasizes parental co-learning and academic enrichment.")
    ]
    for lbl, desc in comp_items:
        p = tf_comp.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(6)

    # Right: Assumptions Register Table
    add_card(s10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), bg_color=COLOR_WHITE)
    tb_ass = s10.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf_ass = tb_ass.text_frame
    tf_ass.word_wrap = True

    p = tf_ass.paragraphs[0]
    p.text = "ASSUMPTIONS REGISTER & VALIDATION TESTS"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(8)

    assumptions = [
        ("Blended CPL $29.85: ", "High confidence | Source: Q3 US Meta benchmark | Validating Test: Day 1-3 pilot at $2.5k/day in Dallas & Bay Area."),
        ("Demo Show Rate 71%: ", "High confidence | Source: Instant calendar lock + reminder cadence | Validating Test: First 100 scheduled slots Nov 1-4."),
        ("Demo Close Rate 17.9%: ", "Medium confidence | Source: Senior US sales counselor pod | Validating Test: First 25 completed sessions."),
        ("Gross Margin 55%: ", "High confidence | Source: Mentor payout ($30-35/hr) + SaaS COGS | Validating Test: Unit cost ledger audit.")
    ]
    for lbl, desc in assumptions:
        p = tf_ass.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 11: First-10-Days Test Plan, Pre-Launch & Decisions Needed
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "9. First-10-Days Test Plan, Pre-Launch Checklist & Leadership Asks")

    # Left: First 10 Days & Kill Criteria
    add_card(s11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.3), bg_color=COLOR_WHITE)
    tb_tp = s11.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.2), Inches(5.0))
    tf_tp = tb_tp.text_frame
    tf_tp.word_wrap = True

    p = tf_tp.paragraphs[0]
    p.text = "FIRST-10-DAYS TEST PLAN & KILL CRITERIA"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)

    t_plan = [
        ("Days 1-3 (Signal Smoke Test): ", "Pilot spend ($2.5k/day) in Bay Area & Dallas. Verify CAPI EMQ > 8.0 and slot sync."),
        ("Days 4-7 (Hook Calibration): ", "A/B test 'Beyond Kumon' vs. 'Academic Logic Edge'. Calibrate ad-set CPMs."),
        ("Days 8-10 (Throughput Audit): ", "First 200+ completed demos. Audit show rate and initial Stripe transactions."),
        ("KILL / PIVOT CRITERIA: ", "\n• Trigger 1: If Tier 1 CPL > $42 after 150 leads -> Shift 10% budget to Tier 2.\n• Trigger 2: If Booking Rate < 55% -> Activate fallback 1-step sticky form.\n• Trigger 3: If Show Rate < 60% -> Mandate manual phone check-in at T-4h.")
    ]
    for lbl, desc in t_plan:
        p = tf_tp.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(4)

    # Right: Checklist & Decisions Needed
    add_card(s11, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), bg_color=COLOR_WHITE)
    tb_ch = s11.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    tf_ch = tb_ch.text_frame
    tf_ch.word_wrap = True

    p = tf_ch.paragraphs[0]
    p.text = "PRE-LAUNCH CHECKLIST & DECISIONS NEEDED"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_INDIGO
    p.space_after = Pt(6)

    chk = [
        ("[x] Meta CAPI Pipeline: ", "Verified with SHA-256 parent hashing & monotonic event values."),
        ("[x] Mutually Exclusive Geos: ", "Uploaded to Meta Business Manager."),
        ("[x] Landing Page Intake: ", "Laptop access question, SMS OTP mock & TCPA consent live."),
        ("[x] Campaign Optimization: ", "Configured on 'Schedule' with 'Purchase' as value signal."),
        ("DECISION 1: Budget Approval: ", "Authorize $164,175 media pacing across Nov-Dec."),
        ("DECISION 2: Counselor Assignment: ", "Confirm roster of 16 dedicated US-shift mentors."),
        ("DECISION 3: Holiday Voucher: ", "Approve $150 tuition scholarship voucher for BFCM.")
    ]
    for lbl, desc in chk:
        p = tf_ch.add_paragraph()
        append_run(p, lbl, bold=True, size_pt=8.5, color=COLOR_INDIGO if "DECISION" in lbl else COLOR_NAVY)
        append_run(p, desc, size_pt=8.5, color=COLOR_SLATE)
        p.space_after = Pt(4)

    prs.save(PPTX_PATH)
    print(f"Presentation successfully saved to: {PPTX_PATH}")

    # Export to PDF via PowerPoint COM
    try:
        import win32com.client as win32
        ppt_app = win32.Dispatch("PowerPoint.Application")
        presentation = ppt_app.Presentations.Open(PPTX_PATH, WithWindow=False)
        presentation.SaveAs(PDF_PATH, 32) # 32 = ppSaveAsPDF
        presentation.Close()
        ppt_app.Quit()
        print(f"Executive Deck PDF successfully created at: {PDF_PATH}")
    except Exception as e:
        print(f"Error converting PPTX to PDF via COM: {e}")

if __name__ == "__main__":
    create_deck()
