"""Unit tests for deterministic rule-based scheme scoring engine."""
import pytest
from backend.models import UserProfile, Scheme
from backend.scoring_engine import (
    load_schemes_catalog,
    evaluate_scheme,
    match_user_schemes,
    matches_state
)


@pytest.fixture
def catalog():
    return load_schemes_catalog()


def get_scheme(catalog, scheme_id):
    for s in catalog:
        if s.id == scheme_id:
            return s
    raise ValueError(f"Scheme {scheme_id} not found in test catalog")


def test_catalog_loads_successfully(catalog):
    assert len(catalog) >= 15
    central_schemes = [s for s in catalog if s.type == "Central"]
    state_schemes = [s for s in catalog if s.type == "State"]
    assert len(central_schemes) >= 8
    assert len(state_schemes) >= 5


def test_state_matching_logic():
    assert matches_state("ALL", "Maharashtra") is True
    assert matches_state("MH", "Maharashtra") is True
    assert matches_state("MH", "MH") is True
    assert matches_state("MH", "Pune") is True
    assert matches_state("MH", "Bihar") is False
    assert matches_state("UP", "Uttar Pradesh") is True
    assert matches_state("UP", "Tamil Nadu") is False


def test_stand_up_india_eligibility(catalog):
    stand_up = get_scheme(catalog, "stand_up_india")

    # 1. Male General should NOT be eligible for Stand-Up India
    male_gen = UserProfile(
        age=30,
        gender="Male",
        social_category="General",
        investment_needed=2500000,
        existing_business=False
    )
    res1 = evaluate_scheme(stand_up, male_gen)
    assert res1.match_score == 0
    assert res1.match_grade == "Not Eligible"
    assert any("SC, ST, or Woman" in u for u in res1.unmet_criteria)

    # 2. Female General should BE eligible
    fem_gen = UserProfile(
        age=30,
        gender="Female",
        social_category="General",
        investment_needed=2500000,
        existing_business=False
    )
    res2 = evaluate_scheme(stand_up, fem_gen)
    assert res2.match_score > 0
    assert any("Woman entrepreneur" in w for w in res2.why_matched)

    # 3. Male SC should BE eligible
    male_sc = UserProfile(
        age=30,
        gender="Male",
        social_category="SC",
        investment_needed=2500000,
        existing_business=False
    )
    res3 = evaluate_scheme(stand_up, male_sc)
    assert res3.match_score > 0
    assert any("SC category" in w for w in res3.why_matched)


def test_mudra_loan_brackets(catalog):
    shishu = get_scheme(catalog, "mudra_shishu")
    kishore = get_scheme(catalog, "mudra_kishore")
    tarun = get_scheme(catalog, "mudra_tarun")

    # Asking ₹30,000
    micro_profile = UserProfile(
        age=28,
        gender="Female",
        investment_needed=30000,
        existing_business=False
    )
    res_shishu = evaluate_scheme(shishu, micro_profile)
    assert res_shishu.match_score >= 80

    # Asking ₹3,00,000 -> Shishu is disqualified (exceeds max ₹50,000 * 2)
    mid_profile = UserProfile(
        age=28,
        gender="Female",
        investment_needed=300000,
        existing_business=False
    )
    res_shishu_mid = evaluate_scheme(shishu, mid_profile)
    assert res_shishu_mid.match_score == 0
    assert res_shishu_mid.match_grade == "Not Eligible"

    res_kishore_mid = evaluate_scheme(kishore, mid_profile)
    assert res_kishore_mid.match_score >= 80


def test_age_restrictions(catalog):
    pmegp = get_scheme(catalog, "pmegp")

    # Under 18 years old
    minor = UserProfile(
        age=16,
        gender="Male",
        social_category="OBC",
        investment_needed=500000
    )
    res_minor = evaluate_scheme(pmegp, minor)
    assert res_minor.match_score == 0
    assert any("Minimum age" in u for u in res_minor.unmet_criteria)

    # Age 30 (Valid)
    adult = UserProfile(
        age=30,
        gender="Male",
        social_category="OBC",
        investment_needed=500000,
        existing_business=False
    )
    res_adult = evaluate_scheme(pmegp, adult)
    assert res_adult.match_score > 70


def test_existing_business_restriction(catalog):
    pmegp = get_scheme(catalog, "pmegp")
    mudra_kishore = get_scheme(catalog, "mudra_kishore")

    existing_biz_profile = UserProfile(
        age=35,
        gender="Male",
        social_category="OBC",
        investment_needed=400000,
        existing_business=True  # Expansion of existing enterprise
    )

    # PMEGP first loan requires greenfield
    res_pmegp = evaluate_scheme(pmegp, existing_biz_profile)
    assert res_pmegp.match_score == 0
    assert any("exclusively for setting up new (greenfield) enterprises" in u for u in res_pmegp.unmet_criteria)

    # Mudra Kishore permits existing business
    res_mudra = evaluate_scheme(mudra_kishore, existing_biz_profile)
    assert res_mudra.match_score > 70


def test_state_specific_scheme_filtering(catalog):
    maha_cmegp = get_scheme(catalog, "maha_cmegp")

    # User from Maharashtra
    mh_user = UserProfile(
        age=26,
        gender="Female",
        state="Maharashtra",
        investment_needed=1000000,
        existing_business=False
    )
    res_mh = evaluate_scheme(maha_cmegp, mh_user)
    assert res_mh.match_score > 75

    # User from Bihar (disqualified for Maharashtra CMEGP)
    br_user = UserProfile(
        age=26,
        gender="Female",
        state="Bihar",
        investment_needed=1000000,
        existing_business=False
    )
    res_br = evaluate_scheme(maha_cmegp, br_user)
    assert res_br.match_score == 0
    assert any("State-specific scheme for MH" in u for u in res_br.unmet_criteria)


def test_match_user_schemes_ranking():
    # Female SC entrepreneur from Maharashtra seeking 20 Lakhs for greenfield food processing
    profile = UserProfile(
        age=32,
        gender="Female",
        social_category="SC",
        state="Maharashtra",
        sector="Food Processing",
        investment_needed=2000000,
        existing_business=False
    )
    matched, total = match_user_schemes(profile)
    assert total >= 15
    assert len(matched) >= 3

    # Top matches should have high scores (>= 80)
    top_scheme_ids = [m.scheme.id for m in matched[:3]]
    assert "stand_up_india" in top_scheme_ids or "pmegp" in top_scheme_ids or "pmfme" in top_scheme_ids or "maha_cmegp" in top_scheme_ids
    assert matched[0].match_score >= matched[1].match_score
