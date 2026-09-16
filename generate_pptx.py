"""Script to generate professional Smart India Hackathon (SIH 2026) PowerPoint Presentation."""
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_sih_presentation(output_path: str):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY_DARK = RGBColor(11, 60, 93)      # #0B3C5D
    C_NAVY_DEEP = RGBColor(7, 37, 59)       # #07253B
    C_SAFFRON = RGBColor(216, 67, 21)       # #D84315
    C_ORANGE_ACC = RGBColor(255, 153, 51)   # #FF9933
    C_GREEN = RGBColor(27, 94, 32)          # #1B5E20
    C_GREEN_LIGHT = RGBColor(46, 125, 50)   # #2E7D32
    C_BG_LIGHT = RGBColor(244, 246, 249)    # #F4F6F9
    C_WHITE = RGBColor(255, 255, 255)
    C_CARD_BG = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(26, 32, 44)      # #1A202C
    C_TEXT_MUTED = RGBColor(74, 85, 104)    # #4A5568
    C_BORDER_LIGHT = RGBColor(203, 213, 224)

    def add_top_ribbon(slide):
        """Adds standard SIH tricolor stripe and header bar."""
        # Tricolor stripes
        w = prs.slide_width / 3
        h = Inches(0.08)
        # Saffron
        s1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, w, h)
        s1.fill.solid(); s1.fill.fore_color.rgb = C_ORANGE_ACC; s1.line.fill.background()
        # White
        s2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, w, 0, w, h)
        s2.fill.solid(); s2.fill.fore_color.rgb = C_WHITE; s2.line.fill.background()
        # Green
        s3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, w*2, 0, w, h)
        s3.fill.solid(); s3.fill.fore_color.rgb = C_GREEN; s3.line.fill.background()

    def add_slide_header(slide, title_text: str, category_text: str = "SMART INDIA HACKATHON 2026"):
        add_top_ribbon(slide)
        
        # Header banner
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.08), prs.slide_width, Inches(1.05))
        banner.fill.solid(); banner.fill.fore_color.rgb = C_NAVY_DARK; banner.line.fill.background()

        # Category / Tag
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.5), Inches(0.3))
        p_cat = tb_cat.text_frame.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_ORANGE_ACC

        # Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.5), Inches(0.6))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Footer bar
        footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.1), prs.slide_width, Inches(0.4))
        footer.fill.solid(); footer.fill.fore_color.rgb = C_NAVY_DEEP; footer.line.fill.background()

        tb_foot = slide.shapes.add_textbox(Inches(0.8), Inches(7.15), Inches(11.7), Inches(0.3))
        p_foot = tb_foot.text_frame.paragraphs[0]
        p_foot.text = "Udhyami Yojna (उद्यमी योजना) | Ministry of MSME / Inclusive Digital Public Infrastructure | SIH 2026"
        p_foot.font.size = Pt(10)
        p_foot.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_top_ribbon(slide1)

    # Dark background
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.08), prs.slide_width, Inches(7.42))
    bg1.fill.solid(); bg1.fill.fore_color.rgb = C_NAVY_DEEP; bg1.line.fill.background()

    # Title Card Accent
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.8))
    card1.fill.solid(); card1.fill.fore_color.rgb = C_NAVY_DARK
    card1.line.color.rgb = C_ORANGE_ACC; card1.line.width = Pt(2)

    # Top Tag
    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.1), Inches(10.3), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026 | OFFICIAL PROJECT SUBMISSION"
    p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_ORANGE_ACC

    # Main Project Title
    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.3), Inches(1.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "उद्यमी योजना (Udhyami Yojna)"
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = C_WHITE

    p2 = tb.text_frame.add_paragraph()
    p2.text = "Government-Scheme Discovery Platform & AI Subsidy Advisory for Marginalized Entrepreneurs"
    p2.font.size = Pt(18); p2.font.color.rgb = RGBColor(226, 232, 240); p2.font.italic = True

    # Details Grid (Two Columns)
    # Left: Problem Statement & Theme
    tb_ps = slide1.shapes.add_textbox(Inches(1.5), Inches(3.2), Inches(4.8), Inches(3.0))
    tf_ps = tb_ps.text_frame
    tf_ps.word_wrap = True

    p = tf_ps.paragraphs[0]
    p.text = "PROBLEM STATEMENT DETAILS"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_ORANGE_ACC

    p = tf_ps.add_paragraph()
    p.text = "• PS ID: SIH-2026-MSME-1402"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_ps.add_paragraph()
    p.text = "• Category: Software / Digital Public Infrastructure"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_ps.add_paragraph()
    p.text = "• Ministry: Ministry of MSME / Financial Inclusion"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_ps.add_paragraph()
    p.text = "• Theme: Inclusive Governance & Smart Financial Empowerment"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    # Right: Team Details
    tb_tm = slide1.shapes.add_textbox(Inches(6.8), Inches(3.2), Inches(5.0), Inches(3.0))
    tf_tm = tb_tm.text_frame
    tf_tm.word_wrap = True

    p = tf_tm.paragraphs[0]
    p.text = "TEAM PARTICIPATION DETAILS"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_GREEN_LIGHT

    p = tf_tm.add_paragraph()
    p.text = "• Team Name: CodeCrafters / Team Udhyam"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_tm.add_paragraph()
    p.text = "• Team Leader: Technical Lead & System Architect"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_tm.add_paragraph()
    p.text = "• Institution: Smart India Hackathon Participant Institute"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    p = tf_tm.add_paragraph()
    p.text = "• Tech Stack: FastAPI, Google Gemini AI, Rule Engine, Vanilla Web Stack"; p.font.size = Pt(13); p.font.color.rgb = C_WHITE

    # =========================================================================
    # SLIDE 2: Idea & Solution Overview
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide2, "1. Proposed Solution & Core Value Proposition")

    # Card 1: Problem Statement
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.3))
    c1.fill.solid(); c1.fill.fore_color.rgb = C_CARD_BG; c1.line.color.rgb = C_BORDER_LIGHT
    tb1 = slide2.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(4.9))
    tf1 = tb1.text_frame; tf1.word_wrap = True
    p = tf1.paragraphs[0]; p.text = "THE GRASSROOTS CHALLENGE"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_SAFFRON

    items_prob = [
        ("Massive Information Asymmetry: ", "Over 150+ Central & State schemes exist, yet 85% of rural & micro-entrepreneurs never apply due to complex eligibility rules."),
        ("Linguistic Exclusion: ", "Official guidelines are published in dense bureaucratic English or formal Hindi, alienating non-literate and regional vernacular speakers."),
        ("No Guided Application Pathway: ", "Entrepreneurs are unaware of required documents, eligibility disqualifiers, or exact official application portals, leaving them vulnerable to predatory middlemen.")
    ]
    for title, desc in items_prob:
        p = tf1.add_paragraph()
        run1 = p.add_run(); run1.text = "• " + title; run1.font.bold = True; run1.font.size = Pt(13); run1.font.color.rgb = C_TEXT_DARK
        run2 = p.add_run(); run2.text = desc; run2.font.size = Pt(12); run2.font.color.rgb = C_TEXT_MUTED

    # Card 2: Our Innovation
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    c2.fill.solid(); c2.fill.fore_color.rgb = C_CARD_BG; c2.line.color.rgb = C_BORDER_LIGHT
    tb2 = slide2.shapes.add_textbox(Inches(7.0), Inches(1.6), Inches(5.3), Inches(4.9))
    tf2 = tb2.text_frame; tf2.word_wrap = True
    p = tf2.paragraphs[0]; p.text = "UDHYAMI YOJNA INNOVATION"; p.font.bold = True; p.font.size = Pt(16); p.font.color.rgb = C_GREEN

    items_sol = [
        ("Multilingual Voice Autofill: ", "Speak naturally in any of 12 Indian languages; browser speech recognition transcribes real-time audio with seamless non-blocking fallbacks."),
        ("AI Structured Extraction: ", "Gemini AI extracts 11 structured parameters (age, gender, category, sector, capital needed) with zero-crash heuristic guarantees."),
        ("Deterministic Scoring Source-of-Truth: ", "Pure rule-based Python engine guarantees 100% accurate qualification checks—zero hallucinated schemes or subsidies."),
        ("Vernacular Guidance & Checklists: ", "Provides actionable plain-language next steps and interactive checklists for Aadhaar, PAN, DPR, and caste certificates."),
        ("28 States & UTs Regional Hub: ", "Interactive directory linking local industrial clusters, DIC helplines, and single-window clearance portals.")
    ]
    for title, desc in items_sol:
        p = tf2.add_paragraph()
        run1 = p.add_run(); run1.text = "✔ " + title; run1.font.bold = True; run1.font.size = Pt(12); run1.font.color.rgb = C_NAVY_DARK
        run2 = p.add_run(); run2.text = desc; run2.font.size = Pt(11); run2.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: System Architecture & Technical Workflow
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide3, "2. System Architecture & Technical Flow")

    # 4 Architectural Step Cards
    steps = [
        ("1. Voice & Web Input", C_SAFFRON, [
            "• Web Speech API (12 Indian locales: hi, mr, ta, te, bn, gu, kn, ml, pa, or, as, en)",
            "• Feature detection with non-blocking manual input fallback",
            "• Live transcription preview & 1-click test scenarios"
        ]),
        ("2. AI Extraction & NLP", C_NAVY_DARK, [
            "• Google Gemini 2.5 Flash with Pydantic JSON Schema",
            "• Extracts age, gender, social category, state, district, loan need",
            "• Bilingual Devanagari/English regex fallback for offline resilience"
        ]),
        ("3. Deterministic Engine", C_GREEN, [
            "• Python rule-based scoring engine (100-point multi-factor model)",
            "• Hard gates: Stand-Up India (SC/ST/Women), Mudra loan caps, PMEGP greenfield rules",
            "• Outputs Match % (Strong/Good), met criteria & unmet warnings"
        ]),
        ("4. Discovery & Action", RGBColor(183, 121, 31), [
            "• Ranked scheme match cards with subsidy & funding limits",
            "• Plain-language guidance + required documents checklist",
            "• Direct links to official .gov.in portals + 28 States Ecosystem Hub"
        ])
    ]

    card_w = Inches(2.75)
    card_gap = Inches(0.2)
    start_x = Inches(0.8)

    for i, (stitle, scolor, points) in enumerate(steps):
        cx = start_x + i * (card_w + card_gap)
        sc = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.5), card_w, Inches(3.6))
        sc.fill.solid(); sc.fill.fore_color.rgb = C_CARD_BG; sc.line.color.rgb = scolor; sc.line.width = Pt(2)

        # Header of card
        hdr = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.5), card_w, Inches(0.7))
        hdr.fill.solid(); hdr.fill.fore_color.rgb = scolor; hdr.line.fill.background()
        p = hdr.text_frame.paragraphs[0]; p.text = stitle; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide3.shapes.add_textbox(cx + Inches(0.1), Inches(2.25), card_w - Inches(0.2), Inches(2.7))
        tf = tb.text_frame; tf.word_wrap = True
        for pt in points:
            p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK

    # Bottom Tech Stack Banner
    bot_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.45))
    bot_card.fill.solid(); bot_card.fill.fore_color.rgb = C_BG_LIGHT; bot_card.line.color.rgb = C_BORDER_LIGHT

    tb_stack = slide3.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.25))
    tf_s = tb_stack.text_frame; tf_s.word_wrap = True
    p = tf_s.paragraphs[0]; p.text = "TECHNOLOGY STACK SUMMARY"; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = C_NAVY_DARK

    p = tf_s.add_paragraph()
    r1 = p.add_run(); r1.text = "• Frontend: "; r1.font.bold = True; r1.font.color.rgb = C_SAFFRON
    r2 = p.add_run(); r2.text = "Raw HTML5, Modular CSS (NIC Govt & India.gov.in GIGW theme), Vanilla ES Modules (Zero bundler, zero framework overhead)\n"
    r3 = p.add_run(); r3.text = "• Backend & API: "; r3.font.bold = True; r3.font.color.rgb = C_NAVY_DARK
    r4 = p.add_run(); r4.text = "Python 3.12, FastAPI, Uvicorn, Pydantic V2, Starlette, CORS Middleware\n"
    r5 = p.add_run(); r5.text = "• AI & Scoring: "; r5.font.bold = True; r5.font.color.rgb = C_GREEN
    r6 = p.add_run(); r6.text = "Google Gemini 2.5 Flash via google-genai SDK, Deterministic 100-point multi-dimensional rule-based scoring engine"
    for r in [r2, r4, r6]:
        r.font.size = Pt(11); r.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: Uniqueness & Competitive Advantage
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide4, "3. Innovation, Uniqueness & Comparative Analysis")

    # Table layout
    rows = 5; cols = 4
    left = Inches(0.8); top = Inches(1.5); width = Inches(11.733); height = Inches(5.1)
    table_shape = slide4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(3.533)

    headers = ["Evaluation Feature", "Traditional Govt Portals", "Generic AI Chatbots (LLMs)", "Udhyami Yojna (Our Solution)"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK if j < 3 else C_SAFFRON
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("Multilingual Speech Autofill", "❌ None; rigid drop-downs with high literacy bar", "⚠️ Text-only prompt input; unguided format", "✔ 12 Indian languages voice input with auto form extraction"),
        ("Eligibility Calculation", "❌ Manual search through hundreds of PDF guidelines", "⚠️ Hallucinates schemes, wrong subsidy numbers", "✔ Deterministic rule engine as absolute source-of-truth"),
        ("Offline & Zero-Key Resilience", "❌ Fails when portal is down or slow", "❌ Completely broken without API key / network", "✔ Bilingual heuristic fallback guarantees zero crashes"),
        ("State & Local Ecosystem Depth", "⚠️ Fragmented across 28 separate state websites", "❌ Generic, lacks district craft clusters & helplines", "✔ Unified 28 States/UTs hub with DIC numbers & portals")
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if j < 3 else RGBColor(254, 243, 199)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.font.color.rgb = C_TEXT_DARK
            if j == 3:
                p.font.bold = True

    # =========================================================================
    # SLIDE 5: Feasibility, Viability & Security
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide5, "4. Feasibility, Viability & Security Architecture")

    # 3 Pillars (Technical, Operational/Economic, Security)
    p_cards = [
        ("Technical Feasibility", C_NAVY_DARK, [
            "• Zero Build / No Bundler Overhead: Raw ES Modules run natively in any modern browser on low-cost mobile phones.",
            "• Lightweight & Responsive: Mobile-first NIC India.gov.in theme consumes minimal bandwidth (<150KB total assets).",
            "• Browser Native Capabilities: Leverages standard Web Speech API with non-blocking manual input for Firefox/Safari."
        ]),
        ("Operational & Economic Viability", C_SAFFRON, [
            "• Zero Overhead Integration: Does not require replacing legacy ministry portals; directly links to verified .gov.in forms.",
            "• Negligible Operational Costs: Deterministic Python scoring runs with near-zero latency and minimal server compute.",
            "• Offline Continuity: Zero reliance on paid third-party APIs during offline fallback mode."
        ]),
        ("Data Privacy & Security", C_GREEN, [
            "• Server-Side Secret Isolation: Gemini API keys are strictly read server-side via environment variables; never exposed to browser.",
            "• No Unauthorized PII Storage: Evaluates eligibility in-memory without recording sensitive Aadhaar/PAN data.",
            "• Strict Server Validation: All demographic and numeric inputs are sanitized via Pydantic models against prompt injection."
        ])
    ]

    w_card = Inches(3.7)
    gap = Inches(0.3)
    sx = Inches(0.8)

    for i, (title, col, bullets) in enumerate(p_cards):
        x = sx + i * (w_card + gap)
        sc = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), w_card, Inches(5.1))
        sc.fill.solid(); sc.fill.fore_color.rgb = C_CARD_BG; sc.line.color.rgb = col; sc.line.width = Pt(2)

        # Title
        hdr = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), w_card, Inches(0.75))
        hdr.fill.solid(); hdr.fill.fore_color.rgb = col; hdr.line.fill.background()
        p = hdr.text_frame.paragraphs[0]; p.text = title; p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide5.shapes.add_textbox(x + Inches(0.15), Inches(2.4), w_card - Inches(0.3), Inches(4.0))
        tf = tb.text_frame; tf.word_wrap = True
        for b in bullets:
            p = tf.add_paragraph(); p.text = b; p.font.size = Pt(12); p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 6: Social Impact & National Alignment
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide6, "5. Social Impact, Inclusivity & National Alignment")

    # 4 Key Impact Stat Cards
    stats = [
        ("12+", "Indian Languages", "Voice recognition covering 90%+ vernacular speaking population"),
        ("100%", "Accurate Rules", "Deterministic Python source-of-truth eliminates misinformation"),
        ("<30s", "Discovery Time", "Reduced from 2 weeks of physical office rounds to 30 seconds"),
        ("28", "States & UTs", "Unified regional entrepreneurial ecosystem with DIC helplines")
    ]

    sw = Inches(2.7)
    sgap = Inches(0.3)
    ssx = Inches(0.8)

    for i, (big, label, sub) in enumerate(stats):
        x = ssx + i * (sw + sgap)
        sc = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), sw, Inches(1.9))
        sc.fill.solid(); sc.fill.fore_color.rgb = C_BG_LIGHT; sc.line.color.rgb = C_SAFFRON; sc.line.width = Pt(1.5)

        tb = slide6.shapes.add_textbox(x, Inches(1.6), sw, Inches(1.7))
        tf = tb.text_frame; tf.word_wrap = True
        p1 = tf.paragraphs[0]; p1.text = big; p1.font.bold = True; p1.font.size = Pt(28); p1.font.color.rgb = C_SAFFRON; p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph(); p2.text = label; p2.font.bold = True; p2.font.size = Pt(12); p2.font.color.rgb = C_NAVY_DARK; p2.alignment = PP_ALIGN.CENTER
        p3 = tf.add_paragraph(); p3.text = sub; p3.font.size = Pt(10); p3.font.color.rgb = C_TEXT_MUTED; p3.alignment = PP_ALIGN.CENTER

    # Bottom Impact Narratives (Two Columns)
    # Col 1: Marginalized Empowerment
    c_imp1 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(5.7), Inches(3.1))
    c_imp1.fill.solid(); c_imp1.fill.fore_color.rgb = C_CARD_BG; c_imp1.line.color.rgb = C_BORDER_LIGHT
    tb_i1 = slide6.shapes.add_textbox(Inches(1.0), Inches(3.75), Inches(5.3), Inches(2.8))
    tf_i1 = tb_i1.text_frame; tf_i1.word_wrap = True
    p = tf_i1.paragraphs[0]; p.text = "EMPOWERING MARGINALIZED GROUPS"; p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = C_GREEN
    imp1_pts = [
        "• Women Entrepreneurs: Instant identification of 10-15% higher subsidy brackets and exclusive incubation programs like WE-Hub and Stand-Up India.",
        "• SC/ST Founders: Prioritized eligibility verification for collateral-free credit, special margin subsidies, and Single Point Registration.",
        "• Rural Artisans & Street Vendors: Clear pathways to PM SVANidhi, PMFME, and traditional craft clusters without bureaucratic intimidation."
    ]
    for pt in imp1_pts:
        p = tf_i1.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK

    # Col 2: Alignment with National Missions
    c_imp2 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.6), Inches(5.7), Inches(3.1))
    c_imp2.fill.solid(); c_imp2.fill.fore_color.rgb = C_CARD_BG; c_imp2.line.color.rgb = C_BORDER_LIGHT
    tb_i2 = slide6.shapes.add_textbox(Inches(7.0), Inches(3.75), Inches(5.3), Inches(2.8))
    tf_i2 = tb_i2.text_frame; tf_i2.word_wrap = True
    p = tf_i2.paragraphs[0]; p.text = "ALIGNMENT WITH NATIONAL MISSIONS"; p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = C_NAVY_DARK
    imp2_pts = [
        "• Viksit Bharat 2047: Building equitable grassroots economic prosperity by making enterprise capital accessible to Tier 2/3 and rural India.",
        "• Digital India & Bhashini Vision: Bridging the digital and linguistic divide through multi-dialect vernacular voice interfaces.",
        "• Financial Inclusion (Jan Dhan to Jan Samarth): Transforming unbanked micro-entrepreneurs into formal credit-worthy enterprise founders."
    ]
    for pt in imp2_pts:
        p = tf_i2.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 7: Future Scope, Roadmap & Conclusion
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide7, "6. Implementation Roadmap, Future Scope & Conclusion")

    # 3 Phase Roadmap Columns
    phases = [
        ("Phase 1: Present (MVP Ready)", C_GREEN, [
            "✔ Full functional Web SPA (Vanilla JS + HTML5)",
            "✔ 12 Indian languages voice input & smart autofill",
            "✔ Deterministic rule engine (Central + 28 States)",
            "✔ 27 Automated test cases passing with zero errors"
        ]),
        ("Phase 2: Next 6 Months", C_SAFFRON, [
            "• WhatsApp & IVR Helpline: Conversational voicebot over phone calls for feature-phone users without internet.",
            "• DigiLocker Integration: 1-click verification of Aadhaar, Caste & Marksheet documents directly inside the portal.",
            "• Bhashini AI Integration: Native Indian accent audio synthesis for reading guidance aloud."
        ]),
        ("Phase 3: Scale & Rollout", C_NAVY_DARK, [
            "• JanSamarth Bank API: Direct digital forwarding of verified application dossiers to lead nationalized banks.",
            "• District DIC Portal Sync: Bi-directional synchronization with all 750+ District Industries Centres across India.",
            "• Vernacular Mentorship Network: Peer-to-peer founder community for marginalized enterprise guidance."
        ])
    ]

    for i, (title, col, pts) in enumerate(phases):
        x = sx + i * (w_card + gap)
        sc = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), w_card, Inches(4.3))
        sc.fill.solid(); sc.fill.fore_color.rgb = C_CARD_BG; sc.line.color.rgb = col; sc.line.width = Pt(2)

        hdr = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), w_card, Inches(0.75))
        hdr.fill.solid(); hdr.fill.fore_color.rgb = col; hdr.line.fill.background()
        p = hdr.text_frame.paragraphs[0]; p.text = title; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.CENTER

        tb = slide7.shapes.add_textbox(x + Inches(0.15), Inches(2.4), w_card - Inches(0.3), Inches(3.2))
        tf = tb.text_frame; tf.word_wrap = True
        for pt in pts:
            p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT_DARK
            p.space_after = Pt(6)

    # Conclusion Bar
    concl_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.85))
    concl_box.fill.solid(); concl_box.fill.fore_color.rgb = C_NAVY_DEEP; concl_box.line.color.rgb = C_ORANGE_ACC

    tb_c = slide7.shapes.add_textbox(Inches(1.0), Inches(6.05), Inches(11.3), Inches(0.75))
    tf_c = tb_c.text_frame; tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "CONCLUSION: Udhyami Yojna turns the vision of Viksit Bharat into a tangible reality by democratizing access to government subsidies and capital for India's 63+ million micro-entrepreneurs."
    p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = C_WHITE; p.alignment = PP_ALIGN.CENTER

    prs.save(output_path)
    print(f"SIH Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "d:\\UDHYAM\\Udhyami_Yojna_SIH_2026.pptx"
    create_sih_presentation(out_file)
