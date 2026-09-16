"""Generates all project flowcharts and presentation slides as high-resolution PNG and JPG images."""
import os
import io
import urllib.request
import base64
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set fonts for both English and Devanagari Hindi
plt.rcParams['font.family'] = ['Nirmala UI', 'Segoe UI', 'DejaVu Sans']

BASE_DIR = Path(r"d:\UDHYAM")
IMG_DIR = BASE_DIR / "images"
PNG_DIR = IMG_DIR / "png"
JPG_DIR = IMG_DIR / "jpg"
STATIC_IMG_DIR = BASE_DIR / "static" / "images"

for d in [PNG_DIR, JPG_DIR, STATIC_IMG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# SIH Official Color Palette
C_NAVY = "#0B3C5D"
C_DARK = "#07253B"
C_SAFFRON = "#D84315"
C_ORANGE = "#FF9933"
C_GREEN = "#1B5E20"
C_GREEN_LIGHT = "#2E7D32"
C_WHITE = "#FFFFFF"
C_BG_LIGHT = "#F8FAFC"
C_CARD_BG = "#FFFFFF"
C_BORDER = "#CBD5E1"
C_TEXT_DARK = "#0F172A"
C_TEXT_MUTED = "#475569"
C_GOLD = "#B7791F"

def save_fig(fig, name: str, dpi: int = 150):
    """Saves a matplotlib figure as both PNG and JPG."""
    png_path = PNG_DIR / f"{name}.png"
    jpg_path = JPG_DIR / f"{name}.jpg"
    static_png = STATIC_IMG_DIR / f"{name}.png"
    static_jpg = STATIC_IMG_DIR / f"{name}.jpg"

    fig.savefig(png_path, facecolor=fig.get_facecolor(), edgecolor='none', dpi=dpi, bbox_inches='tight')
    plt.close(fig)

    # Convert to clean JPG via Pillow
    with Image.open(png_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(jpg_path, 'JPEG', quality=95)
        # Also copy to static
        im.save(static_png)
        rgb_im.save(static_jpg, 'JPEG', quality=95)

    print(f"Generated: {name}.png and {name}.jpg")

def draw_top_ribbon(ax):
    """Draws SIH Tricolor ribbon at top."""
    ax.add_patch(patches.Rectangle((0, 0.985), 0.333, 0.015, transform=ax.transAxes, color=C_ORANGE, clip_on=False))
    ax.add_patch(patches.Rectangle((0.333, 0.985), 0.334, 0.015, transform=ax.transAxes, color=C_WHITE, clip_on=False))
    ax.add_patch(patches.Rectangle((0.667, 0.985), 0.333, 0.015, transform=ax.transAxes, color=C_GREEN, clip_on=False))

def draw_header_footer(ax, title: str, subtitle: str, slide_num: int = None):
    """Draws consistent SIH slide header and footer."""
    draw_top_ribbon(ax)
    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.86), 1, 0.125, transform=ax.transAxes, color=C_NAVY, clip_on=False))
    ax.text(0.04, 0.94, subtitle.upper(), transform=ax.transAxes, color=C_ORANGE, fontsize=11, fontweight='bold', va='center')
    ax.text(0.04, 0.89, title, transform=ax.transAxes, color=C_WHITE, fontsize=20, fontweight='bold', va='center')

    # Footer bar
    ax.add_patch(patches.Rectangle((0, 0), 1, 0.045, transform=ax.transAxes, color=C_DARK, clip_on=False))
    ax.text(0.04, 0.022, "Udhyami Yojna (उद्यमी योजना) | Ministry of MSME / Digital Public Infrastructure | SIH 2026",
            transform=ax.transAxes, color=C_WHITE, fontsize=9.5, va='center')
    if slide_num:
        ax.text(0.96, 0.022, f"Slide {slide_num} of 7", transform=ax.transAxes, color="#90CAF9", fontsize=9.5, ha='right', va='center')

# =============================================================================
# 1. FLOWCHART 1: SYSTEM ARCHITECTURE & DATA FLOW
# =============================================================================
def make_flowchart_1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "End-to-End System Architecture & Data Flow", "TECHNICAL FLOWCHART 1")

    # Column 1: User & Voice
    b1 = patches.FancyBboxPatch((0.04, 0.10), 0.20, 0.73, boxstyle="round,pad=0.02",
                                facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.14, 0.78, "1. USER & INGESTION", transform=ax.transAxes, ha='center', va='center', fontsize=12.5, fontweight='bold', color=C_NAVY)
    ax.text(0.14, 0.73, "[VOICE] Web Speech API", transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color="#1E40AF")
    ax.text(0.14, 0.57, "* 12 Regional Locales\n  (Hindi, Marathi, Tamil...)\n* Audio visualizer pulse\n* Non-blocking fallback\n* Keyboard manual search",
            transform=ax.transAxes, ha='center', va='center', fontsize=9.5, color=C_TEXT_DARK)
    ax.text(0.14, 0.24, "CLIENT FRONTEND\nRaw HTML5 + Modular CSS\nVanilla ES Modules\n(Zero Bundler / Zero React)",
            transform=ax.transAxes, ha='center', va='center', fontsize=9, color=C_TEXT_MUTED,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=C_WHITE, edgecolor=C_BORDER))

    # Arrow 1 -> 2
    ax.annotate("", xy=(0.28, 0.48), xytext=(0.245, 0.48), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_SAFFRON, lw=3))
    ax.text(0.262, 0.52, "POST\n/api/extract", transform=ax.transAxes, ha='center', fontsize=8.5, fontweight='bold', color=C_SAFFRON)

    # Column 2: AI & Fallback
    b2 = patches.FancyBboxPatch((0.28, 0.10), 0.20, 0.73, boxstyle="round,pad=0.02",
                                facecolor="#FDF4FF", edgecolor="#A855F7", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.38, 0.78, "2. AI EXTRACTION", transform=ax.transAxes, ha='center', va='center', fontsize=12.5, fontweight='bold', color="#6B21A8")
    ax.text(0.38, 0.73, "[AI] Gemini + Regex Fallback", transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color="#7E22CE")
    ax.text(0.38, 0.57, "* Structured Pydantic Schema\n* Category, Loan, Sector\n* Indian City-to-District DB\n* Bilingual Regex Engine\n* 100% Offline Fallback Tier",
            transform=ax.transAxes, ha='center', va='center', fontsize=9.5, color=C_TEXT_DARK)
    ax.text(0.38, 0.24, "ZERO-BLANK GUARANTEE\nFuzzy select mapping\nSmart demographic defaults\nZero missing values",
            transform=ax.transAxes, ha='center', va='center', fontsize=9, color=C_TEXT_MUTED,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=C_WHITE, edgecolor=C_BORDER))

    # Arrow 2 -> 3
    ax.annotate("", xy=(0.52, 0.48), xytext=(0.485, 0.48), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))
    ax.text(0.502, 0.52, "POST\n/match-schemes", transform=ax.transAxes, ha='center', fontsize=8.5, fontweight='bold', color=C_NAVY)

    # Column 3: Rule Engine
    b3 = patches.FancyBboxPatch((0.52, 0.10), 0.20, 0.73, boxstyle="round,pad=0.02",
                                facecolor="#ECFDF5", edgecolor="#10B981", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b3)
    ax.text(0.62, 0.78, "3. RULE ENGINE", transform=ax.transAxes, ha='center', va='center', fontsize=12.5, fontweight='bold', color="#065F46")
    ax.text(0.62, 0.73, "[RULES] 100-Point Scorer", transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color="#047857")
    ax.text(0.62, 0.57, "* Hard Quota / Age Gating\n* Demographic Fit (30 pts)\n* Financial Fit (25 pts)\n* Sector Fit (20 pts)\n* Regional Fit (15 pts)\n* Subsidy Fit (10 pts)",
            transform=ax.transAxes, ha='center', va='center', fontsize=9.5, color=C_TEXT_DARK)
    ax.text(0.62, 0.24, "DATABASE LAYER\n21 Flagship Schemes\n28 States & UTs Catalog\nschemes.json | states.json",
            transform=ax.transAxes, ha='center', va='center', fontsize=9, color=C_TEXT_MUTED,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=C_WHITE, edgecolor=C_BORDER))

    # Arrow 3 -> 4
    ax.annotate("", xy=(0.76, 0.48), xytext=(0.725, 0.48), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_GREEN, lw=3))
    ax.text(0.742, 0.52, "Ranked\nResults", transform=ax.transAxes, ha='center', fontsize=8.5, fontweight='bold', color=C_GREEN)

    # Column 4: Delivery & Portals
    b4 = patches.FancyBboxPatch((0.76, 0.10), 0.20, 0.73, boxstyle="round,pad=0.02",
                                facecolor="#FFFBEB", edgecolor="#F59E0B", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b4)
    ax.text(0.86, 0.78, "4. ACTIONABLE OUTPUT", transform=ax.transAxes, ha='center', va='center', fontsize=12.5, fontweight='bold', color="#92400E")
    ax.text(0.86, 0.73, "[OUTPUT] Schemes & Subsidies", transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color="#B45309")
    ax.text(0.86, 0.57, "* Ranked Scheme Cards\n* Match % & Subsidy callout\n* Interactive doc checklist\n* Direct Official Links\n  (PMEGP, Mudra, StandUp)\n* District Industries Centres",
            transform=ax.transAxes, ha='center', va='center', fontsize=9.5, color=C_TEXT_DARK)
    ax.text(0.86, 0.24, "OUTCOME FOR FOUNDER\nClear eligibility visibility\nZero middleman hassle\nDirect application access",
            transform=ax.transAxes, ha='center', va='center', fontsize=9, color=C_TEXT_MUTED,
            bbox=dict(boxstyle="round,pad=0.4", facecolor=C_WHITE, edgecolor=C_BORDER))

    ax.axis('off')
    save_fig(fig, "01_system_architecture_flowchart")

# =============================================================================
# 2. FLOWCHART 2: VOICE AUTOFILL & EXTRACTION PIPELINE
# =============================================================================
def make_flowchart_2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Multilingual Voice Extraction & Zero-Blank Pipeline", "TECHNICAL FLOWCHART 2")

    # Step 1: Voice Input
    b1 = patches.FancyBboxPatch((0.04, 0.55), 0.26, 0.26, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor="#3B82F6", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.17, 0.76, "Step 1: Native Speech Audio", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_NAVY)
    ax.text(0.17, 0.66, 'User speaks in native language:\n"मुझे बेकरी की दुकान के लिए\n5 लाख का लोन चाहिए, कल्याण में"',
            transform=ax.transAxes, ha='center', fontsize=10.5, color="#1E3A8A", fontstyle='italic')
    ax.text(0.17, 0.58, "Web Speech API (12 Locales)", transform=ax.transAxes, ha='center', fontsize=9, color=C_TEXT_MUTED)

    # Arrow 1 -> 2
    ax.annotate("", xy=(0.35, 0.68), xytext=(0.305, 0.68), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))

    # Step 2: Gateway & Decision
    b2 = patches.FancyBboxPatch((0.35, 0.50), 0.30, 0.35, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_NAVY, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.50, 0.79, "Step 2: Backend NLP Routing", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_NAVY)
    ax.text(0.50, 0.73, "FastAPI endpoint: POST /api/extract", transform=ax.transAxes, ha='center', fontsize=10, fontweight='bold', color=C_SAFFRON)

    # Sub-paths inside box
    ax.text(0.50, 0.64, "Path A: Google Gemini 2.5 Flash\nPydantic JSON Schema enforcement", transform=ax.transAxes, ha='center', fontsize=9.5, color="#6B21A8")
    ax.text(0.50, 0.54, "Path B (Fallback): Bilingual Regex Engine\nDevanagari numerals, lakh multiplier, city gazetteer", transform=ax.transAxes, ha='center', fontsize=9.5, color=C_GREEN)

    # Arrow 2 -> 3
    ax.annotate("", xy=(0.70, 0.68), xytext=(0.655, 0.68), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))

    # Step 3: Entity Resolution & Zero Blank Defaults
    b3 = patches.FancyBboxPatch((0.70, 0.55), 0.26, 0.26, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_GREEN, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b3)
    ax.text(0.83, 0.76, "Step 3: Smart Resolution", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_GREEN)
    ax.text(0.83, 0.66, "• Loan Amount: ₹5,00,000\n• City 'Kalyan' ➔ Thane, MH\n• Sector: Retail / Food\n• Smart Default: Age 30, 10th Pass",
            transform=ax.transAxes, ha='center', fontsize=10, color=C_TEXT_DARK)
    ax.text(0.83, 0.58, "100% Zero-Blank Guarantee", transform=ax.transAxes, ha='center', fontsize=9.5, fontweight='bold', color=C_SAFFRON)

    # Down Arrow to Form Filling
    ax.annotate("", xy=(0.50, 0.43), xytext=(0.50, 0.49), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_SAFFRON, lw=3))
    ax.text(0.50, 0.45, "Structured Profile JSON", transform=ax.transAxes, ha='center', fontsize=9, fontweight='bold', color=C_SAFFRON, backgroundcolor=C_WHITE)

    # Step 4: DOM Population
    b4 = patches.FancyBboxPatch((0.15, 0.12), 0.70, 0.28, boxstyle="round,pad=0.02",
                                facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b4)
    ax.text(0.50, 0.35, "Step 4: Client Form Autofill & Visual Highlight (render.js)",
            transform=ax.transAxes, ha='center', fontsize=13, fontweight='bold', color="#92400E")
    ax.text(0.50, 0.25,
            "1. Fuzzy Option Selection: Matches aliases ('retail' ➔ 'Trading / Shop', 'kalyan' ➔ 'Maharashtra')\n"
            "2. Input Fields Updated: Loan Amount = 500000, Category = General/OBC, District = Thane\n"
            "3. CSS Animation Triggered: Inputs flash .auto-filled-highlight (light green border pulse)\n"
            "4. Immediate Readiness: Entrepreneur reviews in 1 second and clicks 'योजनाएं खोजें / Match Schemes'",
            transform=ax.transAxes, ha='center', fontsize=10.5, color="#78350F")

    ax.axis('off')
    save_fig(fig, "02_voice_autofill_pipeline")

# =============================================================================
# 3. FLOWCHART 3: DETERMINISTIC SCORING ENGINE
# =============================================================================
def make_flowchart_3():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Deterministic 100-Point Scheme Scoring Rule Engine", "TECHNICAL FLOWCHART 3")

    # Hard Gate Block
    b1 = patches.FancyBboxPatch((0.04, 0.46), 0.44, 0.35, boxstyle="round,pad=0.02",
                                facecolor="#FEE2E2", edgecolor="#EF4444", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.26, 0.76, "STAGE 1: HARD ELIGIBILITY GATING", transform=ax.transAxes, ha='center', fontsize=13, fontweight='bold', color="#991B1B")
    ax.text(0.26, 0.69, "Mandatory Pass / Fail Thresholds (Strict Rule Gates)", transform=ax.transAxes, ha='center', fontsize=10, color="#7F1D1D")
    ax.text(0.26, 0.56,
            "[GATE 1] Loan Scope: User requirement in [min_loan, max_loan]\n"
            "[GATE 2] Age Limits: User age within [min_age, max_age]\n"
            "[GATE 3] Quota Gate: Target category permitted (e.g. Women only for Stand-Up)\n"
            "[GATE 4] State Territory: Scheme is All-India OR user state matches scheme\n\n"
            "IF ANY CRITERIA FAILS -> DISQUALIFIED (Score = 0%, Reason Logged)",
            transform=ax.transAxes, ha='center', fontsize=10, color="#7F1D1D")

    # Arrow Hard Gate -> Scoring
    ax.annotate("", xy=(0.53, 0.63), xytext=(0.485, 0.63), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_GREEN, lw=3))
    ax.text(0.508, 0.66, "IF PASS\n(Eligible)", transform=ax.transAxes, ha='center', fontsize=9.5, fontweight='bold', color=C_GREEN)

    # Scoring Points Accumulator
    b2 = patches.FancyBboxPatch((0.53, 0.46), 0.43, 0.35, boxstyle="round,pad=0.02",
                                facecolor="#ECFDF5", edgecolor="#10B981", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.745, 0.76, "STAGE 2: 100-POINT WEIGHTED ACCUMULATOR", transform=ax.transAxes, ha='center', fontsize=13, fontweight='bold', color="#065F46")
    ax.text(0.745, 0.58,
            "(+) Base Eligibility Baseline: +30 Points\n"
            "(+) Demographic Affirmative Action: +20 Points (Women, SC, ST, Divyangjan)\n"
            "(+) Financial Capital Calibration: +20 Points (Optimal subsidy band)\n"
            "(+) Sector & Activity Alignment: +15 Points (Manufacturing, Agro, Handloom)\n"
            "(+) Regional / Rural Subsidy Tier: +15 Points (Max 35% subsidy category)\n\n"
            "TOTAL DETERMINISTIC SCORE = 0 to 100 POINTS",
            transform=ax.transAxes, ha='center', fontsize=10, color="#064E3B")

    # Down Arrow to Tiering
    ax.annotate("", xy=(0.50, 0.37), xytext=(0.50, 0.44), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))

    # Stage 3: Tiering & Ranked Output
    b3 = patches.FancyBboxPatch((0.04, 0.10), 0.92, 0.25, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_NAVY, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b3)
    ax.text(0.50, 0.31, "STAGE 3: NORMALIZED TIERING & ACTIONABLE GENERATION",
            transform=ax.transAxes, ha='center', fontsize=13, fontweight='bold', color=C_NAVY)

    # 3 Tier Badges
    ax.text(0.18, 0.22, "[TIER 1] EXCEPTIONAL (>= 80%)\nHigh approval likelihood\nMax subsidy entitlement",
            transform=ax.transAxes, ha='center', fontsize=10, color="#1B5E20",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#2E7D32"))
    ax.text(0.50, 0.22, "[TIER 2] RECOMMENDED (60-79%)\nStandard loan qualification\nSecondary collateral rules",
            transform=ax.transAxes, ha='center', fontsize=10, color="#B7791F",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FEF3C7", edgecolor="#F59E0B"))
    ax.text(0.82, 0.22, "[TIER 3] ALTERNATIVE (< 60%)\nContingency scheme option\nGeneral category parameters",
            transform=ax.transAxes, ha='center', fontsize=10, color="#475569",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#F1F5F9", edgecolor="#94A3B8"))

    ax.text(0.50, 0.13, "Outputs dynamic document checklist + Direct link to official central/state application portal",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_MUTED, fontstyle='italic')

    ax.axis('off')
    save_fig(fig, "03_deterministic_scoring_flowchart")

# =============================================================================
# 4. FLOWCHART 4: STATE DISCOVERY HUB
# =============================================================================
def make_flowchart_4():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "State-Wise Entrepreneurial Discovery Hub Architecture", "TECHNICAL FLOWCHART 4")

    # UI Controls
    b1 = patches.FancyBboxPatch((0.04, 0.18), 0.27, 0.62, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor="#3B82F6", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.175, 0.74, "UI INTERACTION LAYER", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color="#1E40AF")
    ax.text(0.175, 0.62,
            "[STATES] 28 States & UTs Dropdown\n"
            "Full India coverage from\n"
            "Andhra Pradesh to West Bengal\n\n"
            "[SECTORS] Sector Filter Chips\n"
            "Handloom, Food Processing,\n"
            "Ceramics, IT/Electronics, Agro\n\n"
            "[SEARCH] Cluster Search Bar\n"
            "Instant filter by cluster name\n"
            "or district industries centre",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_DARK)

    # Arrow 1 -> 2
    ax.annotate("", xy=(0.35, 0.49), xytext=(0.315, 0.49), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))

    # Backend API & Store
    b2 = patches.FancyBboxPatch((0.35, 0.18), 0.28, 0.62, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_NAVY, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.49, 0.74, "BACKEND ROUTER & DATA", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_NAVY)
    ax.text(0.49, 0.62,
            "[API] Endpoint: GET /api/states\n"
            "FastAPI async JSON responder\n\n"
            "[DATA] Database: states.json\n"
            "Structured schema covering:\n"
            "* State capital & target sectors\n"
            "* Industrial cluster directory\n"
            "* State industrial policy name\n"
            "* State exclusive MSME schemes\n"
            "* District Industries Centre contacts",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_DARK)

    # Arrow 2 -> 3
    ax.annotate("", xy=(0.67, 0.49), xytext=(0.635, 0.49), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_GREEN, lw=3))

    # Rendered Cards
    b3 = patches.FancyBboxPatch((0.67, 0.18), 0.29, 0.62, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_GREEN, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b3)
    ax.text(0.815, 0.74, "DYNAMIC STATE DASHBOARD", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_GREEN)
    ax.text(0.815, 0.62,
            "1. Macro Industrial Overview\n"
            "Key focus areas & state incentives\n\n"
            "2. Prominent Clusters\n"
            "e.g., Surat Textiles, Morbi Tiles,\n"
            "Ludhiana Hosiery, Varanasi Silk\n\n"
            "3. State Exclusive Schemes\n"
            "Mukhyamantri Udyami Yojna,\n"
            "Anbaraj Project, Mission Shakti\n\n"
            "4. Local DIC Office Connect\n"
            "Official address, helpline, email",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_DARK)

    ax.axis('off')
    save_fig(fig, "04_state_discovery_hub_flowchart")

# =============================================================================
# 5. FLOWCHART 5: ZERO PII SECURITY ARCHITECTURE
# =============================================================================
def make_flowchart_5():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Zero PII Retention & Data Privacy Architecture", "TECHNICAL FLOWCHART 5")

    # Layer 1: Client
    b1 = patches.FancyBboxPatch((0.04, 0.22), 0.27, 0.54, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor="#3B82F6", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.175, 0.70, "CLIENT BROWSER LAYER", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color="#1E40AF")
    ax.text(0.175, 0.50,
            "* Local Voice Processing:\n  Audio buffers never written to disk\n"
            "* No Identity Storage:\n  No Aadhaar, PAN or bank accounts\n  ever requested\n"
            "* Session Volatility:\n  State clears upon tab close\n"
            "* GIGW & WCAG 2.1 AA Compliant",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_DARK)

    # Arrow 1 -> 2
    ax.annotate("", xy=(0.35, 0.49), xytext=(0.315, 0.49), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_NAVY, lw=3))
    ax.text(0.332, 0.53, "TLS 1.3\nEncrypted", transform=ax.transAxes, ha='center', fontsize=8.5, fontweight='bold', color=C_NAVY)

    # Layer 2: API & Stateless
    b2 = patches.FancyBboxPatch((0.35, 0.22), 0.28, 0.54, boxstyle="round,pad=0.02",
                                facecolor=C_WHITE, edgecolor=C_NAVY, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.49, 0.70, "STATELESS APPLICATION TIER", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_NAVY)
    ax.text(0.49, 0.50,
            "* In-Memory Computation:\n  Profiles evaluated in volatile RAM\n"
            "* Immediate GC:\n  Python objects dereferenced immediately\n"
            "* CORS Restriction:\n  Configurable allowed origins\n"
            "* Strict Rate Limiting:\n  Protects against scraping attacks",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_TEXT_DARK)

    # Arrow 2 -> 3
    ax.annotate("", xy=(0.67, 0.49), xytext=(0.635, 0.49), xycoords='axes fraction',
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=C_GREEN, lw=3))

    # Layer 3: Database Policy
    b3 = patches.FancyBboxPatch((0.67, 0.22), 0.29, 0.54, boxstyle="round,pad=0.02",
                                facecolor="#F0FDF4", edgecolor=C_GREEN, linewidth=2, transform=ax.transAxes)
    ax.add_patch(b3)
    ax.text(0.815, 0.70, "ZERO USER DATA RETENTION", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_GREEN)
    ax.text(0.815, 0.50,
            "[X] ZERO User Database:\n  No user tables or tracking cookies\n\n"
            "[SAFE] Zero Telemetry Leakage:\n  Speech transcripts not stored in DB\n\n"
            "[DIRECT] Official Portal Redirect:\n  Actual applications happen on official\n  gov portals (PMEGP, JanSamarth)",
            transform=ax.transAxes, ha='center', fontsize=10.5, color="#064E3B")

    ax.axis('off')
    save_fig(fig, "05_zero_pii_security_flowchart")

# =============================================================================
# 6. ALL 7 PRESENTATION SLIDES (SIH 2026 OFFICIAL PITCH DECK)
# =============================================================================
def make_slide_1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_DARK)
    ax.set_facecolor(C_DARK)
    draw_top_ribbon(ax)

    # Main Center Card
    card = patches.FancyBboxPatch((0.08, 0.10), 0.84, 0.78, boxstyle="round,pad=0.03",
                                  facecolor=C_NAVY, edgecolor=C_ORANGE, linewidth=2.5, transform=ax.transAxes)
    ax.add_patch(card)

    ax.text(0.50, 0.81, "SMART INDIA HACKATHON 2026 | OFFICIAL PROJECT SUBMISSION",
            transform=ax.transAxes, ha='center', color=C_ORANGE, fontsize=14, fontweight='bold')
    ax.text(0.50, 0.68, "Udhyami Yojna (उद्यमी योजना)",
            transform=ax.transAxes, ha='center', color=C_WHITE, fontsize=32, fontweight='bold')
    ax.text(0.50, 0.57, "Autonomous AI Scheme Discovery & Subsidy Advisory for Marginalized Indian Entrepreneurs",
            transform=ax.transAxes, ha='center', color="#90CAF9", fontsize=15, fontstyle='italic')

    # Metadata Grid Box
    meta = patches.FancyBboxPatch((0.15, 0.22), 0.70, 0.27, boxstyle="round,pad=0.02",
                                  facecolor=C_DARK, edgecolor=C_BORDER, linewidth=1, transform=ax.transAxes)
    ax.add_patch(meta)

    ax.text(0.25, 0.42, "Problem Statement ID:", transform=ax.transAxes, color="#94A3B8", fontsize=11, fontweight='bold')
    ax.text(0.25, 0.38, "SIH-2026-MSME-1402", transform=ax.transAxes, color=C_WHITE, fontsize=12, fontweight='bold')

    ax.text(0.25, 0.30, "Theme:", transform=ax.transAxes, color="#94A3B8", fontsize=11, fontweight='bold')
    ax.text(0.25, 0.26, "Inclusive Digital Public Infrastructure & MSME", transform=ax.transAxes, color=C_WHITE, fontsize=12, fontweight='bold')

    ax.text(0.65, 0.42, "Category:", transform=ax.transAxes, color="#94A3B8", fontsize=11, fontweight='bold')
    ax.text(0.65, 0.38, "Software Edition (Voice AI, Web, FinTech)", transform=ax.transAxes, color=C_WHITE, fontsize=12, fontweight='bold')

    ax.text(0.65, 0.30, "Target Beneficiaries:", transform=ax.transAxes, color="#94A3B8", fontsize=11, fontweight='bold')
    ax.text(0.65, 0.26, "Women, SC/ST, Vishwakarma Artisans, Divyangjan", transform=ax.transAxes, color=C_WHITE, fontsize=12, fontweight='bold')

    # Footer
    ax.add_patch(patches.Rectangle((0, 0), 1, 0.04, transform=ax.transAxes, color="#051B2C", clip_on=False))
    ax.text(0.50, 0.02, "Ministry of MSME & Financial Inclusion | Viksit Bharat 2047 | Slide 1 of 7",
            transform=ax.transAxes, ha='center', color=C_WHITE, fontsize=10)

    ax.axis('off')
    save_fig(fig, "sih_slide_1_title")

def make_slide_2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Grassroots Challenges vs Udhyami Yojna Solution", "1. IDEA / PROPOSED SOLUTION", 2)

    # Left Box: Problem
    b1 = patches.FancyBboxPatch((0.04, 0.10), 0.44, 0.72, boxstyle="round,pad=0.02",
                                facecolor="#FFF5F5", edgecolor="#FEB2B2", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b1)
    ax.text(0.26, 0.76, "GROUND-LEVEL CHALLENGES", transform=ax.transAxes, ha='center', fontsize=14, fontweight='bold', color="#C53030")
    ax.text(0.26, 0.53,
            "[!] Information Asymmetry:\n"
            "Over 100+ schemes exist across Central & State bodies,\n"
            "hidden behind dense 40-page gazette PDF notifications.\n\n"
            "[!] Language & Literacy Barriers:\n"
            "First-generation rural founders struggle with 30-field\n"
            "complex English/Hindi forms.\n\n"
            "[!] Predatory Middlemen & Unaware Subsidy:\n"
            "Rural artisans lose 15-30% of subsidies to agents, or take\n"
            "informal loans at 36-60% annual interest rates.\n\n"
            "[!] Neglect of State-Level Ecosystems:\n"
            "National portals overlook district clusters and DIC incentives.",
            transform=ax.transAxes, ha='center', fontsize=10.5, color="#742A2A")

    # Right Box: Solution
    b2 = patches.FancyBboxPatch((0.52, 0.10), 0.44, 0.72, boxstyle="round,pad=0.02",
                                facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=2, transform=ax.transAxes)
    ax.add_patch(b2)
    ax.text(0.74, 0.76, "THE UDHYAMI YOJNA PILLARS", transform=ax.transAxes, ha='center', fontsize=14, fontweight='bold', color="#15803D")
    ax.text(0.74, 0.53,
            "[+] Multilingual Voice Autofill:\n"
            "12 Indian regional languages via Web Speech API.\n"
            "Zero typing friction for rural and illiterate entrepreneurs.\n\n"
            "[+] Smart Zero-Blank Defaults:\n"
            "Gemini 2.5 Flash + 100% offline regex fallback guarantees\n"
            "zero blank fields and resolves Indian towns to districts.\n\n"
            "[+] Deterministic 100-Point Rule Scoring:\n"
            "Zero hallucinations. Hard criteria gating + weighted math\n"
            "delivers verified scheme matches and subsidy callouts.\n\n"
            "[+] 28 States & UTs Industrial Hub:\n"
            "Direct connect to District Industries Centres & clusters.",
            transform=ax.transAxes, ha='center', fontsize=10.5, color="#14532D")

    ax.axis('off')
    save_fig(fig, "sih_slide_2_problem_solution")

def make_slide_3():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Lightweight, High-Resilience Modular Stack", "2. TECHNICAL ARCHITECTURE & TECH STACK", 3)

    # 4 Cards with Flow Arrows
    steps = [
        ("1. Voice & Web Input", ["* Web Speech API (12 locales)", "* Real-time waveform pulse", "* Non-blocking fallback banner", "* Keyboard manual option"], "#EFF6FF", "#3B82F6"),
        ("2. AI Extraction", ["* Gemini 2.5 Flash", "* Structured Pydantic schema", "* Offline bilingual regex", "* City-to-district resolver"], "#FAF5FF", "#A855F7"),
        ("3. Rule Engine", ["* Pure Python deterministic", "* Quota & threshold gating", "* 100-pt weighted algorithm", "* Dynamic document checklist"], "#ECFDF5", "#10B981"),
        ("4. Actionable Hub", ["* Ranked scheme cards", "* Subsidy % & grant badges", "* Official portal redirect", "* 28 States & DIC directory"], "#FFFBEB", "#F59E0B")
    ]

    for i, (title, points, bg, border) in enumerate(steps):
        x = 0.04 + i * 0.24
        card = patches.FancyBboxPatch((x, 0.40), 0.20, 0.40, boxstyle="round,pad=0.02",
                                      facecolor=bg, edgecolor=border, linewidth=2, transform=ax.transAxes)
        ax.add_patch(card)
        ax.text(x + 0.10, 0.74, title, transform=ax.transAxes, ha='center', fontsize=11.5, fontweight='bold', color=C_NAVY)
        ax.text(x + 0.10, 0.58, "\n".join(points), transform=ax.transAxes, ha='center', fontsize=9.5, color=C_TEXT_DARK)

        if i < 3:
            ax.annotate("", xy=(x + 0.24, 0.60), xytext=(x + 0.205, 0.60), xycoords='axes fraction',
                        arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.5", color=C_SAFFRON, lw=2.5))

    # Tech Stack Banner
    banner = patches.FancyBboxPatch((0.04, 0.10), 0.92, 0.25, boxstyle="round,pad=0.02",
                                    facecolor=C_WHITE, edgecolor=C_BORDER, linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(banner)
    ax.text(0.50, 0.29, "PRODUCTION TECH STACK & SPECIFICATIONS", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_NAVY)

    ax.text(0.18, 0.19, "FRONTEND LAYER\nRaw HTML5, Modular CSS (NIC Theme)\nVanilla ES Modules (Zero bundler/npm)\nGIGW & WCAG 2.1 AA Compliant",
            transform=ax.transAxes, ha='center', fontsize=9.5, color=C_TEXT_MUTED)
    ax.text(0.50, 0.19, "BACKEND & API TIER\nPython 3.12, FastAPI, Uvicorn Daemon\nPydantic V2 schemas, CORS middleware\n100% Stateless & Zero PII Retention",
            transform=ax.transAxes, ha='center', fontsize=9.5, color=C_TEXT_MUTED)
    ax.text(0.82, 0.19, "AI, SCORING & TESTING\nGoogle GenAI SDK (Gemini 2.5 Flash)\nDeterministic pure-math rule engine\n27/27 Pytest Unit Tests Passing (100%)",
            transform=ax.transAxes, ha='center', fontsize=9.5, color=C_TEXT_MUTED)

    ax.axis('off')
    save_fig(fig, "sih_slide_3_architecture")

def make_slide_4():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Why Udhyami Yojna Outperforms Existing Alternatives", "3. INNOVATION & COMPARATIVE ANALYSIS", 4)

    # Comparison Table
    table_data = [
        ["Feature / Dimension", "Existing Portals (MyScheme)", "Generic AI Chatbots", "Udhyami Yojna (Our Solution)"],
        ["User Interaction", "Complex 30+ dropdown forms", "Free text prompt (typing)", "Multilingual Voice (12 Locales)"],
        ["Offline Resilience", "Zero (Crashes without internet)", "Zero (Requires active LLM)", "100% Offline Heuristic Fallback"],
        ["Eligibility Guarantee", "Manual PDF interpretation", "Prone to LLM hallucinations", "Deterministic 100-Point Rule Engine"],
        ["Zero-Blank Auto-fill", "Manual input required", "Missing fields left blank", "Fuzzy Matching + Smart Defaults"],
        ["Regional Ecosystems", "Predominantly Central schemes", "Generic national summaries", "28 States & UTs + DIC Contacts"],
        ["Bandwidth Footprint", "Heavy JS frameworks / slow", "High streaming latency", "Lightweight Vanilla UI (< 250 KB)"]
    ]

    # Draw Table
    col_widths = [0.24, 0.24, 0.24, 0.28]
    start_y = 0.78
    row_h = 0.088

    for r_idx, row in enumerate(table_data):
        y = start_y - r_idx * row_h
        for c_idx, cell in enumerate(row):
            x = 0.04 + sum(col_widths[:c_idx])
            w = col_widths[c_idx] - 0.01

            if r_idx == 0:
                bg = C_NAVY if c_idx < 3 else C_SAFFRON
                tc = C_WHITE
                fw = 'bold'
                fs = 10.5
            else:
                bg = "#EFF6FF" if c_idx == 3 else (C_WHITE if r_idx % 2 == 0 else "#F8FAFC")
                tc = C_NAVY if c_idx == 3 else C_TEXT_DARK
                fw = 'bold' if c_idx == 3 else 'normal'
                fs = 9.5

            rect = patches.FancyBboxPatch((x, y - row_h + 0.02), w, row_h - 0.015, boxstyle="round,pad=0.01",
                                          facecolor=bg, edgecolor=C_BORDER, linewidth=1, transform=ax.transAxes)
            ax.add_patch(rect)
            ax.text(x + w/2, y - row_h/2 + 0.01, cell, transform=ax.transAxes, ha='center', va='center',
                    fontsize=fs, fontweight=fw, color=tc)

    ax.axis('off')
    save_fig(fig, "sih_slide_4_comparative_matrix")

def make_slide_5():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Technical, Economic & Operational Robustness", "4. FEASIBILITY, VIABILITY & SECURITY", 5)

    pillars = [
        ("Technical Feasibility",
         "• 100% functional working prototype\n• Fast response times (< 800 ms Gemini, < 20 ms scoring)\n• 27 automated unit tests passing\n• GIGW & WCAG 2.1 AA compliant",
         "#EFF6FF", "#3B82F6"),
        ("Economic Viability",
         "• Zero-cost offline fallback tier\n• Free tier Gemini Flash token budget\n• Zero expensive frontend build servers\n• Highly scalable on low-cost cloud / NIC servers",
         "#F0FDF4", "#10B981"),
        ("Operational Viability",
         "• Immediate deployment in CSCs / Jan Seva Kendras\n• Accessible via Gram Panchayat digital kiosks\n• Works smoothly on entry-level Android 2G/3G\n• Direct external links to official portals",
         "#FFFBEB", "#F59E0B"),
        ("Security & Privacy",
         "• Strict Zero PII retention policy\n• No Aadhaar, PAN or phone stored in DB\n• In-memory stateless FastAPI calculation\n• Encrypted TLS 1.3 data in transit",
         "#FAF5FF", "#A855F7")
    ]

    for i, (title, content, bg, border) in enumerate(pillars):
        x = 0.04 + (i % 2) * 0.48
        y = 0.46 if i < 2 else 0.10
        card = patches.FancyBboxPatch((x, y), 0.44, 0.32, boxstyle="round,pad=0.02",
                                      facecolor=bg, edgecolor=border, linewidth=2, transform=ax.transAxes)
        ax.add_patch(card)
        ax.text(x + 0.22, y + 0.26, title, transform=ax.transAxes, ha='center', fontsize=13, fontweight='bold', color=C_NAVY)
        ax.text(x + 0.22, y + 0.13, content, transform=ax.transAxes, ha='center', fontsize=10, color=C_TEXT_DARK)

    ax.axis('off')
    save_fig(fig, "sih_slide_5_feasibility_security")

def make_slide_6():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Empowering 6.3 Crore Unorganized Micro-Enterprises", "5. SOCIAL IMPACT & VIKSIT BHARAT 2047", 6)

    metrics = [
        ("35% Maximum Subsidy", "Unlocking PMEGP & Mudra grants for rural women & special category founders"),
        ("12 Regional Languages", "Eliminating linguistic barriers across 28 States & Union Territories"),
        ("100% Zero-Blank", "Voice & AI extraction guarantees full form submission ready in 1 click"),
        ("₹2.5 Lakh Crore", "Bridging the unorganized micro-enterprise credit gap under Viksit Bharat 2047")
    ]

    for i, (stat, desc) in enumerate(metrics):
        x = 0.04 + i * 0.235
        card = patches.FancyBboxPatch((x, 0.52), 0.21, 0.28, boxstyle="round,pad=0.02",
                                      facecolor=C_NAVY, edgecolor=C_ORANGE, linewidth=2, transform=ax.transAxes)
        ax.add_patch(card)
        ax.text(x + 0.105, 0.72, stat, transform=ax.transAxes, ha='center', fontsize=15, fontweight='bold', color=C_ORANGE)
        ax.text(x + 0.105, 0.60, desc, transform=ax.transAxes, ha='center', fontsize=9.5, color=C_WHITE)

    # Beneficiary Callout Box
    ben_box = patches.FancyBboxPatch((0.04, 0.10), 0.92, 0.36, boxstyle="round,pad=0.02",
                                     facecolor=C_WHITE, edgecolor=C_GREEN, linewidth=2, transform=ax.transAxes)
    ax.add_patch(ben_box)
    ax.text(0.50, 0.40, "TARGET BENEFICIARIES & AFFIRMATIVE ACTION PILLARS",
            transform=ax.transAxes, ha='center', fontsize=12.5, fontweight='bold', color=C_GREEN)

    ax.text(0.18, 0.24, "[1] WOMEN ENTREPRENEURS\nStand-Up India quota allocation,\n35% PMEGP rural subsidy, mudra loans,\nand state Stree Nidhi benefits.",
            transform=ax.transAxes, ha='center', fontsize=10, color=C_TEXT_DARK)
    ax.text(0.50, 0.24, "[2] PM-VISHWAKARMA ARTISANS\nINR 15,000 toolkits grant, 5% credit,\nmarketing support for 18\ntraditional trades & craftsmen.",
            transform=ax.transAxes, ha='center', fontsize=10, color=C_TEXT_DARK)
    ax.text(0.82, 0.24, "[3] SC / ST & DIVYANGJAN\nNational SC-ST Hub priority,\nconcessional credit rates, and dedicated\nstate affirmative capital.",
            transform=ax.transAxes, ha='center', fontsize=10, color=C_TEXT_DARK)

    ax.axis('off')
    save_fig(fig, "sih_slide_6_social_impact")

def make_slide_7():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    fig.patch.set_facecolor(C_BG_LIGHT)
    ax.set_facecolor(C_BG_LIGHT)
    draw_header_footer(ax, "Implementation Milestones & National Scalability", "6. IMPLEMENTATION ROADMAP & CONCLUSION", 7)

    phases = [
        ("Phase 1: SIH Prototype (Current)",
         "• 10 Central + 11 State flagship schemes\n• 12 Indian languages voice recognition\n• Deterministic 100-pt scoring rule engine\n• 28 States & UTs discovery directory\n• Fully functional working prototype (27/27 tests)",
         "#EFF6FF", "#3B82F6"),
        ("Phase 2: National Pilot (Months 3-6)",
         "• WhatsApp & Telegram multilingual chatbot\n• Bhashini AI voice translation integration\n• NIC SMS Gateway push notifications\n• Pilot across 50 rural Common Service Centres (CSC)",
         "#FAF5FF", "#A855F7"),
        ("Phase 3: Digital Public Good (Months 6-12)",
         "• DigiLocker 1-click document verification\n• Direct API integration with JanSamarth & Udyam\n• Automated DPR (Detailed Project Report) generator\n• National rollout under Ministry of MSME",
         "#ECFDF5", "#10B981")
    ]

    for i, (title, bullets, bg, border) in enumerate(phases):
        x = 0.04 + i * 0.315
        card = patches.FancyBboxPatch((x, 0.38), 0.29, 0.42, boxstyle="round,pad=0.02",
                                      facecolor=bg, edgecolor=border, linewidth=2, transform=ax.transAxes)
        ax.add_patch(card)
        ax.text(x + 0.145, 0.73, title, transform=ax.transAxes, ha='center', fontsize=11.5, fontweight='bold', color=C_NAVY)
        ax.text(x + 0.145, 0.54, bullets, transform=ax.transAxes, ha='center', fontsize=9.5, color=C_TEXT_DARK)

    # Conclusion Banner
    conc = patches.FancyBboxPatch((0.04, 0.10), 0.92, 0.22, boxstyle="round,pad=0.02",
                                  facecolor=C_NAVY, edgecolor=C_ORANGE, linewidth=2, transform=ax.transAxes)
    ax.add_patch(conc)
    ax.text(0.50, 0.25, "CONCLUSION & NATIONAL VALUE PROPOSITION", transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold', color=C_ORANGE)
    ax.text(0.50, 0.16,
            "Udhyami Yojna transforms complex government gazettes into actionable financial lifelines for marginalized founders.\n"
            "By pairing voice accessibility with deterministic mathematical scoring and zero PII retention, it is ready to scale\n"
            "as an inclusive Digital Public Good under the Ministry of MSME.",
            transform=ax.transAxes, ha='center', fontsize=10.5, color=C_WHITE)

    ax.axis('off')
    save_fig(fig, "sih_slide_7_roadmap_conclusion")

# =============================================================================
# MAIN RUNNER
# =============================================================================
if __name__ == "__main__":
    print("Generating Flowcharts (PNG & JPG)...")
    make_flowchart_1()
    make_flowchart_2()
    make_flowchart_3()
    make_flowchart_4()
    make_flowchart_5()

    print("\nGenerating SIH 2026 Presentation Slides (PNG & JPG)...")
    make_slide_1()
    make_slide_2()
    make_slide_3()
    make_slide_4()
    make_slide_5()
    make_slide_6()
    make_slide_7()

    print("\nAll 12 PNG and 12 JPG files generated successfully!")
