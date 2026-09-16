# Udhyami Yojna (उद्यमी योजना) — System Flowcharts & Architecture

This document provides the complete flowchart architecture for **Udhyami Yojna**, designed for the **Smart India Hackathon (SIH 2026)**. It illustrates the user journey, AI extraction pipeline, deterministic scoring engine, and backend data flow.

---

## 1. High-Level End-to-End System Flowchart

This diagram traces the entire journey from the entrepreneur speaking in their native language to receiving personalized government subsidies and official application links.

```mermaid
flowchart TD
    %% Styling
    classDef userNode fill:#FFF3E0,stroke:#D84315,stroke-width:2px,color:#1A202C;
    classDef clientNode fill:#E3F2FD,stroke:#0B3C5D,stroke-width:2px,color:#1A202C;
    classDef aiNode fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px,color:#1A202C;
    classDef engineNode fill:#E8F5E9,stroke:#1B5E20,stroke-width:2px,color:#1A202C;
    classDef dataNode fill:#ECEFF1,stroke:#374151,stroke-width:2px,color:#1A202C;
    classDef outNode fill:#FFF9C4,stroke:#F57F17,stroke-width:2px,color:#1A202C;

    %% Nodes
    A["👤 Rural / Marginalized Entrepreneur\n(Women, SC/ST, Artisan, Divyangjan)"]:::userNode
    
    subgraph Frontend ["Client-Side Browser (Raw HTML5 + ES Modules)"]
        B["🎙️ Voice Input (Web Speech API)\n12 Indian Locales (hi-IN, mr-IN, ta-IN...)"]:::clientNode
        B_alt["⌨️ Manual Form Entry / Direct Search"]:::clientNode
        C["⚡ Live Audio Waveform & Speech Preview"]:::clientNode
        D["📋 Auto-Filled Entrepreneur Profile Form\n(Fuzzy Select Match + Zero-Blank Guarantee)"]:::clientNode
    end

    subgraph Backend_Gateway ["FastAPI Gateway (backend/main.py)"]
        E["POST /api/extract\n{ text: string }"]:::clientNode
        F["POST /api/match-schemes\n{ profile: EntrepreneurProfile }"]:::clientNode
        G["GET /api/states & /api/schemes"]:::clientNode
    end

    subgraph AI_Pipeline ["AI Extraction & Fallback Engine (backend/gemini_service.py)"]
        H{"Is GEMINI_API_KEY\nconfigured?"}:::aiNode
        I["Google Gemini 2.5 Flash\n(Pydantic Structured JSON Schema)"]:::aiNode
        J["🛡️ Offline Bilingual Heuristic Parser\n(Devanagari/English Regex + City Resolver)"]:::aiNode
        K["Smart Default Imputation\n(Guarantees Zero Blank Fields)"]:::aiNode
    end

    subgraph Scoring_Core ["Deterministic Rule Engine (backend/scoring_engine.py)"]
        L["Hard Eligibility Gating\n(Strict Criteria, Gender, Category, Loan Range)"]:::engineNode
        M["Deterministic 100-Point Scorer\n• Demographic Fit (30 pts)\n• Financial Fit (25 pts)\n• Sector Fit (20 pts)\n• Regional Fit (15 pts)\n• Subsidy Fit (10 pts)"]:::engineNode
        N["Dynamic Document Checklist Generator\n(Mandatory Aadhaar, Caste, Udyam, DPR...)"]:::engineNode
    end

    subgraph Data_Storage ["Static & Dynamic Data Store (JSON)"]
        O[("Central & State Schemes\n(schemes.json - 21 Schemes)")]:::dataNode
        P[("28 States & UTs Hub\n(states.json - Ecosystem & DIC)")]:::dataNode
    end

    subgraph User_Action ["Actionable Output Layer"]
        Q["🏆 Ranked Scheme Cards\n(Match Score % + Subsidy Highlight)"]:::outNode
        R["📑 Interactive Document Checklist\n(Printable PDF / Verification Status)"]:::outNode
        S["🔗 Direct Government Portal Links\n(PMEGP, JanSamarth, Mudra, StandUp India)"]:::outNode
        T["🏛️ State DIC & Industrial Cluster Contacts"]:::outNode
    end

    %% Flow Connections
    A -->|Speaks into Mic| B
    A -->|Types details| B_alt
    B --> C
    B_alt --> D
    C -->|Transcript Sent| E
    
    E --> H
    H -->|Yes & Online| I
    H -->|No / Timeout / Offline| J
    I -->|Parsed Entities| K
    J -->|Extracted Profile| K
    K -->|Profile JSON| D
    
    D -->|User verifies & clicks Match| F
    F --> L
    O --> L
    L -->|Eligible Candidates| M
    M --> N
    N --> Q
    N --> R
    N --> S
    
    A -->|Explores State Hub| G
    P --> G
    G --> T

```

---

## 2. Detailed Voice-to-Form Auto-Fill Pipeline

This flowchart illustrates how unstructured native speech (e.g. Hindi *"मुझे बेकरी की दुकान के लिए 5 लाख का लोन चाहिए"*) is converted into fully structured profile parameters without any blank fields.

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Entrepreneur
    participant Mic as 🎙️ Browser Web Speech API
    participant UI as 🖥️ Vanilla JS Frontend (render.js)
    participant API as 🚀 FastAPI (/api/extract)
    participant Gemini as 🤖 Gemini 2.5 Flash
    participant Fallback as 🛡️ Regex Heuristic Parser
    participant Resolver as 📍 Indian City/District DB

    User->>Mic: Clicks mic & speaks in native tongue (e.g., Hindi)
    Mic->>UI: Real-time transcript stream (interim & final results)
    UI->>UI: Update visual waveform pulse & transcript display
    UI->>API: HTTP POST /api/extract { text: "..." }
    
    alt Gemini API Key Available & Service Up
        API->>Gemini: generateContent with ProfileSchema (Pydantic)
        Gemini-->>API: Structured JSON (category, state, loan, sector)
    else Offline Mode / API Quota Exceeded / Fallback
        API->>Fallback: Run Bilingual Regex (Devanagari & English)
        Fallback->>Resolver: Match Indian city/district (e.g., "Kalyan" -> "Thane, Maharashtra")
        Resolver-->>Fallback: Resolved State & District
        Fallback->>Fallback: Impute smart defaults (Age: 30, Edu: 10th Pass)
        Fallback-->>API: Complete Structured Profile
    end

    API-->>UI: 200 OK: ExtractedProfile JSON (zero nulls)
    UI->>UI: populateProfileForm() executes
    UI->>UI: Fuzzy-matches <select> options with aliases
    UI->>UI: Triggers .auto-filled-highlight CSS flash
    UI-->>User: Form populated with 100% complete values ready to match
```

---

## 3. Deterministic 100-Point Scoring Rule Engine Flowchart

Unlike non-deterministic LLM chatbots that can hallucinate scheme qualification, Udhyami Yojna executes a mathematically verifiable 100-point scoring algorithm.

```mermaid
flowchart TD
    Start(["Input: User Profile + Scheme Catalog (21 Schemes)"]) --> Loop["For Each Scheme in Catalog"]
    
    subgraph Hard_Gate ["Stage 1: Hard Eligibility Gating (Pass / Fail)"]
        Loop --> G1{"Loan Amount within\n[min_loan, max_loan]?"}
        G1 -- No --> Reject["Disqualified: Score = 0%\n(Loan out of scope)"]
        G1 -- Yes --> G2{"Age within\n[min_age, max_age]?"}
        G2 -- No --> Reject2["Disqualified: Score = 0%\n(Age limit exceeded)"]
        G2 -- Yes --> G3{"Target Category Allowed?\n(All, Women, SC, ST, OBC, Divyangjan)"}
        G3 -- No --> Reject3["Disqualified: Score = 0%\n(Quota restriction)"]
        G3 -- Yes --> G4{"State Matches?\n('All India' OR user.state == scheme.state)"}
        G4 -- No --> Reject4["Disqualified: Score = 0%\n(State specific mismatch)"]
    end

    subgraph Soft_Scoring ["Stage 2: Deterministic 100-Point Score Accumulator"]
        G4 -- Yes (Eligible) --> S1["Base Eligibility Points: +30 pts"]
        
        S1 --> S2{"Demographic Fit\n(Target group priority)"}
        S2 -- Exact Match --> P2["+20 pts"]
        S2 -- General Match --> P2_alt["+10 pts"]
        
        P2 & P2_alt --> S3{"Financial Fit\n(Loan & Capital alignment)"}
        S3 -- Optimal Range --> P3["+20 pts"]
        S3 -- Sub-optimal --> P3_alt["+10 pts"]
        
        P3 & P3_alt --> S4{"Sector Alignment\n(Manufacturing, Services, Trading, Agri)"}
        S4 -- Target Sector --> P4["+15 pts"]
        S4 -- Allied Sector --> P4_alt["+5 pts"]

        P4 & P4_alt --> S5{"Regional Subsidies\n(Rural vs Urban location factor)"}
        S5 -- Special Category / Rural Area --> P5["+15 pts (Max 35% subsidy tier)"]
        S5 -- General Urban --> P5_alt["+5 pts (25% subsidy tier)"]
    end

    subgraph Output_Ranking ["Stage 3: Normalization & Tiering"]
        P5 & P5_alt --> Tot["Sum Score (0 to 100 Points)"]
        Tot --> Tier{"Score Level"}
        Tier -- ">= 80" --> High["🟢 Exceptional Match (High Priority)"]
        Tier -- "60 - 79" --> Med["🟡 Good Match (Recommended)"]
        Tier -- "< 60" --> Low["⚪ Potential Match (Alternative)"]
    end

    High & Med & Low --> Sort["Sort descending by Score"]
    Sort --> Finish(["Output Ranked Schemes + Dynamic Document Checklist"])
```

---

## 4. State-Wise Discovery Hub Architecture

```mermaid
graph LR
    subgraph UI_Layer ["State Hub Frontend (state-hub.js)"]
        A["🏛️ Interactive State Selector\n(28 States & UTs Dropdown)"]
        B["📍 Sector Filter Buttons\n(All, Handloom, Food Processing, IT, Auto)"]
        C["🔍 Keyword Search Box\n(Cluster, District, Scheme Name)"]
    end

    subgraph API_Layer ["Backend Route (/api/states)"]
        D["FastAPI State Router\n(backend/routers/schemes.py)"]
        E[("states.json Database")]
    end

    subgraph Render_Layer ["Dynamic UI Cards"]
        F["📊 State Macro Overview\n(Capital, Target Sectors, Policy Name)"]
        G["🏭 Key Industrial Clusters & Districts\n(e.g., Surat Textiles, Morbi Ceramics)"]
        H["📜 State Exclusive Schemes\n(e.g., Mukhyamantri Udyami Yojna)"]
        I["🏢 District Industries Centre (DIC)\n(Office Address, Helpline, Nodal Email)"]
    end

    A & B & C --> D
    D --> E
    E --> D
    D --> F & G & H & I
```

---

## 5. Security & Privacy Architecture (Zero PII Retention)

```mermaid
flowchart TD
    subgraph User_Space ["Client Device (Local Browser)"]
        A["Entrepreneur enters info / speaks"]
        B["Browser Voice Buffer (Volatile RAM)"]
    end

    subgraph Network ["HTTPS / TLS 1.3 Transport"]
        C["Encrypted JSON Payload\n(No Aadhaar number, No PAN card)"]
    end

    subgraph Server_Space ["Stateless Application Tier (FastAPI)"]
        D["Volatile Memory Processing Only\n(Profiles parsed in-memory)"]
        E["Deterministic Rule Evaluation"]
        F["Immediate Garbage Collection"]
        G["🚫 NO Database of User Identity"]
        H["🛡️ Zero PII Logging Policy"]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    D -.-> G
    D -.-> H
```

---

## 6. Component Interaction Matrix

| Module | File Path | Role | Key Functions / Methods |
| :--- | :--- | :--- | :--- |
| **Voice Engine** | `static/js/voice.js` | Browser audio capture | `startListening()`, `switchLocale()`, `showBrowserWarning()` |
| **API Client** | `static/js/api.js` | REST client | `extractVoiceProfile()`, `matchSchemes()`, `getStates()` |
| **DOM Renderer** | `static/js/render.js` | Form fill & UI display | `populateProfileForm()`, `renderSchemes()`, `renderDocumentChecklist()` |
| **State Hub** | `static/js/state-hub.js` | 28 States catalog | `renderStateDetail()`, `filterBySector()`, `filterBySearch()` |
| **App Coordinator** | `static/js/app.js` | Master event wiring | `initTabs()`, `bindVoiceEvents()`, `bindFormEvents()` |
| **FastAPI App** | `backend/main.py` | Static & API router | `/api/extract`, `/api/match-schemes`, `/presentation`, `/download/presentation` |
| **AI Service** | `backend/gemini_service.py` | Entity extraction | `extract_profile_from_text()`, fallback regex, city resolver |
| **Rule Engine** | `backend/scoring_engine.py` | 100-pt determinism | `score_scheme_eligibility()`, `filter_and_rank_schemes()` |

---
*Generated for Smart India Hackathon (SIH 2026) | Udhyami Yojna Technical Documentation*
