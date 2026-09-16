"""Gemini API client for structured voice extraction and plain-language scheme advice."""
import json
import logging
import re
from typing import Optional, List, Dict, Any

from backend.config import settings
from backend.models import UserProfile, ExtractionResponse, SchemeMatchResult

logger = logging.getLogger("udhyami.gemini")


class GeminiService:
    """Service interacting with Google Gemini API via the official google-genai SDK, with safe fallbacks."""

    def __init__(self):
        self._client = None
        self._init_client()

    def _init_client(self):
        """Initializes the google-genai Client if API key is provided."""
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
                logger.info("Initialized Google GenAI client successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Google GenAI client: {e}. Fallback parser will be used.")
                self._client = None
        else:
            logger.info("No GEMINI_API_KEY set. Heuristic fallback extractor active.")

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def extract_profile_from_transcript(self, transcript: str, language: str = "hi-IN") -> ExtractionResponse:
        """
        Extracts structured UserProfile fields from free-form speech transcript.
        Uses Gemini API with JSON response schema if available; otherwise falls back to regex/heuristic parser.
        Never throws unhandled exceptions.
        """
        if self._client:
            try:
                from google.genai import types

                prompt = f"""
You are an expert government enterprise counselor helping marginalized Indian entrepreneurs apply for welfare subsidies and micro-loans.
Extract the following user attributes from the user's speech transcript (which may be in Hindi, Hinglish, English, or another Indian language):

Fields to extract:
- age (integer or null, completed years)
- gender ("Male", "Female", or "Other", or null)
- annual_income (number in INR, or null)
- state (Indian State name, e.g. "Maharashtra", "Uttar Pradesh", "Bihar", "Tamil Nadu", or null)
- district (District name or city if mentioned, or null)
- social_category ("General", "OBC", "SC", "ST", "Minority", "Women", "Divyangjan", "EBC", or null)
- education ("Below 8th", "8th Pass", "10th Pass", "12th Pass", "Graduate / Diploma", "Post Graduate", or null)
- business_idea (short description of the business they want to do or run)
- sector ("Manufacturing", "Service", "Trading", "Food Processing", "Handicraft/Handloom", "Agri-allied", "Tech/IT", or null)
- investment_needed (number in INR. E.g. '5 lakh' = 500000, '50 hazaar' = 50000, '1 crore' = 10000000)
- existing_business (boolean: true if expanding an existing unit, false if starting a new greenfield enterprise)
- urban_rural ("Rural" or "Urban")

User Language: {language}
User Transcript:
\"\"\"{transcript}\"\"\"
"""
                response = self._client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_json_schema=UserProfile.model_json_schema(),
                        temperature=0.1
                    )
                )

                if response and response.text:
                    parsed_json = json.loads(response.text)
                    profile = UserProfile(**parsed_json)
                    return ExtractionResponse(
                        profile=profile,
                        confidence=0.95,
                        extractor_used="gemini",
                        notes="Successfully extracted via Google Gemini AI."
                    )
            except Exception as e:
                logger.warning(f"Gemini API structured extraction failed ({e}). Falling back to heuristic parser.")

        # Fallback to deterministic regex & keyword parser
        fallback_profile = self._heuristic_fallback_extract(transcript)
        return ExtractionResponse(
            profile=fallback_profile,
            confidence=0.75,
            extractor_used="fallback_heuristic",
            notes="Extracted via intelligent heuristic parser (Gemini offline or key omitted)."
        )

    def _heuristic_fallback_extract(self, text: str) -> UserProfile:
        """Rule-based and regex parser for Indian vernacular speech transcripts in Hindi and English."""
        t_lower = text.lower()

        # 1. Age extraction
        age = None
        age_match = re.search(r'(\b\d{1,2}\b)\s*(?:saal|sal|years?|varsh|वर्ष|साल|age)', t_lower)
        if not age_match:
            age_match = re.search(r'(?:age|umar|umra|उम्र|आयु)\s*(?:is|hai|ho|:)?\s*(\b\d{1,2}\b)', t_lower)
        if age_match:
            val = int(age_match.group(1))
            if 14 <= val <= 90:
                age = val

        # 2. Gender extraction
        gender = None
        if any(w in t_lower for w in ["mahila", "woman", "female", "aurat", "stri", "ladki", "girl", "महिला", "औरत", "स्त्री"]):
            gender = "Female"
        elif any(w in t_lower for w in ["purush", "man", "male", "aadmi", "ladka", "boy", "पुरुष", "आदमी"]):
            gender = "Male"

        # 3. Social category extraction
        social_category = None
        if re.search(r'(?:\b(sc|scheduled caste|dalit|valmiki|jatav)\b|अनुसूचित जाति|एससी)', t_lower):
            social_category = "SC"
        elif re.search(r'(?:\b(st|scheduled tribe|adivasi|tribal)\b|अनुसूचित जनजाति|एसटी)', t_lower):
            social_category = "ST"
        elif re.search(r'(?:\b(obc|other backward|pichhada)\b|पिछड़ा वर्ग|ओबीसी)', t_lower):
            social_category = "OBC"
        elif re.search(r'(?:\b(minority|muslim|christian|sikh|alpsankhyak)\b|अल्पसंख्यक)', t_lower):
            social_category = "Minority"
        elif re.search(r'(?:\b(divyang|pwd|handicap|disabled|viklang)\b|दिव्यांग)', t_lower):
            social_category = "Divyangjan"
        elif re.search(r'(?:\b(general|samanya)\b|सामान्य)', t_lower):
            social_category = "General"

        # 4. Annual Income extraction (Process FIRST so it doesn't get confused with loan need)
        annual_income = None
        cleaned_text_for_loan = t_lower
        inc_match = re.search(r'(?:income|kamai|aamdani|आय|कमाई)\s*(?:is|hai|:)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|लाख)', t_lower)
        if inc_match:
            annual_income = float(inc_match.group(1)) * 100000
            cleaned_text_for_loan = t_lower[:inc_match.start()] + t_lower[inc_match.end():]
        else:
            inc_raw = re.search(r'(?:income|kamai|aamdani|आय|कमाई)\s*(?:is|hai|:)?\s*(\d{4,8})', t_lower)
            if inc_raw:
                annual_income = float(inc_raw.group(1))
                cleaned_text_for_loan = t_lower[:inc_raw.start()] + t_lower[inc_raw.end():]

        # 5. Investment Needed extraction (in Lakhs, Crores, Thousands) from remaining text
        investment_needed = None
        # Check specific loan/capital patterns first
        loan_specific = re.search(r'(?:need|want|loan|capital|chahiye|require|जरूरत|चाहिए|ऋण)\s*(?:of|is|:)?\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(lakh|lac|लाख|crore|cr|करोड़|thousand|hazar|हजार)?', cleaned_text_for_loan)
        if loan_specific:
            val = float(loan_specific.group(1).replace(',', ''))
            unit = loan_specific.group(2) or ''
            if any(u in unit for u in ['lakh', 'lac', 'लाख']):
                investment_needed = val * 100000
            elif any(u in unit for u in ['crore', 'cr', 'करोड़']):
                investment_needed = val * 10000000
            elif any(u in unit for u in ['thousand', 'hazar', 'हजार']):
                investment_needed = val * 1000
            elif val > 1000:
                investment_needed = val

        if not investment_needed:
            # Lakhs: e.g. "5 lakh", "10.5 lakh", "5 लाख"
            lakh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lakh|lac|लाख)', cleaned_text_for_loan)
            if lakh_match:
                investment_needed = float(lakh_match.group(1)) * 100000
            else:
                # Crores
                cr_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:crore|cr|करोड़)', cleaned_text_for_loan)
                if cr_match:
                    investment_needed = float(cr_match.group(1)) * 10000000
                else:
                    # Thousands / Hazar
                    th_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:thousand|hazar|hazaar|हजार)', cleaned_text_for_loan)
                    if th_match:
                        investment_needed = float(th_match.group(1)) * 1000
                    else:
                        # Raw numbers > 1000 with currency or commas
                        raw_num = re.search(r'(?:rs\.?|inr|rupees?|₹)\s*([\d,]{4,10})', cleaned_text_for_loan)
                        if raw_num:
                            investment_needed = float(raw_num.group(1).replace(',', ''))
                        else:
                            # Standalone numbers like "20,000" or "50000"
                            num_match = re.search(r'\b(\d{1,3}(?:,\d{3})+|\d{4,8})\b', cleaned_text_for_loan)
                            if num_match:
                                investment_needed = float(num_match.group(1).replace(',', ''))

        # 6. State and District identification (Support both Devanagari and English)
        state = None
        district = None

        # City to (State, District) mapping
        city_map = {
            "mumbai": ("Maharashtra", "Mumbai"),
            "pune": ("Maharashtra", "Pune"),
            "nagpur": ("Maharashtra", "Nagpur"),
            "nashik": ("Maharashtra", "Nashik"),
            "aurangabad": ("Maharashtra", "Chhatrapati Sambhajinagar"),
            "solapur": ("Maharashtra", "Solapur"),
            "kolhapur": ("Maharashtra", "Kolhapur"),
            "lucknow": ("Uttar Pradesh", "Lucknow"),
            "kanpur": ("Uttar Pradesh", "Kanpur"),
            "varanasi": ("Uttar Pradesh", "Varanasi"),
            "agra": ("Uttar Pradesh", "Agra"),
            "gorakhpur": ("Uttar Pradesh", "Gorakhpur"),
            "meerut": ("Uttar Pradesh", "Meerut"),
            "aligarh": ("Uttar Pradesh", "Aligarh"),
            "noida": ("Uttar Pradesh", "Gautam Buddha Nagar"),
            "patna": ("Bihar", "Patna"),
            "gaya": ("Bihar", "Gaya"),
            "muzaffarpur": ("Bihar", "Muzaffarpur"),
            "bhagalpur": ("Bihar", "Bhagalpur"),
            "jaipur": ("Rajasthan", "Jaipur"),
            "jodhpur": ("Rajasthan", "Jodhpur"),
            "udaipur": ("Rajasthan", "Udaipur"),
            "kota": ("Rajasthan", "Kota"),
            "ahmedabad": ("Gujarat", "Ahmedabad"),
            "surat": ("Gujarat", "Surat"),
            "vadodara": ("Gujarat", "Vadodara"),
            "rajkot": ("Gujarat", "Rajkot"),
            "chennai": ("Tamil Nadu", "Chennai"),
            "coimbatore": ("Tamil Nadu", "Coimbatore"),
            "madurai": ("Tamil Nadu", "Madurai"),
            "salem": ("Tamil Nadu", "Salem"),
            "tiruppur": ("Tamil Nadu", "Tiruppur"),
            "bengaluru": ("Karnataka", "Bengaluru"),
            "bangalore": ("Karnataka", "Bengaluru"),
            "mysuru": ("Karnataka", "Mysuru"),
            "hubballi": ("Karnataka", "Dharwad"),
            "hyderabad": ("Telangana", "Hyderabad"),
            "warangal": ("Telangana", "Warangal"),
            "kolkata": ("West Bengal", "Kolkata"),
            "howrah": ("West Bengal", "Howrah"),
            "bhopal": ("Madhya Pradesh", "Bhopal"),
            "indore": ("Madhya Pradesh", "Indore"),
            "ludhiana": ("Punjab", "Ludhiana"),
            "amritsar": ("Punjab", "Amritsar"),
            "guwahati": ("Assam", "Kamrup"),
            "bhubaneswar": ("Odisha", "Khordha"),
            "cuttack": ("Odisha", "Cuttack"),
            "kochi": ("Kerala", "Ernakulam"),
            "thiruvananthapuram": ("Kerala", "Thiruvananthapuram"),
            "delhi": ("Delhi", "New Delhi"),
            "new delhi": ("Delhi", "New Delhi")
        }

        for city_kw, (st_name, dist_name) in city_map.items():
            if city_kw in t_lower:
                state = st_name
                district = dist_name
                break

        if not state:
            state_keywords = {
                "Maharashtra": ["maharashtra", "महाराष्ट्र"],
                "Uttar Pradesh": ["uttar pradesh", "उत्तर प्रदेश", "यूपी", "up"],
                "Tamil Nadu": ["tamil nadu", "तमिलनाडु", "तमिल नाडु", "tn"],
                "Gujarat": ["gujarat", "गुजरात"],
                "Karnataka": ["karnataka", "कर्नाटक"],
                "Bihar": ["bihar", "बिहार"],
                "Rajasthan": ["rajasthan", "राजस्थान"],
                "West Bengal": ["west bengal", "पश्चिम बंगाल", "bengal"],
                "Telangana": ["telangana", "तेलंगाना"],
                "Assam": ["assam", "असम"],
                "Odisha": ["odisha", "orissa", "ओडिशा"],
                "Kerala": ["kerala", "केरल"],
                "Madhya Pradesh": ["madhya pradesh", "मध्य प्रदेश", "mp"],
                "Punjab": ["punjab", "पंजाब"],
                "Andhra Pradesh": ["andhra pradesh", "आंध्र प्रदेश"],
                "Delhi": ["delhi", "दिल्ली", "ncr"],
                "Haryana": ["haryana", "हरियाणा"],
                "Jharkhand": ["jharkhand", "झारखंड"],
                "Chhattisgarh": ["chhattisgarh", "छत्तीसगढ़"],
                "Uttarakhand": ["uttarakhand", "उत्तराखंड"],
                "Himachal Pradesh": ["himachal pradesh", "हिमाचल प्रदेश"]
            }
            for st_name, kw_list in state_keywords.items():
                if any(kw in t_lower for kw in kw_list):
                    state = st_name
                    break

        # 7. Sector & Business Idea
        sector = None
        business_idea = text.strip()
        if any(w in t_lower for w in ["dairy", "डेयरी", "doodh", "milk", "दूध", "food", "खाद्य", "pickle", "achaar", "अचार", "papad", "पापड़", "bakery", "makhana", "मखाना", "spices", "masala", "मसाला", "restaurant", "cafe", "dhaba", "mithai", "sweet"]):
            sector = "Food Processing"
        elif any(w in t_lower for w in ["handloom", "weaver", "bunkar", "बुनकर", "saree", "साड़ी", "सिलाई", "sewing", "tailor", "handicraft", "shilp", "शिल्प", "wood toy", "carpet", "pottery", "craft", "garment", "boutique"]):
            sector = "Handicraft/Handloom"
        elif any(w in t_lower for w in ["goat", "bakri", "बकरी", "poultry", "murgi", "मुर्गी", "fishery", "machhli", "मछली", "farming", "kheti", "खेती", "agri", "krishi", "कृषि", "pashupalan"]):
            sector = "Agri-allied"
        elif any(w in t_lower for w in ["software", "app", "tech", "computer", "website", "ai ", "digital", "mobile", "cyber"]):
            sector = "Tech/IT"
        elif any(w in t_lower for w in ["dukan", "shop", "kirana", "retail", "wholesale", "trading", "stall", "thela", "ठेला", "vendor", "vending", "street", "cart", "सब्जी", "vegetable", "दुकान", "किराना", "store", "mart", "cloth"]):
            sector = "Trading"
        elif any(w in t_lower for w in ["repair", "salon", "beauty parlour", "coaching", "mechanic", "dry cleaner", "service", "transport", "delivery", "clinic"]):
            sector = "Service"
        elif any(w in t_lower for w in ["factory", "manufacturing", "karkhana", "कारखाना", "production", "fabrication", "plant", "unit", "plastic", "textile", "विनिर्माण", "making", "produce"]):
            sector = "Manufacturing"

        # 8. Existing vs Greenfield (New) Business
        existing_business = False
        if any(w in t_lower for w in ["already", "running", "chalu", "purana", "expansion", "pehle se", "vistar", "chal raha hai", "पहले से", "चल रहा"]):
            existing_business = True

        # 9. Education
        education = None
        if any(w in t_lower for w in ["graduate", "degree", "ba", "bcom", "bsc", "btech", "engineer", "diploma"]):
            education = "Graduate / Diploma"
        elif any(w in t_lower for w in ["12th", "barahvi", "intermediate", "10+2", "12वीं"]):
            education = "12th Pass"
        elif any(w in t_lower for w in ["10th", "dasvi", "matric", "high school", "10वीं"]):
            education = "10th Pass"
        elif any(w in t_lower for w in ["8th", "aathvi", "middle school", "8वीं"]):
            education = "8th Pass"
        elif any(w in t_lower for w in ["anpadh", "uneducated", "illiterate", "padha likha nahi", "अनपढ़"]):
            education = "Below 8th"

        # 10. Urban / Rural
        urban_rural = "Rural" if any(w in t_lower for w in ["gaon", "village", "gram", "dehat", "rural", "khet", "गाँव", "गांव", "देहात"]) else "Urban"

        # Gender name inference fallback
        if not gender:
            if any(w in t_lower for w in ["devi", "kumari", "shrimati", "begum", "khatun", "bai", "behn", "didi", "parlour", "boutique", "saree", "सिलाई"]):
                gender = "Female"
            elif any(w in t_lower for w in ["shri", "kumar", "singh", "ram", "lal", "prasad", "sharma", "verma", "gupta", "yadav", "khan", "bhai", "babu", "ramesh", "suresh"]):
                gender = "Male"

        # INTELLIGENT DEFAULTS: Ensure no blank space is left unfilled
        final_age = age if age is not None else 30
        final_gender = gender or "Female"
        final_category = social_category or ("Women" if final_gender == "Female" else "General")
        final_sector = sector or "Manufacturing"
        final_investment = investment_needed if (investment_needed and investment_needed > 0) else 200000.0
        final_education = education or "10th Pass"
        final_income = annual_income if (annual_income and annual_income > 0) else 200000.0
        final_state = state or "Maharashtra"
        final_district = district or ("Pune" if final_state == "Maharashtra" else "Central")
        final_idea = business_idea if business_idea else f"{final_sector} enterprise requiring working capital"

        return UserProfile(
            age=final_age,
            gender=final_gender,
            annual_income=final_income,
            state=final_state,
            district=final_district,
            social_category=final_category,
            education=final_education,
            business_idea=final_idea[:250],
            sector=final_sector,
            investment_needed=final_investment,
            existing_business=existing_business,
            urban_rural=urban_rural
        )

    def enrich_scheme_advice(
        self,
        profile: UserProfile,
        results: List[SchemeMatchResult],
        max_items: int = 3
    ) -> List[SchemeMatchResult]:
        """
        Uses Gemini API to generate friendly, encouraging, plain-language guidance
        and actionable next steps for top matched schemes.
        Never breaks if API fails: keeps deterministic rule-based advice.
        """
        if not self._client or not results:
            return results

        try:
            top_schemes = results[:max_items]
            scheme_summaries = [
                f"- Scheme: {r.scheme.name} (Score: {r.match_score}%, Subsidy: {r.scheme.subsidy_details or r.scheme.subsidy_percentage})"
                for r in top_schemes
            ]

            prompt = f"""
You are an empathetic, knowledgeable enterprise mentor for Udhyami Yojna (उद्यमी योजना).
A user with the following profile has matched with top government schemes:
- Age: {profile.age or 'Not specified'}
- Gender: {profile.gender or 'Not specified'}
- Social Category: {profile.social_category or 'General'}
- Sector: {profile.sector or 'Micro business'}
- Business Idea: {profile.business_idea or 'Micro enterprise'}
- Loan Needed: ₹{profile.investment_needed or 100000:,.0f}
- State: {profile.state or 'India'}
- Location: {profile.urban_rural or 'Rural'}

Top Matched Schemes:
{chr(10).join(scheme_summaries)}

For each scheme, provide:
1. "plain_summary": A warm, easy-to-understand paragraph (2-3 sentences) explaining the main benefit and how to claim the subsidy.
2. "actionable_steps": 3 concrete, simple bullet-point steps the entrepreneur should take this week.

Return JSON matching this format:
[
  {{
    "scheme_id": "...",
    "plain_summary": "...",
    "actionable_steps": ["step 1", "step 2", "step 3"]
  }}
]
"""
            from google.genai import types

            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )

            if response and response.text:
                advice_list = json.loads(response.text)
                advice_map = {item.get("scheme_id"): item for item in advice_list if "scheme_id" in item}
                for r in results:
                    adv = advice_map.get(r.scheme.id)
                    if adv:
                        if adv.get("plain_summary"):
                            r.plain_summary = adv["plain_summary"]
                        if adv.get("actionable_steps"):
                            r.actionable_steps = adv["actionable_steps"]

        except Exception as e:
            logger.warning(f"Failed to enrich scheme advice with Gemini ({e}); retaining default rule summaries.")

        return results


gemini_service = GeminiService()
