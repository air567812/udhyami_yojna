"""Deterministic rule-based scheme scoring and eligibility engine."""
import json
import re
from typing import List, Tuple, Optional
from backend.config import settings
from backend.models import UserProfile, Scheme, SchemeMatchResult

# State code mapping helper
STATE_SYNONYMS = {
    "MH": ["maharashtra", "mh", "mumbai", "pune", "nagpur"],
    "UP": ["uttar pradesh", "up", "lucknow", "kanpur", "varanasi", "agra"],
    "TN": ["tamil nadu", "tn", "chennai", "coimbatore", "madurai", "salem"],
    "GJ": ["gujarat", "gj", "ahmedabad", "surat", "vadodara", "rajkot"],
    "KA": ["karnataka", "ka", "bengaluru", "bangalore", "mysuru", "hubli"],
    "BR": ["bihar", "br", "patna", "gaya", "muzaffarpur", "bhagalpur"],
    "RJ": ["rajasthan", "rj", "jaipur", "jodhpur", "udaipur", "kota"],
    "WB": ["west bengal", "wb", "kolkata", "howrah", "darjeeling"],
    "TG": ["telangana", "tg", "ts", "hyderabad", "warangal"],
    "AS": ["assam", "as", "guwahati", "dispur", "silchar", "jorhat"],
    "OD": ["odisha", "orissa", "od", "or", "bhubaneswar", "cuttack"],
    "KL": ["kerala", "kl", "kochi", "thiruvananthapuram", "kozhikode"],
    "MP": ["madhya pradesh", "mp", "bhopal", "indore", "gwalior"],
    "PB": ["punjab", "pb", "amritsar", "ludhiana", "jalandhar"],
    "AP": ["andhra pradesh", "ap", "visakhapatnam", "vijayawada", "guntur"],
    "DL": ["delhi", "dl", "nct", "new delhi"]
}


def matches_state(scheme_state_code: str, user_state: Optional[str]) -> bool:
    """Checks whether the user's state matches the scheme's geographical mandate."""
    if scheme_state_code == "ALL" or not scheme_state_code:
        return True
    if not user_state:
        # If user did not provide state, allow central and potentially state with neutral score
        return True

    user_st_clean = user_state.strip().lower()
    target_code = scheme_state_code.upper()

    # Direct match on code
    if user_st_clean == target_code.lower():
        return True

    # Synonyms check
    synonyms = STATE_SYNONYMS.get(target_code, [])
    for syn in synonyms:
        if syn in user_st_clean or user_st_clean in syn:
            return True

    return False


def load_schemes_catalog() -> List[Scheme]:
    """Loads schemes from the JSON data file."""
    with open(settings.SCHEMES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Scheme(**item) for item in data]


def evaluate_scheme(scheme: Scheme, profile: UserProfile) -> SchemeMatchResult:
    """
    Deterministically scores a scheme against a user profile using rule-based scoring (0-100).
    Returns detailed explanations of matched and unmet criteria.
    """
    why_matched: List[str] = []
    unmet_criteria: List[str] = []
    disqualified = False

    # 1. Hard Check: State restriction
    if scheme.state_code != "ALL" and profile.state:
        if not matches_state(scheme.state_code, profile.state):
            disqualified = True
            unmet_criteria.append(
                f"State-specific scheme for {scheme.state_code}; your registered state is {profile.state}."
            )

    # 2. Hard Check: Age limit
    if profile.age is not None:
        if scheme.min_age and profile.age < scheme.min_age:
            disqualified = True
            unmet_criteria.append(
                f"Minimum age required is {scheme.min_age} years (Applicant age: {profile.age})."
            )
        elif scheme.max_age and profile.age > scheme.max_age:
            disqualified = True
            unmet_criteria.append(
                f"Maximum age limit is {scheme.max_age} years (Applicant age: {profile.age})."
            )
        else:
            why_matched.append(
                f"Age criteria met: {profile.age} years falls within eligible band ({scheme.min_age or 18} to {scheme.max_age or 65} years)."
            )

    # 3. Hard Check: Stand-Up India / Category and Gender requirements
    if scheme.id == "stand_up_india":
        is_sc_st = profile.social_category in ["SC", "ST"]
        is_woman = profile.gender == "Female"
        if profile.social_category is not None and profile.gender is not None:
            if not (is_sc_st or is_woman):
                disqualified = True
                unmet_criteria.append(
                    "Stand-Up India strictly mandates borrower to be an SC, ST, or Woman entrepreneur."
                )
            else:
                qualifier = "Woman entrepreneur" if is_woman else f"{profile.social_category} category entrepreneur"
                why_matched.append(f"Stand-Up India criteria fulfilled: Registered as {qualifier}.")

    # 4. Hard Check: Existing Business status (Greenfield vs Expansion)
    if profile.existing_business is True and not scheme.existing_business_allowed:
        disqualified = True
        unmet_criteria.append(
            "Scheme is exclusively for setting up new (greenfield) enterprises; existing units are not eligible for 1st tranche."
        )
    elif profile.existing_business is False and not scheme.existing_business_allowed:
        why_matched.append("Greenfield preference met: Starting a brand new venture matches scheme mandate.")

    # 5. Hard Check: Income ceiling
    if scheme.max_income and profile.annual_income is not None:
        if profile.annual_income > scheme.max_income:
            disqualified = True
            unmet_criteria.append(
                f"Annual household income exceeds maximum ceiling of ₹{scheme.max_income:,.0f} (Reported: ₹{profile.annual_income:,.0f})."
            )
        else:
            why_matched.append(
                f"Income eligible: Annual income ₹{profile.annual_income:,.0f} is within limit of ₹{scheme.max_income:,.0f}."
            )

    # 6. Loan range suitability
    if profile.investment_needed is not None and profile.investment_needed > 0:
        loan_req = profile.investment_needed
        # Severe mismatch
        if scheme.max_loan and loan_req > (scheme.max_loan * 2.0):
            disqualified = True
            unmet_criteria.append(
                f"Loan required (₹{loan_req:,.0f}) significantly exceeds scheme upper limit of ₹{scheme.max_loan:,.0f}."
            )
        elif scheme.min_loan and loan_req < (scheme.min_loan * 0.4):
            # E.g. Stand Up India minimum is 10L, user asking 10k
            disqualified = True
            unmet_criteria.append(
                f"Loan required (₹{loan_req:,.0f}) is below minimum threshold of ₹{scheme.min_loan:,.0f}."
            )

    if disqualified:
        return SchemeMatchResult(
            scheme=scheme,
            match_score=0,
            match_grade="Not Eligible",
            why_matched=why_matched,
            unmet_criteria=unmet_criteria,
            plain_summary=f"You currently do not qualify for {scheme.name} due to specific eligibility boundaries.",
            actionable_steps=["Review unmet conditions or explore alternative schemes."],
            required_documents=scheme.required_documents,
            official_url=scheme.official_url
        )

    # Calculate Weighted Match Score (Max 100 Points)
    category_score = 0
    sector_score = 0
    loan_score = 0
    geo_score = 0
    readiness_score = 0

    # A. Social Category & Inclusion Score (25 Points)
    user_cat = profile.social_category or "General"
    is_target_cat = "All" in scheme.target_categories or user_cat in scheme.target_categories
    is_woman = profile.gender == "Female"
    is_special = bool(profile.special_category) or user_cat in ["Divyangjan", "SC", "ST"]

    if scheme.id == "stand_up_india" and (user_cat in ["SC", "ST"] or is_woman):
        category_score = 25
    elif user_cat in scheme.target_categories and user_cat != "All":
        category_score = 25
        why_matched.append(f"Target social group match: Special priority & higher subsidy for {user_cat} category.")
    elif is_woman and ("Women" in scheme.target_categories or "Female" in scheme.target_genders or "All" in scheme.target_categories):
        category_score = 25
        why_matched.append("Women entrepreneur preference: Eligible for higher subsidy slab / lower promoter margin.")
    elif is_special:
        category_score = 25
        why_matched.append("Special category prioritization applied.")
    elif is_target_cat:
        category_score = 20
        why_matched.append(f"Social category {user_cat} is fully eligible.")
    else:
        category_score = 12

    # B. Sector & Industry Fit (25 Points)
    if not profile.sector:
        sector_score = 18
        why_matched.append("Applicable across broad enterprise sectors.")
    elif profile.sector in scheme.sectors:
        sector_score = 25
        why_matched.append(f"Sector match: {profile.sector} is an explicitly supported activity.")
    elif "All" in scheme.sectors or len(scheme.sectors) >= 4:
        sector_score = 20
        why_matched.append(f"Broad sector coverage includes {profile.sector}.")
    else:
        sector_score = 10
        unmet_criteria.append(
            f"Scheme prioritizes {', '.join(scheme.sectors[:3])}; your sector {profile.sector} may require review."
        )

    # C. Loan & Financial Bracket Fit (25 Points)
    if profile.investment_needed is None or profile.investment_needed == 0:
        loan_score = 18
        why_matched.append(f"Offers funding bracket from ₹{scheme.min_loan:,.0f} up to ₹{scheme.max_loan:,.0f}.")
    else:
        loan_req = profile.investment_needed
        if (scheme.min_loan or 0) <= loan_req <= (scheme.max_loan or 50000000):
            loan_score = 25
            why_matched.append(
                f"Financial fit: Required capital ₹{loan_req:,.0f} aligns with scheme loan bracket (₹{scheme.min_loan:,.0f} to ₹{scheme.max_loan:,.0f})."
            )
        else:
            # Slight deviation
            loan_score = 12
            why_matched.append(
                f"Financing permissible with adjusted project scope (Scheme limit: ₹{scheme.max_loan:,.0f})."
            )

    # D. Geographical & State Focus (15 Points)
    if scheme.state_code != "ALL":
        geo_score = 15
        why_matched.append(f"State initiative advantage: High-priority localized support for {scheme.state_code}.")
    else:
        geo_score = 13
        why_matched.append("Pan-India Central Government Scheme available across all districts.")

    # E. Entrepreneur Stage & Education (10 Points)
    if scheme.existing_business_allowed:
        readiness_score += 5
    else:
        readiness_score += 5

    if scheme.education_requirement:
        if profile.education:
            readiness_score += 5
            why_matched.append(f"Education guidelines: {scheme.education_requirement}.")
        else:
            readiness_score += 3
    else:
        readiness_score += 5
        why_matched.append("No restrictive educational barrier.")

    # Total Score
    total_score = min(100, max(1, category_score + sector_score + loan_score + geo_score + readiness_score))

    if total_score >= 85:
        match_grade = "Strong Match"
    elif total_score >= 70:
        match_grade = "Good Match"
    elif total_score >= 50:
        match_grade = "Moderate Match"
    else:
        match_grade = "Low Match"

    # Friendly Plain-language summary & actionable next steps
    subsidy_callout = scheme.subsidy_details or scheme.subsidy_percentage or "Credit-linked support"
    plain_summary = (
        f"You qualify strongly for {scheme.name}. Under this scheme, you can receive {subsidy_callout}. "
        f"It is specifically designed to support entrepreneurs in {profile.sector or 'your sector'} "
        f"with financial assistance and bank credit guarantees."
    )

    actionable_steps = [
        f"Prepare your basic KYC documents: Aadhaar Card, PAN Card, and Bank Account passbook.",
        f"Draft a brief project note or quotation for machinery/supplies needed (₹{profile.investment_needed or 100000:,.0f}).",
        f"Submit application online via the official portal ({scheme.official_url}) or visit your local District Industries Centre (DIC) / bank branch."
    ]

    return SchemeMatchResult(
        scheme=scheme,
        match_score=total_score,
        match_grade=match_grade,
        why_matched=why_matched,
        unmet_criteria=unmet_criteria,
        plain_summary=plain_summary,
        actionable_steps=actionable_steps,
        required_documents=scheme.required_documents,
        official_url=scheme.official_url
    )


def match_user_schemes(profile: UserProfile) -> Tuple[List[SchemeMatchResult], int]:
    """
    Evaluates all schemes in catalog against profile.
    Returns sorted list of eligible matched schemes (highest score first) and total evaluated count.
    """
    catalog = load_schemes_catalog()
    results = [evaluate_scheme(scheme, profile) for scheme in catalog]

    # Filter out completely disqualified (score == 0) unless nothing matched
    matched = [r for r in results if r.match_score > 0]
    matched.sort(key=lambda x: x.match_score, reverse=True)

    return matched, len(catalog)
