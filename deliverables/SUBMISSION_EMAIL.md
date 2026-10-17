# Executive Submission Email to Yatharth Sahoo

**To:** `yatharth.sahoo@brightchamps.com`  
**Subject:** Strategic Plan & Working Prototype: BrightCHAMPS USA Q4 Expansion (5,500 Leads @ $29.85 CPL) — Bharanee B  
**Attachments:**  
1. `BrightCHAMPS_USA_Q4_Strategy_Deck.pdf` (11-Slide Executive Presentation Deck)  
2. `BrightCHAMPS_USA_Q4_Strategy_Memo.pdf` (Comprehensive Strategy Memo & Technical Runbook)  
3. `Bharanee_BrightCHAMPS_USA_Q4_Expansion.zip` (Complete Codebase & Working Prototypes)

---

Hi Yatharth,

Thank you for our conversation on Friday and for setting up this live strategic challenge for the USA marketing region. 

Following your mandate to deliver **2,500 leads in November and 3,000 leads in December at the $30 CPL target ("at the right cost")** while safeguarding lead quality across diverse US demographics and geographies, I have structured and built a complete **Dual-Pillar Strategy & Technical Architecture (Marketing + Product Tech)**.

I have attached both the **11-Slide Executive Strategy Deck** and the **Comprehensive Strategy Memo** to this email. All operational numbers across the deck, memo, and prototypes strictly reconcile to a single source of truth simulation (`unit_economics_financial_model.py`).

Below is an executive summary of the strategy, unit economics, and working software prototypes:

---

### 1. Reconciled Financial Scorecard (Single Source of Truth)
* **Total Inbound Leads**: **5,500 qualified leads** (2,500 in Nov | 3,000 in Dec)
* **Actual Blended CPL**: **$29.85 USD** (Total Media Spend: **$164,175.00**; strictly under the $165,000 budget ceiling by -$825 buffer)
* **Demos Scheduled**: **3,723 demos** (67.7% booking rate via dynamic 2-step intake)
* **Demos Attended (Joined)**: **2,643 demos** (71.0% show rate via instant <=48h calendar lock & multi-channel reminders)
* **Paid Enrollments**: **473 students** (17.9% demo close rate | 8.60% full-funnel lead-to-paid conversion)
* **Net Booked Revenue**: **$367,550.00 USD** (Exact sum of tiers: Tier 1 $169,150 + Tier 2 $152,250 + Tier 3 $46,150; gross list $414,850 minus $47,300 promo voucher dilution)
* **Revenue Less Media Spend**: **$203,375.00 USD** (Net direct revenue after digital advertising spend)
* **Assumed Gross Margin**: **55.0%** (Clearly marked assumption: 40% mentor payout + 5% platform/AWS SaaS = 45% delivery COGS)
* **Contribution Margin**: **$37,977.50 USD** (Net operating contribution profit after all media spend and instructional delivery)
* **First-Order Media ROAS**: **2.24x** (Substantially exceeds our **1.82x break-even ROAS** at the assumed 55% margin)
* **Blended CAC per Student**: **$347.09 USD** (2.24x LTV/CAC first-order ratio on $777 net blended ARPU)
* **Upfront Cash Collected (M1)**: **$275,662.50 USD** (75% upfront cash, providing immediate liquidity; 25% in 30-60 day installments)

---

### 2. Pillar 1: Compliant Meta Targeting & Mutually Exclusive Geos
In the US digital ad ecosystem, running unsegmented national campaigns causes budget to drain into low-intent areas. We balance volume, cost, and purchasing power across a **Mutually Exclusive 3-Tier Geographic Matrix**:

* **Compliant Diaspora & STEM Targeting**: Ethnic affinity targeting is prohibited and unavailable on Meta. We reach high-propensity Indian-American and tech-forward families through 3 compliant proxies:
  1. *High-Density Zip-Code Clusters*: Fremont (94539), Sunnyvale (94087), Frisco (75034), Edison (08820), Bellevue (98052), Alpharetta (30005), Cary (27519), Naperville (60563).
  2. *Academic Affinity Proxies*: Parents (30-55) indexing heavily on Kumon, Russian School of Math (RSM), Mathnasium, Singapore Math, USACO, First Robotics, and Chess.com.
  3. *1% Lookalikes from US Customer Lists*: Seed lists of historical US paid customer records (SHA-256 hashed).

* **The 3 Mutually Exclusive Tiers (Empirical Hypotheses to Validate)**:
  1. **Tier 1: Tech & Diaspora Metros (30% Vol | 1,650 Leads | $36.00 CPL | $850 Net ARPU)**:
     * *Audience*: Tech-forward engineering parents. Reject drag-and-drop toys; want rigorous Python, GenAI/LLM foundations, and algorithmic problem-solving for college resumes.
     * *Hook*: *"Beyond Kumon: Why Top Tech Parents in Sunnyvale & Frisco are Moving Kids from Passive Roblox to Real Python & AI."*
     * *Economics*: 72% booking, 76% show rate, 22% demo close -> **$169,150 revenue on $59,400 spend (2.85x ROAS)**.
  2. **Tier 2: Affluent Suburban Corridors (45% Vol | 2,475 Leads | $29.00 CPL | $750 Net ARPU)**:
     * *Audience*: Physicians, corporate directors, attorneys in top suburban school districts.
     * *Hook*: *"Kumon built their math foundation. BrightCHAMPS builds their AI and logic future (1-on-1 Classes from Home)."*
     * *Economics*: 68% booking, 71% show rate, 17% demo close -> **$152,250 revenue on $71,775 spend (2.12x ROAS)**.
  3. **Tier 3: Inland & Heartland America (25% Vol | 1,375 Leads | $24.00 CPL | $650 Net ARPU)**:
     * *Audience*: Families seeking accessible, high-quality STEM programs without local elite academies.
     * *Hook*: *"Silicon Valley Tech Mentors Right in Your Living Room: Free 1-on-1 Trial Class + Winter Holiday Scholarship Voucher."*
     * *Economics*: 62% booking, 64% show rate, 13% demo close -> **$46,150 revenue on $33,000 spend (1.40x ROAS)**.

$$\text{Blended CPL} = (0.30 \times \$36.00) + (0.45 \times \$29.00) + (0.25 \times \$24.00) = \mathbf{\$29.85 \text{ USD}}$$

---

### 3. Pillar 2: Product Tech (Data Engine & Dynamic Intake UI)
Rather than treating this as a theoretical exercise, I built working software prototypes in the repository:

* **Sub-Pillar A: The Data Engine (`product_tech/data_engine/`)**:
  * **Lead Scoring & Validation (`lead_scoring_engine.py`)**: Real-time regex validation for US +1 E.164 phone numbers and RFC emails, filtering disposable domains. Replaced device penalties with a **self-reported laptop readiness check** (*"Does your child have access to a laptop or desktop computer?"*).
  * **Server-Side Meta Conversions API (CAPI) Dispatcher (`meta_capi_dispatcher.py`)**:
    * *Monotonic Conversion Values*: Calibrated as $P(\text{Paid} \mid \text{Stage}) \times \text{ARPU}$ so values strictly ascend down the funnel (`Lead`: $66.83 < `Schedule`: $98.72 < `DemoAttended`: $139.07 < `Purchase`: $777.06).
    * *Optimization Event*: Configured on **`Schedule`** (~3,723 events or ~108/week/ad-set), comfortably exiting Meta's 50 conversions/week learning phase. `DemoAttended` and `Purchase` stream as offline Value Signals for Target ROAS / Value-Based Bidding.
    * *COPPA & Privacy*: Zero minor data (child name/age) transmitted to Meta; only SHA-256 hashed parent contact records (`em`, `ph`, `st`, `zp`).
* **Sub-Pillar B: Dynamic Landing Page & Instant Calendar Lock (`product_tech/landing_page/`)**:
  * **UTM Auto-Mapping**: Reads `utm_content` / ad-set parameters to auto-render matching geo persona variants (keeping `?geo=` as an override).
  * **Mock Twilio SMS OTP**: Integrates 6-digit phone verification (sandbox code: `123456`) structured for drop-in Twilio Verify deployment.
  * **TCPA Compliance**: Mandatory explicit consent checkbox for informational calls, SMS, and WhatsApp alerts.
  * **Attendance Assurance**: Locks demo slots within $\le 48$ hours (1-Click Google Calendar & Apple `.ics` sync), featuring an automated reminder cadence (T-24h Email, T-2h SMS, T-15m WhatsApp) and a low-friction reschedule action to prevent no-show ghosts.

---

### 4. Operations, Scenarios & Leadership Decisions
* **Counselor Capacity by US Timezone**: 3,723 demos across 60 days = ~62 demos/day (Eastern 40% [25/day] | Central 30% [19/day] | Pacific 30% [18/day]). Handled by a dedicated roster of **16 US-shift trial educators** operating during local school-day evenings (4:30 PM – 8:30 PM).
* **Scenarios & Break-Even**: Tested Base (2.24x ROAS, +$37.9k margin) vs. Stress Downside (55% show, 14% close, +15% CPL -> 1.03x ROAS) vs. Upside (3.03x ROAS, +$98.3k margin). Break-even ROAS is **1.82x** at 55% gross margin.
* **First-10-Days Test Plan**: Days 1-3 CAPI signal smoke test in Dallas & Bay Area ($2,500/day); Days 4-7 creative hook A/B tests; Days 8-10 throughput audit with clear kill criteria ($42 Tier 1 CPL cap, 55% booking rate floor).
* **Decisions Needed from Leadership**:
  1. Authorize $164,175 media pacing across Nov-Dec ($74.6k Nov / $89.5k Dec).
  2. Confirm roster of 16 dedicated US-shift trial mentors for after-school hours.
  3. Approve $150 tuition scholarship voucher for Black Friday / Cyber Week campaigns.

---

### 5. Repository & Artifacts Summary
All deliverables are organized and ready:
* **`deliverables/BrightCHAMPS_USA_Q4_Strategy_Deck.pdf`**: 11-slide executive presentation deck.
* **`deliverables/BrightCHAMPS_USA_Q4_Strategy_Memo.pdf`**: Publication-grade strategy memo & technical runbook.
* **`strategy/unit_economics_financial_model.py`**: Python single-source-of-truth financial simulation.
* **`product_tech/data_engine/`**: Production Python lead scoring and Meta CAPI dispatchers.
* **`product_tech/landing_page/`**: Dynamic landing page prototype with SMS OTP and calendar lock.
* **`deliverables/Bharanee_BrightCHAMPS_USA_Q4_Expansion.zip`**: Complete archived submission package.

I’m very excited about the potential of the US market in Q4, and I would love to walk you through the deck, the CAPI architecture, or the working prototype at your earliest convenience.

Best regards,  
**Bharanee B**  
AI Associate Candidate, Founder's Office  
Phone: +91 97890 27440 | Chennai / Bengaluru (Ready to relocate immediately)
