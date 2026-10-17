# Executive Submission Email to Yatharth Sahoo

**To:** yatharth.sahoo@brightchamps.com  
**Subject:** Strategic Plan and Working Prototype: BrightCHAMPS USA Q4 Expansion (5,500 Leads at $29.85 CPL) - Bharanee B  
**Attachments:**  
1. BrightCHAMPS_USA_Q4_Strategy_Deck.pdf (11-Slide Executive Presentation Deck)  
2. BrightCHAMPS_USA_Q4_Strategy_Memo.pdf (Comprehensive Strategy Memo and Technical Runbook)  
3. Bharanee_BrightCHAMPS_USA_Q4_Expansion.zip (Complete Codebase and Working Prototypes)

---

Hi Yatharth,

Thank you for our conversation on Friday and for setting up this live strategic challenge for the USA marketing region. 

Following your mandate to deliver 2,500 leads in November and 3,000 leads in December at the $30 CPL target ("at the right cost") while safeguarding lead quality across diverse US demographics and diaspora communities, I have structured and built a complete Dual-Pillar Strategy and Technical Architecture (Marketing + Product Tech).

Rather than submitting only static decks, I have also deployed a live interactive web application and simulation hub that you can test directly in your browser:
* Live Dynamic Intake Landing Page: https://brightchamps-r2.onrender.com/ (tests the 2-step assessment, mock SMS OTP verification, and calendar slot booking)
* Founder's Strategy Hub and Live Model Simulator: https://brightchamps-r2.onrender.com/hub.html (adjust financial model assumptions in real time and inspect our server-side Meta CAPI pipeline)
* GitHub Codebase: https://github.com/Totto1403/brightchamps-r2

I have attached both the 11-Slide Executive Strategy Deck and the Comprehensive Strategy Memo to this email. Below is an executive summary of the unit economics, marketing segmentation, and product-tech engine.

---

### 1. Reconciled Unit Economics (Single Source of Truth)
All operational figures reconcile to a single simulation model:
* Total Volume Target: 5,500 qualified leads (2,500 in November | 3,000 in December)
* Blended Cost Per Lead: $29.85 USD (Total Spend: $164,175.00, staying under the $165,000 budget ceiling with an $825 buffer)
* Demos Scheduled: 3,723 demos (67.7% booking rate via dynamic 2-step intake)
* Demos Attended: 2,643 demos (71.0% show rate via instant <=48h calendar lock and automated multi-channel reminders)
* Paid Enrollments: 473 students (17.9% demo close rate | 8.60% full-funnel lead-to-paid conversion)
* Net Booked Revenue: $367,550.00 USD (Exact sum of tiers: Tier 1 $169,150 + Tier 2 $152,250 + Tier 3 $46,150, after promo voucher dilution)
* Revenue Less Media Spend: $203,375.00 USD (Direct gross margin after media expenditure)
* Contribution Margin (at 55% Gross Margin): $37,977.50 USD (Net operating contribution after all media spend and 1-on-1 mentor delivery COGS)
* First-Order Media ROAS: 2.24x (Substantially exceeds our 1.82x break-even ROAS)
* Blended CAC: $347.09 USD per enrolled student (2.24x LTV/CAC ratio on $777 net blended ARPU)
* Upfront Cash Collected (Month 1): $275,662.50 USD (75% upfront liquidity to recycle into media)

---

### 2. Pillar 1: Compliant Meta Geo-Matrix and Diaspora Wedge
To prevent ad spend from draining into low-intent rural areas or bidding against ourselves, we segment the US into a Mutually Exclusive 3-Tier Matrix:

1. Tier 1: Tech and Diaspora Metros (30% Volume | 1,650 Leads | $36.00 CPL | $850 Net ARPU):
   * Targeting Mechanism: High-density zip-code clustering in premier school districts (Fremont 94539, Sunnyvale 94087, Frisco 75034, Edison 08820, Bellevue 98052) paired with academic interest proxies (Kumon, Russian School of Math, Mathnasium, Singapore Math, USACO) and 1% customer lookalikes.
   * Positioning: Moving students from passive Roblox and gaming to real Python, GenAI/LLM logic, and competitive STEM for college resumes.
   * Hook: "Beyond Kumon: Why Top Tech Parents in Sunnyvale and Frisco are Moving Kids from Passive Roblox to Real Python and AI."
   * Economics: 72% booking, 76% show rate, 22% demo close yielding $169,150 revenue on $59,400 spend (2.85x ROAS).
2. Tier 2: Affluent Suburban Corridors (45% Volume | 2,475 Leads | $29.00 CPL | $750 Net ARPU):
   * Geographies: Greater Atlanta (Alpharetta/Johns Creek), RTP NC (Cary/Morrisville), Chicago Suburbs (Naperville), Northern VA (Fairfax/Ashburn), Orange County CA (Irvine), Houston Suburbs (Sugar Land).
   * Positioning: Premier 1-on-1 STEM edge from home, eliminating 45-minute driving commutes to physical franchises.
   * Hook: "Kumon built their math foundation. BrightCHAMPS builds their AI and logic future (1-on-1 Classes from Home)."
   * Economics: 68% booking, 71% show rate, 17% demo close yielding $152,250 revenue on $71,775 spend (2.12x ROAS).
3. Tier 3: Inland and Heartland America (25% Volume | 1,375 Leads | $24.00 CPL | $650 Net ARPU):
   * Geographies: Midwest, Central US, and non-metro Sunbelt.
   * Positioning: Accessible Silicon Valley mentors for communities without local elite STEM academies.
   * Economics: 62% booking, 64% show rate, 13% demo close yielding $46,150 revenue on $33,000 spend (1.40x ROAS).

Blended CPL Formula: (0.30 x $36.00) + (0.45 x $29.00) + (0.25 x $24.00) = $29.85 USD

---

### 3. Pillar 2: Product Tech (Data Engine and Dynamic Intake UI)
To systematically guarantee lead quality and demo show rates, I built working software modules:

* Server-Side Meta Conversions API (CAPI v19.0):
  * Strictly Monotonic Expected Values: Event values represent downstream expected revenue P(Paid | Stage) x ARPU so values strictly ascend down the funnel: Lead ($66.83) < Schedule ($98.72) < DemoAttended ($139.07) < Purchase ($777.06).
  * Primary Optimization on Schedule: With ~3,723 events (~108/week/ad-set), Schedule comfortably exits Meta's 50 conversions/week learning phase, while Purchase (~470 events) and DemoAttended are transmitted as offline Value Signals for Target ROAS / Value-Based Bidding (VBB).
  * COPPA and Privacy Compliance: Zero minor data (child name/age) is sent to Meta; only SHA-256 hashed parent contact records are shared.
* Lead Quality Scoring and Contact Validation:
  * Real-time E.164 phone and RFC email validation filtering disposable domains.
  * Replaced form device penalties with a self-reported laptop readiness check ("Does your child have access to a laptop or desktop computer for the trial class?"), accommodating parents who browse on mobile.
* Dynamic Landing Page and Instant Calendar Lock:
  * UTM Auto-Mapping: Automatically detects ad sets and renders matching geo persona variants.
  * Mock Twilio SMS OTP: Integrates 6-digit phone verification (sandbox code: 123456) structured for drop-in Twilio Verify deployment.
  * TCPA Compliance: Mandatory explicit consent checkbox for reminder calls, SMS, and WhatsApp alerts.
  * Attendance Assurance: Locks demo slots within <=48 hours (1-click Google Calendar and Apple .ics sync), with an automated reminder cadence (T-24h Email, T-2h SMS, T-15m WhatsApp) and a self-serve reschedule link to eliminate ghosting.

---

### 4. Operational Readiness and Capacity
* Timezone Capacity: Handling 3,723 demos over 60 days requires ~62 live sessions daily (Eastern 40% [25/day] | Central 30% [19/day] | Pacific 30% [18/day]). A dedicated pod of 16 US-shift trial mentors operating during local after-school hours (4:30 PM - 8:30 PM) provides full coverage with a 15% buffer.
* First-10-Days Test Plan: Days 1-3 CAPI signal smoke test in Dallas and Bay Area ($2,500/day); Days 4-7 creative hook A/B tests; Days 8-10 throughput audit with explicit kill/pivot criteria ($42 Tier 1 CPL cap, 55% booking rate floor).

I would welcome the opportunity to walk you through the presentation deck, the live simulation hub, or the CAPI pipeline at your earliest convenience.

Best regards,

Bharanee B  
AI Associate Candidate, Founder's Office  
Phone: +91 97890 27440 | Chennai / Bengaluru (Ready to relocate immediately)  
GitHub: https://github.com/Totto1403/brightchamps-r2
