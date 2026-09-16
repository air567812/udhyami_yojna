# 🇮🇳 Udhyami Yojna (उद्यमी योजना)

**Government Scheme Discovery & AI Subsidy Advisory Platform for Marginalized Indian Entrepreneurs**

Udhyami Yojna is a digital public infrastructure platform purpose-built for marginalized and aspiring Indian entrepreneurs—including Women, Scheduled Castes (SC), Scheduled Tribes (ST), Other Backward Classes (OBC), Divyangjan (Differently-Abled), rural artisans, and small business owners. It bridges the critical information gap between complex government gazette guidelines and grassroots enterprise founders by combining **multilingual voice input**, **Google Gemini AI structured extraction**, and **deterministic rule-based eligibility scoring**.

---

## 🏛️ Architecture Overview

```
                               Browser Client (SPA)
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  HTML5 + Native Modular CSS (NIC Govt Theme) + Vanilla ES Modules           │
  │  - Web Speech API (12 Indian Locales) with Non-Blocking Manual Fallback    │
  │  - Structured Profile Review & Form Editor                                  │
  │  - Ranked Scheme Match Cards with Criteria Breakdown & Document Checklists  │
  │  - State-wise Entrepreneurial Discovery Hub (28 States & UTs)               │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ HTTP REST (JSON)
                                         ▼
                             FastAPI Backend (Python 3.12)
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │  - Static Asset Delivery (Serves / and /static/*)                            │
  │  - POST /api/extract        (Gemini AI with Heuristic Fallback)             │
  │  - POST /api/match-schemes  (Rule-Based Eligibility Engine + Gemini Advice) │
  │  - GET  /api/schemes        (Filterable Catalog of Central & State Schemes) │
  │  - GET  /api/states         (State Ecosystems, Clusters & Helplines)        │
  │  - GET  /api/health         (System Health & Model Status)                  │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │  Deterministic Scoring Engine (Source of Truth):                            │
  │  - Hard eligibility gates (Age, State, Gender, Social Category, Greenfield) │
  │  - Weighted multi-factor scoring (0 - 100 points)                           │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │  Google Gemini Service (Official google-genai SDK):                         │
  │  - Structured Output via JSON Schema (`UserProfile`)                        │
  │  - Plain-language personalized guidance for top matched schemes             │
  │  - Zero-crash offline fallback parser for Hindi, Hinglish, and English      │
  └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12
- Modern Web Browser (Chrome, Edge, Brave recommended for Speech Recognition; Firefox and Safari fully supported via manual input)

### 2. Clone and Setup Environment
```bash
# Navigate to repository root
cd UDHYAM

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` with your settings:
```ini
# Google Gemini API Key (Optional: system works in offline fallback mode if omitted)
GEMINI_API_KEY=your_gemini_api_key_here

# Gemini Model ID (default: gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash

# CORS Allowed Origins
ALLOWED_ORIGINS=*

# Server host and port
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 4. Run the Application
Launch the server using `uvicorn`:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Once running:
- **Web Application**: Open [http://localhost:8000](http://localhost:8000) in your browser.
- **Interactive Swagger Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs).
- **Alternative ReDoc**: Open [http://localhost:8000/redoc](http://localhost:8000/redoc).

---

## 🧪 Running Automated Tests

Run the complete test suite using `pytest`:
```bash
# Ensure virtual environment is active
pytest -v
```

All 27 test cases run deterministically and **pass without requiring a Gemini API key**:
- `tests/test_scoring.py`: Validates deterministic rule-based matching, Stand-Up India SC/ST/Women conditions, Mudra brackets (Shishu/Kishore/Tarun), age cutoffs, and state boundaries.
- `tests/test_gemini_fallback.py`: Validates the bilingual Devanagari/English heuristic parser and offline resilience.
- `tests/test_api.py`: Validates FastAPI endpoints, JSON response models, input validation, and mocked Gemini handling.

---

## 🌟 Core Features & Modules

### 1. Multilingual Voice Autofill & Accessibility
- **12 Indian Locales Supported**: Hindi (`hi-IN`), English India (`en-IN`), Marathi (`mr-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), Bengali (`bn-IN`), Gujarati (`gu-IN`), Kannada (`kn-IN`), Malayalam (`ml-IN`), Punjabi (`pa-IN`), Odia (`or-IN`), and Assamese (`as-IN`).
- **Feature Detection**: Accurately detects `SpeechRecognition` support. If running in a browser without speech support (e.g. Firefox), an informative banner is displayed and the manual form is promoted without blocking the user.
- **Pulsing Mic Visualizer**: Animated concentric rings and live status updates inform the user when the mic is actively recording.
- **Quick-Test Scenarios**: Pre-configured real-world vernacular sample prompts allow instantaneous one-click testing of complex applicant scenarios.

### 2. AI Structured Extraction with Safe Fallback
- Converts conversational speech transcripts into a validated `UserProfile` model (age, gender, income, state, district, social group, education, sector, loan needed, business stage).
- **Zero-Crash Guarantee**: If the Gemini API key is missing or an API error occurs, the built-in heuristic regex parser immediately extracts key demographic and financial parameters.

### 3. Deterministic Rule-Based Scoring Engine
- **Source of Truth**: Python rule engine executes strict eligibility checks:
  - **Stand-Up India**: Strictly validates SC, ST, or Woman applicant status.
  - **Mudra Yojana**: Dispatches between Shishu (up to ₹50k), Kishore (₹50k - ₹5L), and Tarun (₹5L - ₹20L).
  - **PMEGP / CMEGP**: Enforces greenfield enterprise requirements (existing businesses are ineligible for 1st tranche).
  - **State Alignment**: Matches local state initiatives with applicant location while keeping Central schemes accessible nationwide.
- **Explainability**: Returns explicit `why_matched` bullet points and `unmet_criteria` notifications.
- **Personalized Plain-Language Advice**: Gemini AI enriches top matches with friendly next steps and simple instructions.

### 4. State-Wise Discovery Hub
- Comprehensive directory covering **28 Indian States & UTs**.
- Detailed regional profiles featuring:
  - Key regional industrial focus sectors.
  - District-level industrial clusters & craft belts (e.g. Banarasi Silk in Varanasi, Auto Ancillaries in Pune, Cotton Knitwear in Tiruppur).
  - Official Single-Window Clearance Portal links.
  - District Industries Centre (DIC) portals and toll-free helpline numbers.
  - State-specific exclusive entrepreneurial schemes.

### 5. NIC / India.gov.in Visual Styling
- Authentic Indian Government portal aesthetic: Saffron (`#D84315`), Ashoka Navy (`#0B3C5D`), and Forest Green (`#1B5E20`) tricolor palette.
- Ashoka Chakra emblem placeholder, bilingual headers (Hindi / English), and GIGW-compliant typography.
- Mobile-first responsive layout with minimum 48px touch targets, visible focus rings, and screen-reader skip links.

---

## 📁 Repository Structure

```
UDHYAM/
├── backend/
│   ├── __init__.py
│   ├── config.py                 # Application settings and environment loading
│   ├── models.py                 # Pydantic schemas for requests, schemes, and profiles
│   ├── gemini_service.py         # Google GenAI client & bilingual heuristic fallback
│   ├── scoring_engine.py         # Deterministic rule-based scheme scoring engine
│   ├── main.py                   # FastAPI app serving static frontend & API
│   ├── routers/
│   │   ├── __init__.py
│   │   └── schemes.py            # Endpoints for extraction, matching, catalog, and states
│   └── data/
│       ├── schemes.json          # Seed catalog of Central and State government schemes
│       └── states.json           # 28 States/UTs ecosystems, clusters, and DIC portals
├── static/
│   ├── index.html                # Semantic HTML5 single-page application
│   ├── css/
│   │   ├── nic-theme.css         # India.gov.in / NIC styling, tricolor accents, accessibility
│   │   └── components.css        # Mic visualizer, scheme cards, badges, loaders
│   └── js/
│       ├── app.js                # Main frontend controller & event coordinator
│       ├── api.js                # Fetch wrapper for /api/* endpoints
│       ├── voice.js              # Web Speech API manager & feature detection
│       ├── state-hub.js          # State discovery hub manager
│       └── render.js             # DOM rendering for cards, checklists, and forms
├── tests/
│   ├── __init__.py
│   ├── test_scoring.py           # Unit tests for rule-based scoring engine
│   ├── test_api.py               # Integration tests for FastAPI endpoints
│   └── test_gemini_fallback.py   # Heuristic parser resilience tests
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore file protecting keys and caches
├── requirements.txt              # Production and test Python dependencies
└── README.md                     # Project documentation and run guide
```

---

## 📋 Manual Verification Guide

1. **Start the Server**:
   ```bash
   uvicorn backend.main:app --port 8000 --reload
   ```
2. **Access Home Page**:
   - Visit `http://localhost:8000`
   - Verify the NIC Government portal header with national emblem and tricolor ribbon.
3. **Test Voice Input / Quick Scenarios**:
   - On Chrome/Edge: click "बोलें / Speak", speak into the mic, and observe live text in the transcript box.
   - Click any of the quick-test scenario chips (e.g. "उत्तर प्रदेश - महिला सिलाई व्यवसाय").
   - Click **"⚡ Auto-Fill Form with AI"** and confirm that the 11 fields populate automatically.
4. **Test Scheme Matching**:
   - Click **"🎯 Find Eligible Schemes"**.
   - Verify that the ranked schemes appear with match percentages, subsidy highlights, "Why You Qualify" checkmarks, interactive document checklists, and official `.gov.in` application links.
5. **Test State Discovery Hub**:
   - Click on the **"🏛️ State Discovery Hub"** tab.
   - Select different states (e.g. Maharashtra, Uttar Pradesh, Tamil Nadu, Bihar, Gujarat).
   - Verify that regional industrial clusters, DIC helpline numbers, single-window links, and state schemes render dynamically.
6. **Test Scheme Catalog**:
   - Click on the **"📜 Browse All Schemes"** tab.
   - Filter by sector (e.g. "Food Processing") or search by keyword ("Mudra", "PMEGP").
