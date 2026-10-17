"""
BrightCHAMPS USA Q4 Growth & Expansion Engine
Component: Live Web Application & Founder's Strategic Hub
Author: Bharanee B (AI Associate, Founder's Office)
Stakeholder: Yatharth Sahoo (Senior Lead, Founder's Office)

Description:
Production Flask application hosted on Render.
Serves:
1. Dynamic 2-Step Intake Landing Page ('/')
2. Interactive Founder's Strategy Hub & Model Simulator ('/hub')
3. Real-Time Lead Scoring & Meta CAPI Inspection APIs ('/api/...')
4. Direct PDF & Document Viewers ('/deliverables/...')
"""

import os
import sys
import json
from flask import Flask, send_from_directory, jsonify, request, render_template_string

# Add local modules to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "strategy"))
sys.path.append(os.path.join(BASE_DIR, "product_tech", "data_engine"))

from lead_scoring_engine import LeadScoringEngine
from meta_capi_dispatcher import MetaCAPIDispatcher, STAGE_EXPECTED_VALUES

app = Flask(__name__, static_folder=None)
app.config['JSON_SORT_KEYS'] = False

capi_dispatcher = MetaCAPIDispatcher(optimization_event="Schedule", dry_run=True)

# ==============================================================================
# ROUTE 1: DYNAMIC LANDING PAGE PROTOTYPE
# ==============================================================================
@app.route("/")
@app.route("/landing")
def landing_page():
    """Serves the dynamic 2-step assessment landing page."""
    landing_dir = os.path.join(BASE_DIR, "product_tech", "landing_page")
    return send_from_directory(landing_dir, "index.html")

@app.route("/styles.css")
def landing_css():
    landing_dir = os.path.join(BASE_DIR, "product_tech", "landing_page")
    return send_from_directory(landing_dir, "styles.css", mimetype="text/css")

@app.route("/app.js")
def landing_js():
    landing_dir = os.path.join(BASE_DIR, "product_tech", "landing_page")
    return send_from_directory(landing_dir, "app.js", mimetype="application/javascript")

# ==============================================================================
# ROUTE 2: DELIVERABLES & DOCUMENT DOWNLOADS
# ==============================================================================
@app.route("/deliverables/<path:filename>")
def get_deliverable(filename):
    """Serves PDF, PPTX, DOCX, and ZIP deliverables."""
    deliv_dir = os.path.join(BASE_DIR, "deliverables")
    return send_from_directory(deliv_dir, filename)

# ==============================================================================
# ROUTE 3: API ENDPOINTS
# ==============================================================================
@app.route("/api/score-lead", methods=["POST"])
def api_score_lead():
    """Real-time lead scoring and CAPI payload generation."""
    data = request.get_json(force=True) or {}
    scored = LeadScoringEngine.score_lead(data)
    return jsonify(scored)

@app.route("/api/dispatch-capi", methods=["POST"])
def api_dispatch_capi():
    """Dispatches monotonic CAPI events."""
    data = request.get_json(force=True) or {}
    event_type = data.get("event_type", "Lead")
    lead_input = data.get("lead", {})

    scored = LeadScoringEngine.score_lead(lead_input)
    geo_tier = scored["geo_tier"]

    if event_type == "Lead":
        res = capi_dispatcher.dispatch_lead_event(scored)
    elif event_type == "Schedule":
        res = capi_dispatcher.dispatch_schedule_event(scored["lead_id"], scored["meta_capi_user_data"], geo_tier=geo_tier)
    elif event_type == "DemoAttended":
        res = capi_dispatcher.dispatch_offline_attended_event(scored["lead_id"], scored["meta_capi_user_data"], geo_tier=geo_tier)
    elif event_type == "Purchase":
        rev = 850.0 if geo_tier == "TIER_1_TECH_DIASPORA" else (750.0 if geo_tier == "TIER_2_SUBURBAN" else 650.0)
        res = capi_dispatcher.dispatch_purchase_event(scored["lead_id"], scored["meta_capi_user_data"], package_name="Next-Gen STEM & AI Track", revenue_usd=rev, geo_tier=geo_tier)
    else:
        return jsonify({"error": f"Unknown event type: {event_type}"}), 400

    return jsonify({"scored_lead": scored, "dispatched_capi_event": res})

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Dynamic unit economics and sensitivity simulation."""
    data = request.get_json(force=True) or {}

    leads_total = int(data.get("leads_total", 5500))
    t1_pct = float(data.get("t1_pct", 0.30))
    t2_pct = float(data.get("t2_pct", 0.45))
    t3_pct = float(data.get("t3_pct", 0.25))

    cpl_t1 = float(data.get("cpl_t1", 36.00))
    cpl_t2 = float(data.get("cpl_t2", 29.00))
    cpl_t3 = float(data.get("cpl_t3", 24.00))

    show_rate = float(data.get("show_rate", 0.71))
    close_rate = float(data.get("close_rate", 0.179))
    gross_margin = float(data.get("gross_margin", 0.55))
    voucher_discount = float(data.get("voucher_discount", 100.00))

    # Tiers calculation
    l_t1 = int(leads_total * t1_pct)
    l_t2 = int(leads_total * t2_pct)
    l_t3 = leads_total - l_t1 - l_t2

    spend_t1 = l_t1 * cpl_t1
    spend_t2 = l_t2 * cpl_t2
    spend_t3 = l_t3 * cpl_t3
    total_spend = spend_t1 + spend_t2 + spend_t3
    blended_cpl = total_spend / leads_total

    sched_t1 = int(l_t1 * 0.72)
    sched_t2 = int(l_t2 * 0.68)
    sched_t3 = int(l_t3 * 0.62)
    total_sched = sched_t1 + sched_t2 + sched_t3

    join_t1 = int(sched_t1 * 0.76)
    join_t2 = int(sched_t2 * 0.71)
    join_t3 = int(sched_t3 * 0.64)
    total_joined = int(total_sched * show_rate)

    paid_t1 = int(join_t1 * 0.22)
    paid_t2 = int(join_t2 * 0.17)
    paid_t3 = int(join_t3 * 0.13)
    total_paid = int(total_joined * close_rate)

    arpu_t1 = 950.0 - voucher_discount
    arpu_t2 = 850.0 - voucher_discount
    arpu_t3 = 750.0 - voucher_discount

    rev_t1 = paid_t1 * arpu_t1
    rev_t2 = paid_t2 * arpu_t2
    rev_t3 = paid_t3 * arpu_t3
    net_revenue = rev_t1 + rev_t2 + rev_t3

    rev_less_media = net_revenue - total_spend
    cogs = net_revenue * (1.0 - gross_margin)
    contrib_margin = (net_revenue * gross_margin) - total_spend
    roas = net_revenue / total_spend if total_spend > 0 else 0.0
    be_roas = 1.0 / gross_margin if gross_margin > 0 else 0.0
    cac = total_spend / total_paid if total_paid > 0 else 0.0

    return jsonify({
        "leads_total": leads_total,
        "blended_cpl": round(blended_cpl, 2),
        "total_spend": round(total_spend, 2),
        "total_scheduled": total_sched,
        "total_joined": total_joined,
        "total_paid": total_paid,
        "net_revenue": round(net_revenue, 2),
        "rev_less_media": round(rev_less_media, 2),
        "contrib_margin": round(contrib_margin, 2),
        "first_order_roas": round(roas, 2),
        "breakeven_roas": round(be_roas, 2),
        "blended_cac": round(cac, 2)
    })

# ==============================================================================
# ROUTE 4: FOUNDER'S STRATEGY HUB & EXECUTIVE DASHBOARD ('/hub')
# ==============================================================================
@app.route("/hub")
@app.route("/executive")
def executive_hub():
    """Serves the interactive Founder's Office Strategy & Simulation Hub."""
    hub_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BrightCHAMPS USA | Founder's Office Strategy & Simulation Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #1E1B4B;
            --indigo: #4338CA;
            --primary: #4F46E5;
            --slate: #0F172A;
            --muted: #64748B;
            --card-bg: #FFFFFF;
            --bg-page: #F8FAFC;
            --border: #E2E8F0;
            --green: #15803D;
            --amber: #F59E0B;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background: var(--bg-page);
            color: var(--slate);
            line-height: 1.5;
        }
        header.hub-header {
            background: var(--navy);
            color: #FFFFFF;
            padding: 20px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--amber);
        }
        .header-brand {
            font-size: 1.4rem;
            font-weight: 800;
        }
        .header-brand span { color: #818CF8; }
        .header-badge {
            background: rgba(255, 255, 255, 0.12);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #FBBF24;
        }
        .nav-links a {
            color: #E0E7FF;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 600;
            margin-left: 20px;
            padding: 6px 14px;
            border-radius: 6px;
            transition: all 0.2s;
        }
        .nav-links a:hover, .nav-links a.active {
            background: var(--primary);
            color: #FFFFFF;
        }
        main.hub-container {
            max-width: 1240px;
            margin: 32px auto;
            padding: 0 24px;
        }
        .hub-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .card-title {
            font-size: 1.1rem;
            font-weight: 800;
            color: var(--navy);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card-sub {
            font-size: 0.85rem;
            color: var(--muted);
            margin-bottom: 20px;
        }
        /* Sliders */
        .slider-group {
            margin-bottom: 18px;
        }
        .slider-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            font-weight: 700;
            color: #334155;
            margin-bottom: 6px;
        }
        .slider-label span.val {
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
        }
        input[type="range"] {
            width: 100%;
            height: 6px;
            border-radius: 4px;
            accent-color: var(--primary);
            cursor: pointer;
        }
        /* Scorecard metrics */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-top: 20px;
        }
        .metric-tile {
            background: #F1F5F9;
            border-radius: 8px;
            padding: 14px;
            text-align: center;
        }
        .metric-tile.highlight {
            background: #EEF2FF;
            border: 1px solid #C7D2FE;
        }
        .metric-val {
            font-size: 1.35rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: var(--navy);
        }
        .metric-tile.highlight .metric-val {
            color: var(--indigo);
        }
        .metric-lbl {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--muted);
            margin-top: 4px;
        }
        /* Download links */
        .download-btn {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            border: 1.5px solid var(--border);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            text-decoration: none;
            color: var(--slate);
            font-size: 0.88rem;
            font-weight: 700;
            transition: all 0.2s;
        }
        .download-btn:hover {
            border-color: var(--primary);
            background: #EEF2FF;
            color: var(--primary);
        }
        .download-tag {
            font-size: 0.72rem;
            font-weight: 800;
            background: #E2E8F0;
            padding: 2px 8px;
            border-radius: 4px;
        }
        /* Code Box */
        pre.json-box {
            background: #0F172A;
            color: #38BDF8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            max-height: 280px;
        }
        .btn-action {
            background: var(--primary);
            color: #FFFFFF;
            border: none;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 10px 18px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn-action:hover {
            background: var(--indigo);
        }
    </style>
</head>
<body>

    <header class="hub-header">
        <div class="header-brand">
            Bright<span>CHAMPS</span> USA <span class="header-badge">FOUNDER'S OFFICE STRATEGY HUB</span>
        </div>
        <nav class="nav-links">
            <a href="/" target="_blank">🌐 Test Live Landing Page</a>
            <a href="#simulator" class="active">📊 Model Simulator</a>
            <a href="#capi">⚡ Meta CAPI Console</a>
            <a href="#deliverables">📂 Downloads & Artifacts</a>
        </nav>
    </header>

    <main class="hub-container">

        <!-- Executive Summary Banner -->
        <div class="card" style="margin-bottom: 24px; border-left: 4px solid var(--indigo);">
            <div class="card-title">📌 Executive Mandate & Single Source of Truth Overview</div>
            <p style="font-size: 0.92rem; color: #334155;">
                Mandate for Yatharth Sahoo (Senior Lead, Founder's Office): Scale US inbound volume to <strong>5,500 qualified leads at a $29.85 blended CPL</strong> ($164,175 spend under $165k ceiling), generating <strong>$367,550.00 Net Booked Revenue</strong> and <strong>$37,977.50 Contribution Margin</strong> at a <strong>2.24x ROAS</strong> (exceeding 1.82x break-even).
            </p>
        </div>

        <div class="hub-grid">
            <!-- Left: Live Financial Model Simulator -->
            <div class="card" id="simulator">
                <div class="card-title">🎛️ Live Unit Economics & Sensitivity Simulator</div>
                <div class="card-sub">Drag sliders to test macro stress conditions, CPM shifts, or show-rate variance:</div>

                <div class="slider-group">
                    <div class="slider-label">
                        <span>Total Inbound Leads (Nov–Dec)</span>
                        <span class="val" id="val-leads">5,500 Leads</span>
                    </div>
                    <input type="range" id="input-leads" min="3000" max="8000" step="250" value="5500">
                </div>

                <div class="slider-group">
                    <div class="slider-label">
                        <span>Tier 1 CPL (Tech & Diaspora Metros)</span>
                        <span class="val" id="val-cpl-t1">$36.00</span>
                    </div>
                    <input type="range" id="input-cpl-t1" min="25" max="50" step="1" value="36">
                </div>

                <div class="slider-group">
                    <div class="slider-label">
                        <span>Demo Show Rate (Attendance)</span>
                        <span class="val" id="val-show">71.0%</span>
                    </div>
                    <input type="range" id="input-show" min="45" max="85" step="1" value="71">
                </div>

                <div class="slider-group">
                    <div class="slider-label">
                        <span>Demo-to-Paid Close Rate</span>
                        <span class="val" id="val-close">17.9%</span>
                    </div>
                    <input type="range" id="input-close" min="10" max="25" step="0.5" value="17.9">
                </div>

                <div class="slider-group">
                    <div class="slider-label">
                        <span>Assumed Gross Margin (Delivery COGS)</span>
                        <span class="val" id="val-margin">55.0%</span>
                    </div>
                    <input type="range" id="input-margin" min="40" max="70" step="1" value="55">
                </div>

                <!-- Calculated Output Grid -->
                <div class="metrics-grid">
                    <div class="metric-tile">
                        <div class="metric-val" id="out-cpl">$29.85</div>
                        <div class="metric-lbl">Blended CPL</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-val" id="out-spend">$164,175</div>
                        <div class="metric-lbl">Total Media Spend</div>
                    </div>
                    <div class="metric-tile">
                        <div class="metric-val" id="out-paid">473</div>
                        <div class="metric-lbl">Enrolled Students</div>
                    </div>
                    <div class="metric-tile highlight">
                        <div class="metric-val" id="out-rev">$367,550</div>
                        <div class="metric-lbl">Net Booked Revenue</div>
                    </div>
                    <div class="metric-tile highlight">
                        <div class="metric-val" id="out-contrib">$37,978</div>
                        <div class="metric-lbl">Contribution Margin</div>
                    </div>
                    <div class="metric-tile highlight">
                        <div class="metric-val" id="out-roas">2.24x</div>
                        <div class="metric-lbl">First-Order ROAS (BE: 1.82x)</div>
                    </div>
                </div>
            </div>

            <!-- Right: Document Downloads & Deliverables -->
            <div class="card" id="deliverables">
                <div class="card-title">📂 Final Deliverables & PDFs</div>
                <div class="card-sub">Publication-grade executive assets ready for download:</div>

                <a href="/deliverables/BrightCHAMPS_USA_Q4_Strategy_Deck.pdf" target="_blank" class="download-btn">
                    <span>📊 Executive Strategy Deck</span>
                    <span class="download-tag">PDF (11 Slides)</span>
                </a>

                <a href="/deliverables/BrightCHAMPS_USA_Q4_Strategy_Memo.pdf" target="_blank" class="download-btn">
                    <span>📄 Comprehensive Strategy Memo</span>
                    <span class="download-tag">PDF (Memo)</span>
                </a>

                <a href="/deliverables/BrightCHAMPS_USA_Q4_Strategy_Deck.pptx" download class="download-btn">
                    <span>📑 Editable Slide Deck</span>
                    <span class="download-tag">PPTX</span>
                </a>

                <a href="/deliverables/BrightCHAMPS_USA_Q4_Strategy_Memo.docx" download class="download-btn">
                    <span>📝 Editable Strategy Memo</span>
                    <span class="download-tag">DOCX</span>
                </a>

                <a href="/deliverables/Bharanee_BrightCHAMPS_USA_Q4_Expansion.zip" download class="download-btn">
                    <span>📦 Full Project Archive</span>
                    <span class="download-tag">ZIP Archive</span>
                </a>

                <div style="margin-top: 16px; padding: 12px; background: #F8FAFC; border-radius: 8px; font-size: 0.78rem; color: #64748B;">
                    <strong>Author:</strong> Bharanee B (AI Associate, Founder's Office)<br>
                    <strong>Email:</strong> yatharth.sahoo@brightchamps.com
                </div>
            </div>
        </div>

        <!-- Bottom: Real-Time Meta CAPI Pipeline Inspector -->
        <div class="card" id="capi">
            <div class="card-title">⚡ Real-Time Meta CAPI & Monotonic Expected Value Console</div>
            <div class="card-sub">Test live event valuation P(Paid | Stage) x ARPU and SHA-256 hashed privacy compliance:</div>

            <div style="display: flex; gap: 12px; margin-bottom: 16px;">
                <button class="btn-action" onclick="triggerCapi('Lead')">1. Test Lead Event</button>
                <button class="btn-action" style="background: #10B981;" onclick="triggerCapi('Schedule')">2. Test Schedule Event (Optimization Target)</button>
                <button class="btn-action" style="background: #6366F1;" onclick="triggerCapi('DemoAttended')">3. Test DemoAttended Event (Zoom)</button>
                <button class="btn-action" style="background: #F59E0B;" onclick="triggerCapi('Purchase')">4. Test Purchase Event (Stripe)</button>
            </div>

            <pre class="json-box" id="capi-output">// Click a button above to execute live backend Meta CAPI dispatcher...</pre>
        </div>

    </main>

    <script>
        // Reactive Financial Simulator
        const inLeads = document.getElementById('input-leads');
        const inCplT1 = document.getElementById('input-cpl-t1');
        const inShow = document.getElementById('input-show');
        const inClose = document.getElementById('input-close');
        const inMargin = document.getElementById('input-margin');

        async function updateModel() {
            document.getElementById('val-leads').textContent = Number(inLeads.value).toLocaleString() + ' Leads';
            document.getElementById('val-cpl-t1').textContent = '$' + Number(inCplT1.value).toFixed(2);
            document.getElementById('val-show').textContent = inShow.value + '%';
            document.getElementById('val-close').textContent = inClose.value + '%';
            document.getElementById('val-margin').textContent = inMargin.value + '%';

            const payload = {
                leads_total: parseInt(inLeads.value),
                cpl_t1: parseFloat(inCplT1.value),
                show_rate: parseFloat(inShow.value) / 100.0,
                close_rate: parseFloat(inClose.value) / 100.0,
                gross_margin: parseFloat(inMargin.value) / 100.0
            };

            const res = await fetch('/api/simulate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            document.getElementById('out-cpl').textContent = '$' + data.blended_cpl.toFixed(2);
            document.getElementById('out-spend').textContent = '$' + Math.round(data.total_spend).toLocaleString();
            document.getElementById('out-paid').textContent = data.total_paid;
            document.getElementById('out-rev').textContent = '$' + Math.round(data.net_revenue).toLocaleString();
            document.getElementById('out-contrib').textContent = '$' + Math.round(data.contrib_margin).toLocaleString();
            document.getElementById('out-roas').textContent = data.first_order_roas.toFixed(2) + 'x';
        }

        [inLeads, inCplT1, inShow, inClose, inMargin].forEach(el => el.addEventListener('input', updateModel));

        // CAPI Event Trigger
        async function triggerCapi(eventType) {
            document.getElementById('capi-output').textContent = 'Transmitting event ' + eventType + ' to server pipeline...';
            const payload = {
                event_type: eventType,
                lead: {
                    lead_id: 'US-LIVE-TEST',
                    parent_first_name: 'Satish',
                    parent_last_name: 'Narayanan',
                    phone: '+14085550192',
                    email: 'satish.narayanan@gmail.com',
                    state: 'CA',
                    zip_code: '94087',
                    has_laptop_access: true,
                    child_name: 'Aarav',
                    child_age: 10,
                    coding_experience: 'SOME_EXPERIENCE',
                    subject_interest: 'AI_CODING'
                }
            };
            const res = await fetch('/api/dispatch-capi', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            document.getElementById('capi-output').textContent = JSON.stringify(data, null, 2);
        }

        // Initialize simulation on load
        updateModel();
    </script>
</body>
</html>
"""
    return render_template_string(hub_html)

# ==============================================================================
# ROUTE 5: HEALTH CHECK FOR RENDER
# ==============================================================================
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "BrightCHAMPS USA Q4 Growth & Expansion Engine",
        "author": "Bharanee B (AI Associate, Founder's Office)",
        "stakeholder": "Yatharth Sahoo"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
