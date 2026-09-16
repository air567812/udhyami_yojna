"""API routers for scheme discovery, AI voice extraction, matching, and state ecosystems."""
import json
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.config import settings
from backend.models import (
    TranscriptExtractRequest,
    ExtractionResponse,
    UserProfile,
    Scheme,
    SchemeMatchResponse,
    SchemeMatchResult,
    StateEcosystem
)
from backend.scoring_engine import load_schemes_catalog, match_user_schemes
from backend.gemini_service import gemini_service

logger = logging.getLogger("udhyami.routers")
router = APIRouter(prefix="/api", tags=["Udhyami Schemes & Discovery"])


@router.post(
    "/extract",
    response_model=ExtractionResponse,
    summary="Extract structured profile from voice transcript",
    description="Accepts speech transcript in Indian languages and extracts structured entrepreneur profile using Gemini AI (with intelligent heuristic fallback)."
)
async def extract_profile(request: TranscriptExtractRequest) -> ExtractionResponse:
    """
    Extracts structured user profile from free-form speech or text input.
    Guaranteed zero-crash fallback if Gemini is offline or unconfigured.
    """
    try:
        extraction = gemini_service.extract_profile_from_transcript(
            transcript=request.transcript,
            language=request.language
        )
        return extraction
    except Exception as e:
        logger.error(f"Unexpected error in /api/extract: {e}", exc_info=True)
        # Safe emergency fallback
        fallback = gemini_service._heuristic_fallback_extract(request.transcript)
        return ExtractionResponse(
            profile=fallback,
            confidence=0.5,
            extractor_used="emergency_fallback",
            notes="Recovered from internal error via basic parser."
        )


@router.post(
    "/match-schemes",
    response_model=SchemeMatchResponse,
    summary="Match and rank government schemes against user profile",
    description="Uses deterministic rule-based scoring as the source of truth to evaluate eligibility and rank schemes. Gemini AI enriches plain-language guidance."
)
async def match_schemes(profile: UserProfile) -> SchemeMatchResponse:
    """
    Evaluates applicant eligibility against all seeded central and state schemes.
    Deterministic rule engine computes match score (0-100), criteria met/unmet, and documents required.
    """
    try:
        matched_results, total_evaluated = match_user_schemes(profile)

        # AI advice enrichment for top 3 schemes if Gemini is active
        ai_enhanced = gemini_service.is_available
        if ai_enhanced:
            matched_results = gemini_service.enrich_scheme_advice(profile, matched_results, max_items=3)

        # Executive summary
        total_matched = len(matched_results)
        strong_count = sum(1 for r in matched_results if r.match_score >= 85)
        good_count = sum(1 for r in matched_results if 70 <= r.match_score < 85)

        if total_matched == 0:
            exec_summary = "No matching schemes found for the specified parameters. Try broadening sector or state selection."
        else:
            top_name = matched_results[0].scheme.name
            exec_summary = (
                f"Evaluated {total_evaluated} schemes. Found {total_matched} eligible schemes "
                f"({strong_count} Strong Matches, {good_count} Good Matches). "
                f"Top recommended initiative is '{top_name}' with a match score of {matched_results[0].match_score}%."
            )

        return SchemeMatchResponse(
            total_evaluated=total_evaluated,
            total_matched=total_matched,
            user_profile=profile,
            matched_schemes=matched_results,
            ai_enhanced=ai_enhanced,
            executive_summary=exec_summary
        )
    except Exception as e:
        logger.error(f"Error matching schemes: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scheme matching engine encountered an error: {str(e)}"
        )


@router.get(
    "/schemes",
    response_model=List[Scheme],
    summary="Browse and filter government schemes",
    description="Returns the full catalog of central and state government schemes with optional sector, state, category, and keyword filters."
)
async def list_schemes(
    sector: Optional[str] = Query(None, description="Filter by sector (e.g. Manufacturing, Food Processing)"),
    state: Optional[str] = Query(None, description="Filter by state code (e.g. MH, UP) or 'ALL' for Central"),
    category: Optional[str] = Query(None, description="Filter by target social group (SC, ST, OBC, Women, etc.)"),
    scheme_type: Optional[str] = Query(None, alias="type", description="Filter by type: 'Central' or 'State'"),
    search: Optional[str] = Query(None, description="Keyword search in name and description")
) -> List[Scheme]:
    """Retrieves filtered list of schemes."""
    schemes = load_schemes_catalog()

    if scheme_type:
        schemes = [s for s in schemes if s.type.lower() == scheme_type.lower()]

    if state and state.upper() != "ALL":
        st_code = state.upper()
        schemes = [s for s in schemes if s.state_code in [st_code, "ALL"]]

    if sector:
        sector_lower = sector.lower()
        schemes = [
            s for s in schemes
            if any(sector_lower in sec.lower() for sec in s.sectors)
        ]

    if category and category.lower() != "all":
        cat_upper = category.upper()
        schemes = [
            s for s in schemes
            if "ALL" in [c.upper() for c in s.target_categories] or
               any(cat_upper in c.upper() for c in s.target_categories)
        ]

    if search:
        q = search.lower()
        schemes = [
            s for s in schemes
            if q in s.name.lower() or
               (s.name_hi and q in s.name_hi.lower()) or
               q in s.description.lower() or
               q in s.ministry.lower()
        ]

    return schemes


@router.get(
    "/schemes/{scheme_id}",
    response_model=Scheme,
    summary="Get scheme details by ID",
    description="Fetches full criteria, subsidy terms, and documentation checklist for a specific scheme."
)
async def get_scheme_by_id(scheme_id: str) -> Scheme:
    """Fetch single scheme by unique identifier."""
    schemes = load_schemes_catalog()
    for s in schemes:
        if s.id.lower() == scheme_id.lower():
            return s
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheme with id '{scheme_id}' was not found in catalog."
    )


@router.get(
    "/states",
    response_model=List[StateEcosystem],
    summary="List all state entrepreneurial ecosystems",
    description="Returns regional industrial focus, single-window clearances, District Industries Centre (DIC) helplines, and industrial cluster specializations for Indian states."
)
async def list_states() -> List[StateEcosystem]:
    """Returns all state ecosystem profiles."""
    with open(settings.STATES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [StateEcosystem(**item) for item in data]


@router.get(
    "/states/{state_code}",
    response_model=dict,
    summary="Get state ecosystem profile and associated state schemes",
    description="Returns state industrial details, district clusters, DIC contacts, and all state-specific schemes."
)
async def get_state_details(state_code: str) -> dict:
    """Returns state details and corresponding state schemes."""
    code_upper = state_code.upper()
    with open(settings.STATES_FILE, "r", encoding="utf-8") as f:
        states_data = json.load(f)

    target_state = None
    for st in states_data:
        if st.get("state_code", "").upper() == code_upper:
            target_state = st
            break

    if not target_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"State with code '{state_code}' not found."
        )

    # Fetch state specific schemes
    all_schemes = load_schemes_catalog()
    state_schemes = [s.model_dump() for s in all_schemes if s.state_code.upper() == code_upper]
    central_schemes = [s.model_dump() for s in all_schemes if s.state_code.upper() == "ALL"]

    return {
        "ecosystem": target_state,
        "state_schemes": state_schemes,
        "central_schemes_available": len(central_schemes)
    }
