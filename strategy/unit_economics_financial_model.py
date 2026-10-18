"""
BrightCHAMPS USA Q4 Expansion (Nov - Dec 2026)
Single Source of Truth: Unit Economics, Scenarios, Sensitivity & P&L Model
Author: Bharanee B (AI Associate, Founder's Office)
Stakeholder: Yatharth Sahoo (Senior Lead, Founder's Office)
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

# ==============================================================================
# 1. CORE CAMPAIGN ASSUMPTIONS & INPUTS (SINGLE SOURCE OF TRUTH)
# ==============================================================================

TOTAL_LEADS_TARGET = 5500
NOV_LEADS_TARGET = 2500
DEC_LEADS_TARGET = 3000
TARGET_BLENDED_CPL_CEILING = 30.00
TOTAL_MEDIA_BUDGET_CEILING = TOTAL_LEADS_TARGET * TARGET_BLENDED_CPL_CEILING # $165,000 USD

# Operational & Financial Assumptions (Clearly marked as assumptions)
ASSUMED_GROSS_MARGIN = 0.55       # 55.0% Gross Margin (Assumes 40% mentor payout + 5% video/curriculum infra)
UPFRONT_CASH_COLLECTION_PCT = 0.75 # 75% collected within 30 days of lead, 25% across 30-60 day installments
BREAK_EVEN_ROAS = 1.0 / ASSUMED_GROSS_MARGIN # 1.818x Break-Even ROAS at 55% GM

# Qualification Gate Definition & Pass Rate
# Definition: OTP-verified US mobile + valid parent email + self-reported laptop/desktop access
DEFAULT_QUALIFICATION_RATE = 0.80  # 80% of raw form fills pass qualification gates

@dataclass
class TierProfile:
    name: str
    lead_share: float
    target_cpl: float
    schedule_rate: float
    show_rate: float
    attendee_conv_rate: float
    gross_list_arpu: float            # Before promotional voucher
    promo_dilution_per_student: float # BFCM / Holiday scholarship voucher
    representative_geos: str

    @property
    def net_booked_arpu(self) -> float:
        return self.gross_list_arpu - self.promo_dilution_per_student

# 3 Mutually Exclusive Tiers (Tier conversion rates and ARPUs marked as hypotheses to validate in 10-day test)
BASE_TIERS: List[TierProfile] = [
    TierProfile(
        name="Tier 1: Tech & Diaspora Metros",
        lead_share=0.30, # 1,650 leads
        target_cpl=36.00,
        schedule_rate=0.72,
        show_rate=0.76,
        attendee_conv_rate=0.22,
        gross_list_arpu=950.00,
        promo_dilution_per_student=100.00, # Net ARPU: $850.00
        representative_geos="CA (Fremont, Sunnyvale, Cupertino, San Jose, SF), WA (Bellevue, Redmond), TX (Austin), MA (Boston/Cambridge), NJ/NY (Edison, Jersey City), NC (Raleigh-Durham, Cary)"
    ),
    TierProfile(
        name="Tier 2: Affluent Suburban Corridors",
        lead_share=0.45, # 2,475 leads
        target_cpl=29.00,
        schedule_rate=0.68,
        show_rate=0.71,
        attendee_conv_rate=0.17,
        gross_list_arpu=850.00,
        promo_dilution_per_student=100.00, # Net ARPU: $750.00
        representative_geos="TX (Frisco, Plano, Allen, Sugar Land, Katy), GA (Alpharetta, Johns Creek), VA/MD (Fairfax, Loudoun, Potomac), CA (Orange County / Irvine), IL (Naperville, DuPage)"
    ),
    TierProfile(
        name="Tier 3: Inland & Heartland America",
        lead_share=0.25, # 1,375 leads
        target_cpl=24.00,
        schedule_rate=0.62,
        show_rate=0.64,
        attendee_conv_rate=0.13,
        gross_list_arpu=750.00,
        promo_dilution_per_student=100.00, # Net ARPU: $650.00
        representative_geos="OH, IN, MI, MO, KS, WI, Inland PA, and non-metro Sunbelt"
    )
]

# ==============================================================================
# 2. BASE MODEL ENGINE (EXACT SUM RECONCILIATION)
# ==============================================================================

def calculate_tier_funnel(t: TierProfile, total_leads: int) -> Dict[str, float]:
    leads = int(round(total_leads * t.lead_share))
    spend = leads * t.target_cpl
    sched = int(round(leads * t.schedule_rate))
    joined = int(round(sched * t.show_rate))
    paid = int(round(joined * t.attendee_conv_rate))
    
    gross_tcv = paid * t.gross_list_arpu
    promo_discount = paid * t.promo_dilution_per_student
    net_revenue = paid * t.net_booked_arpu
    
    delivery_cogs = net_revenue * (1.0 - ASSUMED_GROSS_MARGIN)
    gross_profit = net_revenue * ASSUMED_GROSS_MARGIN
    rev_less_media = net_revenue - spend
    # Labeled as Contribution (before closers/counselors, payment fees, refunds, creative production)
    contribution_margin = gross_profit - spend
    cac = spend / paid if paid > 0 else 0.0
    roas = net_revenue / spend if spend > 0 else 0.0
    cost_per_attended_demo = spend / joined if joined > 0 else 0.0

    return {
        "tier": t.name,
        "leads": leads,
        "cpl": t.target_cpl,
        "spend": spend,
        "sched": sched,
        "joined": joined,
        "paid": paid,
        "gross_tcv": gross_tcv,
        "promo_discount": promo_discount,
        "net_revenue": net_revenue,
        "gross_profit": gross_profit,
        "delivery_cogs": delivery_cogs,
        "rev_less_media": rev_less_media,
        "contribution_margin": contribution_margin,
        "cac": cac,
        "roas": roas,
        "cost_per_attended_demo": cost_per_attended_demo,
        "geos": t.representative_geos
    }

def run_base_model():
    tier_results = [calculate_tier_funnel(t, TOTAL_LEADS_TARGET) for t in BASE_TIERS]

    tot_leads = sum(r["leads"] for r in tier_results)
    tot_spend = sum(r["spend"] for r in tier_results)
    tot_sched = sum(r["sched"] for r in tier_results)
    tot_joined = sum(r["joined"] for r in tier_results)
    tot_paid = sum(r["paid"] for r in tier_results)
    tot_gross_tcv = sum(r["gross_tcv"] for r in tier_results)
    tot_promo = sum(r["promo_discount"] for r in tier_results)
    tot_net_rev = sum(r["net_revenue"] for r in tier_results)
    tot_cogs = sum(r["delivery_cogs"] for r in tier_results)
    tot_gp = sum(r["gross_profit"] for r in tier_results)
    tot_rev_less_media = tot_net_rev - tot_spend
    tot_contrib = tot_gp - tot_spend

    blended_cpl = tot_spend / tot_leads
    blended_cac = tot_spend / tot_paid
    blended_roas = tot_net_rev / tot_spend
    blended_show_rate = tot_joined / tot_sched
    blended_lead_to_paid = tot_paid / tot_leads
    blended_cost_per_attended = tot_spend / tot_joined
    blended_net_arpu = tot_net_rev / tot_paid

    # LTV/CAC clarification: Gross margin basis vs revenue ROAS
    first_order_gm_ltv_cac = (blended_net_arpu * ASSUMED_GROSS_MARGIN) / blended_cac

    # Break-even thresholds
    be_cpl = tot_gp / tot_leads                         # $36.76
    be_gross_margin = tot_spend / tot_net_rev           # 44.7%
    be_paid_students = (tot_spend / ASSUMED_GROSS_MARGIN) / blended_net_arpu
    be_close_rate = be_paid_students / tot_joined       # 14.5%

    # Cash timing
    upfront_cash = tot_net_rev * UPFRONT_CASH_COLLECTION_PCT
    installment_receivables = tot_net_rev * (1.0 - UPFRONT_CASH_COLLECTION_PCT)

    return {
        "tiers": tier_results,
        "totals": {
            "leads": tot_leads,
            "spend": tot_spend,
            "blended_cpl": blended_cpl,
            "sched": tot_sched,
            "joined": tot_joined,
            "show_rate": blended_show_rate,
            "paid": tot_paid,
            "lead_to_paid": blended_lead_to_paid,
            "gross_tcv": tot_gross_tcv,
            "promo_discount": tot_promo,
            "net_revenue": tot_net_rev,
            "net_arpu": blended_net_arpu,
            "upfront_cash": upfront_cash,
            "installment_receivables": installment_receivables,
            "gross_profit": tot_gp,
            "delivery_cogs": tot_cogs,
            "rev_less_media": tot_rev_less_media,
            "contribution_margin": tot_contrib,
            "cac": blended_cac,
            "roas": blended_roas,
            "first_order_gm_ltv_cac": first_order_gm_ltv_cac,
            "cost_per_attended_demo": blended_cost_per_attended,
            "break_even_roas": BREAK_EVEN_ROAS,
            "break_even_cpl": be_cpl,
            "break_even_gross_margin": be_gross_margin,
            "break_even_close_rate": be_close_rate
        }
    }

# ==============================================================================
# 3. RAW-TO-QUALIFIED LEAD BRIDGE
# ==============================================================================

def run_raw_lead_bridge() -> List[Dict[str, float]]:
    """Bridge calculating required raw form fills and max raw CPL at varying qualification pass rates."""
    target_qualified = TOTAL_LEADS_TARGET
    total_spend = 164175.00
    pass_rates = [0.90, 0.80, 0.70]
    results = []
    for rate in pass_rates:
        raw_leads = int(round(target_qualified / rate))
        max_raw_cpl = total_spend / raw_leads
        results.append({
            "pass_rate": rate,
            "qualified_leads": target_qualified,
            "raw_leads_needed": raw_leads,
            "max_raw_cpl": max_raw_cpl,
            "qualified_cpl": total_spend / target_qualified
        })
    return results

# ==============================================================================
# 4. SENSITIVITY SCENARIOS (CONTRIBUTION & STRESS TESTS)
# ==============================================================================

def run_key_sensitivity_scenarios() -> List[Dict[str, Any]]:
    """Specific stress scenarios showing impact on Contribution Margin."""
    base = run_base_model()["totals"]
    
    scenarios = [
        {
            "name": "Base Plan of Record",
            "condition": "CPL $29.85 | Show 71.0% | Close 17.9%",
            "spend": base["spend"],
            "net_rev": base["net_revenue"],
            "contrib": base["contribution_margin"],
            "notes": "Base case plan with 2.24x ROAS"
        },
        {
            "name": "CPL Inflation ($34.00)",
            "condition": "Blended CPL rises to $34.00 (+14%)",
            "spend": 5500 * 34.00,
            "net_rev": base["net_revenue"],
            "contrib": (base["net_revenue"] * ASSUMED_GROSS_MARGIN) - (5500 * 34.00),
            "notes": "+$15.2k contribution remaining"
        },
        {
            "name": "CPL Stress ($36.00)",
            "condition": "Blended CPL rises to $36.00 (+21%)",
            "spend": 5500 * 36.00,
            "net_rev": base["net_revenue"],
            "contrib": (base["net_revenue"] * ASSUMED_GROSS_MARGIN) - (5500 * 36.00),
            "notes": "+$4.2k contribution near break-even"
        },
        {
            "name": "Round 1 Show Rate (64.8%)",
            "condition": "Show rate drops to R1 actual (64.8%)",
            "spend": base["spend"],
            # Attended = 3,723 * 0.648 = 2,412.5 -> Paid = 2,412.5 * 0.179 = 431.84 -> Rev = 431.84 * 777.06 = $335,562
            "net_rev": (3723 * 0.648 * 0.179) * base["net_arpu"],
            "contrib": ((3723 * 0.648 * 0.179) * base["net_arpu"] * ASSUMED_GROSS_MARGIN) - base["spend"],
            "notes": "+$20.4k contribution (absorbed by volume)"
        },
        {
            "name": "Combined Headwind",
            "condition": "CPL $34.00 + Show Rate 64.8%",
            "spend": 5500 * 34.00,
            "net_rev": (3723 * 0.648 * 0.179) * base["net_arpu"],
            "contrib": ((3723 * 0.648 * 0.179) * base["net_arpu"] * ASSUMED_GROSS_MARGIN) - (5500 * 34.00),
            "notes": "-$2.5k slight operating deficit"
        },
        {
            "name": "Severe Q4 CPM Surge (+40%)",
            "condition": "CPL $41.79 (+40% CPM surge)",
            "spend": 5500 * (29.85 * 1.40),
            "net_rev": base["net_revenue"],
            "contrib": (base["net_revenue"] * ASSUMED_GROSS_MARGIN) - (5500 * (29.85 * 1.40)),
            "notes": "-$27.7k deficit without reallocation"
        }
    ]
    return scenarios

# ==============================================================================
# 5. THREE SCENARIOS COMPARISON (BASE vs. DOWNSIDE vs. UPSIDE)
# ==============================================================================

def run_scenarios_comparison():
    base = run_base_model()["totals"]

    # DOWNSIDE SCENARIO: CPL +15% ($34.33), Show Rate 55.0%, Demo-to-Paid 14.0%
    down_spend = TOTAL_LEADS_TARGET * (base["blended_cpl"] * 1.15)
    down_sched = int(TOTAL_LEADS_TARGET * 0.62) # 62% booking
    down_joined = int(down_sched * 0.55)        # 55% show rate
    down_paid = int(down_joined * 0.14)         # 14% demo-to-paid
    down_avg_arpu = 740.00
    down_rev = down_paid * down_avg_arpu
    down_gp = down_rev * ASSUMED_GROSS_MARGIN
    down_cac = down_spend / down_paid if down_paid > 0 else 0
    down_roas = down_rev / down_spend if down_spend > 0 else 0

    downside = {
        "scenario": "Downside (Stress Test)",
        "cpl": base["blended_cpl"] * 1.15,
        "spend": down_spend,
        "leads": TOTAL_LEADS_TARGET,
        "sched": down_sched,
        "joined": down_joined,
        "show_rate": 0.55,
        "paid": down_paid,
        "net_revenue": down_rev,
        "cac": down_cac,
        "roas": down_roas,
        "cost_per_attended": down_spend / down_joined if down_joined > 0 else 0,
        "break_even_roas": BREAK_EVEN_ROAS,
        "rev_less_media": down_rev - down_spend,
        "contrib_margin": down_gp - down_spend
    }

    # UPSIDE SCENARIO: CPL -10% ($26.87), Show Rate 76.0%, Demo-to-Paid 20.0%
    up_spend = TOTAL_LEADS_TARGET * (base["blended_cpl"] * 0.90)
    up_sched = int(TOTAL_LEADS_TARGET * 0.70)   # 70% booking
    up_joined = int(up_sched * 0.76)          # 76% show rate
    up_paid = int(up_joined * 0.20)           # 20% demo-to-paid
    up_avg_arpu = 765.00
    up_rev = up_paid * up_avg_arpu
    up_gp = up_rev * ASSUMED_GROSS_MARGIN
    up_cac = up_spend / up_paid if up_paid > 0 else 0
    up_roas = up_rev / up_spend if up_spend > 0 else 0

    upside = {
        "scenario": "Upside (Outperformance)",
        "cpl": base["blended_cpl"] * 0.90,
        "spend": up_spend,
        "leads": TOTAL_LEADS_TARGET,
        "sched": up_sched,
        "joined": up_joined,
        "show_rate": 0.76,
        "paid": up_paid,
        "net_revenue": up_rev,
        "cac": up_cac,
        "roas": up_roas,
        "cost_per_attended": up_spend / up_joined if up_joined > 0 else 0,
        "break_even_roas": BREAK_EVEN_ROAS,
        "rev_less_media": up_rev - up_spend,
        "contrib_margin": up_gp - up_spend
    }

    base_formatted = {
        "scenario": "Base Case (Current Plan)",
        "cpl": base["blended_cpl"],
        "spend": base["spend"],
        "leads": base["leads"],
        "sched": base["sched"],
        "joined": base["joined"],
        "show_rate": base["show_rate"],
        "paid": base["paid"],
        "net_revenue": base["net_revenue"],
        "cac": base["cac"],
        "roas": base["roas"],
        "cost_per_attended": base["cost_per_attended_demo"],
        "break_even_roas": BREAK_EVEN_ROAS,
        "rev_less_media": base["rev_less_media"],
        "contrib_margin": base["contribution_margin"]
    }

    return [base_formatted, downside, upside]

# ==============================================================================
# 6. SENSITIVITY TABLES (CPL VARIATION & VOLUME MIX SHIFTS)
# ==============================================================================

def run_sensitivity_cpl_shifts() -> List[Tuple[str, float, float, float]]:
    """Table 1: Blended CPL if each tier moves +/- 10%"""
    results = []
    shifts = [(-0.10, "Tier CPL -10% (Cost Savings)"),
              (0.00,  "Base Target CPL ($36 / $29 / $24)"),
              (0.10,  "Tier CPL +10% (CPM Inflation)")]
    
    for pct, label in shifts:
        cpl_t1 = 36.00 * (1.0 + pct)
        cpl_t2 = 29.00 * (1.0 + pct)
        cpl_t3 = 24.00 * (1.0 + pct)
        blended = (0.30 * cpl_t1) + (0.45 * cpl_t2) + (0.25 * cpl_t3)
        total_spend = TOTAL_LEADS_TARGET * blended
        results.append((label, blended, total_spend, total_spend - TOTAL_MEDIA_BUDGET_CEILING))
    return results

def run_sensitivity_volume_mix_shifts() -> List[Tuple[str, str, float, float, int, float]]:
    """Table 2: Shifting volume mix between tiers"""
    mixes = [
        ("Tech Heavy (Quality Focus)",      0.40, 0.40, 0.20),
        ("Base Balanced Plan (Current)",    0.30, 0.45, 0.25),
        ("Heartland Heavy (Cost Buffer)",   0.20, 0.45, 0.35)
    ]
    results = []
    for label, s1, s2, s3 in mixes:
        cpl = (s1 * 36.00) + (s2 * 29.00) + (s3 * 24.00)
        spend = TOTAL_LEADS_TARGET * cpl
        
        # Calculate paid students
        p1 = int(round(TOTAL_LEADS_TARGET * s1 * 0.72 * 0.76 * 0.22))
        p2 = int(round(TOTAL_LEADS_TARGET * s2 * 0.68 * 0.71 * 0.17))
        p3 = int(round(TOTAL_LEADS_TARGET * s3 * 0.62 * 0.64 * 0.13))
        paid = p1 + p2 + p3
        rev = (p1 * 850.00) + (p2 * 750.00) + (p3 * 650.00)
        
        results.append((label, f"{int(s1*100)}/{int(s2*100)}/{int(s3*100)}", cpl, spend, paid, rev))
    return results

# ==============================================================================
# 7. MONTHLY SEASONALITY & PACING MODEL
# ==============================================================================

def run_monthly_pacing_model():
    """Monthly breakdown modeling Q4 CPM surge in November and post-BFCM gifting in December."""
    nov_leads = NOV_LEADS_TARGET # 2,500
    dec_leads = DEC_LEADS_TARGET # 3,000
    
    # November has higher CPMs due to BFCM competition ($30.80 CPL)
    # December blends down ($29.06 CPL) as gifting/New Year intent ramps up
    nov_spend = 77000.00 # $30.80 CPL
    dec_spend = 87175.00 # $29.06 CPL
    total_spend = nov_spend + dec_spend # $164,175.00
    
    return {
        "nov": {"leads": nov_leads, "spend": nov_spend, "cpl": nov_spend / nov_leads},
        "dec": {"leads": dec_leads, "spend": dec_spend, "cpl": dec_spend / dec_leads},
        "total": {"leads": nov_leads + dec_leads, "spend": total_spend, "cpl": total_spend / (nov_leads + dec_leads)}
    }

# ==============================================================================
# 8. CLI OUTPUT RUNNER
# ==============================================================================

def print_full_model():
    model_data = run_base_model()
    t_res = model_data["tiers"]
    tot = model_data["totals"]

    print("=" * 105)
    print("BRIGHTCHAMPS USA Q4 (NOV-DEC 2026) UNIT ECONOMICS & FINANCIAL MODEL")
    print(f"Mandate: {TOTAL_LEADS_TARGET:,} Leads @ ${TARGET_BLENDED_CPL_CEILING:.2f} Target Blended CPL | Budget Ceiling: ${TOTAL_MEDIA_BUDGET_CEILING:,.2f}")
    print(f"Gross Margin Input: {ASSUMED_GROSS_MARGIN*100:.1f}% (Assumed) | Break-Even ROAS: {BREAK_EVEN_ROAS:.2f}x")
    print("=" * 105)

    print(f"\n{'Tier / Cohort':<30} | {'Leads':<6} | {'CPL':<6} | {'Spend ($)':<10} | {'Sched':<6} | {'Joined':<6} | {'Cost/Att':<8} | {'Paid':<5} | {'Net Rev ($)':<11}")
    print("-" * 105)

    for r in t_res:
        print(f"{r['tier']:<30} | {r['leads']:6,d} | ${r['cpl']:4.2f} | ${r['spend']:9,.2f} | {r['sched']:6,d} | {r['joined']:6,d} | ${r['cost_per_attended_demo']:6.2f} | {r['paid']:5,d} | ${r['net_revenue']:10,.2f}")

    print("-" * 105)
    print(f"{'TOTAL / RECONCILED SUM':<30} | {tot['leads']:6,d} | ${tot['blended_cpl']:4.2f} | ${tot['spend']:9,.2f} | {tot['sched']:6,d} | {tot['joined']:6,d} | ${tot['cost_per_attended_demo']:6.2f} | {tot['paid']:5,d} | ${tot['net_revenue']:10,.2f}")
    print("=" * 105)

    print("\n[A] P&L RECONCILIATION & KEY FINANCIAL RATIOS:")
    print(f"  • Gross List TCV (Contract Value):     ${tot['gross_tcv']:,.2f}")
    print(f"  • Promo Voucher Dilution ($100/lead):  -${tot['promo_discount']:,.2f}")
    print(f"  • Net Booked Revenue:                  ${tot['net_revenue']:,.2f} (Exact sum of tiers)")
    print(f"  • Media Spend:                         ${tot['spend']:,.2f} (Under ceiling by ${TOTAL_MEDIA_BUDGET_CEILING - tot['spend']:,.2f})")
    print(f"  • Revenue Less Media Spend:            ${tot['rev_less_media']:,.2f}")
    print(f"  • Delivery COGS (45% assumed):         ${tot['delivery_cogs']:,.2f} (Mentor payout + platform infra)")
    print(f"  • Contribution (before closers/counselors, payment fees, refunds, creative): ${tot['contribution_margin']:,.2f} (10.3% margin)")
    print(f"  • First-Order Media ROAS:              {tot['roas']:.2f}x (Break-Even ROAS: {tot['break_even_roas']:.2f}x)")
    print(f"  • Blended CAC per Enrolled Student:    ${tot['cac']:.2f}")
    print(f"  • Cost Per Attended Demo (North Star): ${tot['cost_per_attended_demo']:.2f}")
    print(f"  • First-Order Gross-Margin LTV/CAC:    {tot['first_order_gm_ltv_cac']:.2f}x (Net ARPU $777.06 * 55% GM / CAC $347.09)")
    print(f"  • Cash Collected (within 30d of lead): ${tot['upfront_cash']:,.2f} (75% upfront liquidity)")
    print(f"  • Trailing Installments (M2-3):        ${tot['installment_receivables']:,.2f}")

    print("\n[B] BREAK-EVEN THRESHOLDS (SENSITIVITY ANALYSIS):")
    print(f"  • Break-Even CPL:          ${tot['break_even_cpl']:.2f} (CPL ceiling before contribution turns negative)")
    print(f"  • Break-Even Gross Margin: {tot['break_even_gross_margin']*100:.1f}% (Minimum gross margin required at $164k media spend)")
    print(f"  • Break-Even Close Rate:   {tot['break_even_close_rate']*100:.1f}% (Minimum demo-to-paid rate required)")

    print("\n[C] RAW-TO-QUALIFIED LEAD BRIDGE:")
    print("  Definition of Qualified: OTP-verified US mobile + valid parent email + self-reported laptop access")
    print(f"  {'Pass Rate (%)':<15} | {'Raw Leads Needed':<18} | {'Qualified Leads':<16} | {'Max Raw CPL ($)':<16}")
    print("  " + "-" * 70)
    for b in run_raw_lead_bridge():
        print(f"  {b['pass_rate']*100:5.1f}%          | {b['raw_leads_needed']:18,d} | {b['qualified_leads']:16,d} | ${b['max_raw_cpl']:14.2f}")
    print("  Benchmarks: Facebook US education lead CPL: $22.83 (avg) to $34.85 (NA high). Lead forms $34.10 vs Instant Experience $49.70.")

    print("\n[D] CONTRIBUTION SENSITIVITY & HEADWIND SCENARIOS:")
    print(f"  {'Scenario':<28} | {'Condition':<36} | {'Spend ($)':<11} | {'Contrib ($)':<12} | {'Notes'}")
    print("  " + "-" * 105)
    for s in run_key_sensitivity_scenarios():
        print(f"  {s['name']:<28} | {s['condition']:<36} | ${s['spend']:9,.2f} | ${s['contrib']:10,.2f} | {s['notes']}")

    print("\n[E] SCENARIOS COMPARISON TABLE (BASE vs. DOWNSIDE vs. UPSIDE):")
    scenarios = run_scenarios_comparison()
    print(f"  {'Metric / Parameter':<26} | {'Base Case':<18} | {'Downside (Stress)':<18} | {'Upside (Outperform)':<18}")
    print("  " + "-" * 85)
    for k, label in [("cpl", "Blended CPL ($)"), ("spend", "Media Spend ($)"), ("show_rate", "Show Rate (%)"), 
                     ("cost_per_attended", "Cost/Attended Demo ($)"), ("paid", "Enrolled Students"), 
                     ("cac", "Blended CAC ($)"), ("net_revenue", "Net Revenue ($)"), 
                     ("roas", "ROAS (x)"), ("contrib_margin", "Contribution ($)")]:
        b_val = f"${scenarios[0][k]:,.2f}" if k in ["cpl", "spend", "cost_per_attended", "cac", "net_revenue", "contrib_margin"] else (f"{scenarios[0][k]*100:.1f}%" if k == "show_rate" else (f"{scenarios[0][k]:.2f}x" if k == "roas" else f"{scenarios[0][k]:,d}"))
        d_val = f"${scenarios[1][k]:,.2f}" if k in ["cpl", "spend", "cost_per_attended", "cac", "net_revenue", "contrib_margin"] else (f"{scenarios[1][k]*100:.1f}%" if k == "show_rate" else (f"{scenarios[1][k]:.2f}x" if k == "roas" else f"{scenarios[1][k]:,d}"))
        u_val = f"${scenarios[2][k]:,.2f}" if k in ["cpl", "spend", "cost_per_attended", "cac", "net_revenue", "contrib_margin"] else (f"{scenarios[2][k]*100:.1f}%" if k == "show_rate" else (f"{scenarios[2][k]:.2f}x" if k == "roas" else f"{scenarios[2][k]:,d}"))
        print(f"  {label:<26} | {b_val:<18} | {d_val:<18} | {u_val:<18}")

    print("\n[F] MONTHLY PACING & SEASONALITY:")
    m = run_monthly_pacing_model()
    print(f"  • November: {m['nov']['leads']:,d} Qualified Leads | Spend: ${m['nov']['spend']:,.2f} | CPL: ${m['nov']['cpl']:.2f} (Thanksgiving spend pause + BFCM ramp)")
    print(f"  • December: {m['dec']['leads']:,d} Qualified Leads | Spend: ${m['dec']['spend']:,.2f} | CPL: ${m['dec']['cpl']:.2f} (STEM holiday gifting + New Year 2027 headstart)")
    print(f"  • Total:    {m['total']['leads']:,d} Qualified Leads | Spend: ${m['total']['spend']:,.2f} | CPL: ${m['total']['cpl']:.2f}")

if __name__ == "__main__":
    print_full_model()
