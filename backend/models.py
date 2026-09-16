"""Pydantic models for request validation, profile extraction, and scheme scoring."""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class TranscriptExtractRequest(BaseModel):
    """Payload for speech transcript extraction."""
    transcript: str = Field(..., min_length=1, max_length=10000, description="Raw speech or text input from user")
    language: str = Field(default="hi-IN", max_length=10, description="Locale code (e.g. hi-IN, en-IN)")

    @field_validator("transcript")
    @classmethod
    def sanitize_transcript(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Transcript cannot be empty or only whitespace")
        return cleaned


class UserProfile(BaseModel):
    """Structured user profile representation used for scheme eligibility evaluation."""
    age: Optional[int] = Field(default=None, ge=14, le=100, description="Age in completed years")
    gender: Optional[str] = Field(default=None, description="Gender: Male, Female, Other")
    annual_income: Optional[float] = Field(default=None, ge=0, description="Annual household income in INR")
    state: Optional[str] = Field(default=None, description="State of residence or enterprise location")
    district: Optional[str] = Field(default=None, description="District name")
    social_category: Optional[str] = Field(
        default=None,
        description="Social group: General, OBC, SC, ST, Minority, Women, Divyangjan, EBC"
    )
    education: Optional[str] = Field(
        default=None,
        description="Highest education level: Below 8th, 8th Pass, 10th Pass, 12th Pass, Graduate / Diploma, Post Graduate"
    )
    business_idea: Optional[str] = Field(default=None, max_length=1000, description="Brief description of enterprise or venture")
    sector: Optional[str] = Field(
        default=None,
        description="Industry sector: Manufacturing, Service, Trading, Food Processing, Handicraft/Handloom, Agri-allied, Tech/IT"
    )
    investment_needed: Optional[float] = Field(default=None, ge=0, description="Loan or capital investment required in INR")
    existing_business: Optional[bool] = Field(
        default=False,
        description="True if expanding existing business, False if starting a brand new venture (greenfield)"
    )
    urban_rural: Optional[str] = Field(default="Rural", description="Location type: Rural or Urban")
    special_category: Optional[List[str]] = Field(default_factory=list, description="Divyangjan, Ex-Servicemen, NER, etc.")

    @field_validator("gender")
    @classmethod
    def normalize_gender(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v_lower = v.strip().lower()
        if "fem" in v_lower or "mahila" in v_lower or "aurat" in v_lower or "stri" in v_lower:
            return "Female"
        if "male" in v_lower or "purush" in v_lower or "aadmi" in v_lower:
            return "Male"
        return "Other"

    @field_validator("social_category")
    @classmethod
    def normalize_category(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v_upper = v.strip().upper()
        if "SC" in v_upper or "SCHEDULED CASTE" in v_upper or "DALIT" in v_upper:
            return "SC"
        if "ST" in v_upper or "SCHEDULED TRIBE" in v_upper or "ADIVASI" in v_upper:
            return "ST"
        if "OBC" in v_upper or "OTHER BACKWARD" in v_upper:
            return "OBC"
        if "MINORITY" in v_upper or "MUSLIM" in v_upper or "CHRISTIAN" in v_upper or "SIKH" in v_upper or "BUDDHIST" in v_upper or "JAIN" in v_upper:
            return "Minority"
        if "DIVYANG" in v_upper or "PWD" in v_upper or "HANDICAP" in v_upper or "DISABLED" in v_upper:
            return "Divyangjan"
        if "WOMEN" in v_upper or "FEMALE" in v_upper:
            return "Women"
        if "EBC" in v_upper:
            return "EBC"
        if "GEN" in v_upper:
            return "General"
        return v.strip().title()

    @field_validator("sector")
    @classmethod
    def normalize_sector(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        v_lower = v.strip().lower()
        if any(w in v_lower for w in ["food", "dairy", "bakery", "pickle", "spice", "grain", "oil mill", "khadya"]):
            return "Food Processing"
        if any(w in v_lower for w in ["craft", "handloom", "weaver", "carpet", "pottery", "artisan", "bunkar", "silpi"]):
            return "Handicraft/Handloom"
        if any(w in v_lower for w in ["agri", "farm", "goat", "poultry", "fishery", "krishi", "pashupalan"]):
            return "Agri-allied"
        if any(w in v_lower for w in ["software", "tech", "app", "digital", "computer", "it "]):
            return "Tech/IT"
        if any(w in v_lower for w in ["shop", "retail", "wholesale", "trading", "kirana", "vendor", "stall", "dukan"]):
            return "Trading"
        if any(w in v_lower for w in ["service", "repair", "salon", "laundry", "clinic", "coaching", "sewa"]):
            return "Service"
        if any(w in v_lower for w in ["manufactur", "factory", "unit", "production", "fabricat", "plastic", "textile", "utpadan"]):
            return "Manufacturing"
        return v.strip().title()


class ExtractionResponse(BaseModel):
    """Result of AI/heuristic extraction."""
    profile: UserProfile
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    extractor_used: str = Field(default="gemini", description="'gemini' or 'fallback_heuristic'")
    notes: Optional[str] = None


class Scheme(BaseModel):
    """Full scheme definition from catalog."""
    id: str
    name: str
    name_hi: Optional[str] = None
    ministry: str
    type: str  # "Central" or "State"
    state_code: str = "ALL"
    min_age: Optional[int] = 18
    max_age: Optional[int] = 70
    target_genders: List[str] = Field(default_factory=lambda: ["All"])
    target_categories: List[str] = Field(default_factory=lambda: ["All"])
    max_income: Optional[float] = None
    min_loan: Optional[float] = 0
    max_loan: Optional[float] = 50000000
    subsidy_percentage: Optional[str] = None
    subsidy_details: Optional[str] = None
    sectors: List[str] = Field(default_factory=list)
    existing_business_allowed: bool = True
    education_requirement: Optional[str] = None
    required_documents: List[str] = Field(default_factory=list)
    official_url: str
    description: str


class SchemeMatchResult(BaseModel):
    """Scored and explained result for an individual scheme."""
    scheme: Scheme
    match_score: int = Field(ge=0, le=100, description="Rule-based match score out of 100")
    match_grade: str = Field(description="'Strong Match', 'Good Match', 'Moderate Match', 'Low Match'")
    why_matched: List[str] = Field(default_factory=list, description="Explicit reasons and met criteria")
    unmet_criteria: List[str] = Field(default_factory=list, description="Advisory or unmet parameters")
    plain_summary: str = Field(description="Plain-language, easy-to-understand explanation")
    actionable_steps: List[str] = Field(default_factory=list, description="Concrete next steps to apply")
    required_documents: List[str] = Field(default_factory=list)
    official_url: str


class SchemeMatchResponse(BaseModel):
    """Response returned by /api/match-schemes."""
    total_evaluated: int
    total_matched: int
    user_profile: UserProfile
    matched_schemes: List[SchemeMatchResult]
    ai_enhanced: bool = False
    executive_summary: str


class DistrictCluster(BaseModel):
    district: str
    specialty: str


class StateEcosystem(BaseModel):
    state_code: str
    name: str
    name_hi: Optional[str] = None
    capital: str
    region: str
    key_sectors: List[str] = Field(default_factory=list)
    single_window_portal: str
    dic_portal: str
    helpline: str
    nodal_agency: str
    regional_initiatives: str
    district_clusters: List[DistrictCluster] = Field(default_factory=list)
