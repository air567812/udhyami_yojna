"""Unit tests for offline heuristic fallback parser and Gemini service resilience."""
import pytest
from backend.gemini_service import GeminiService


@pytest.fixture
def service():
    # Service with no API key -> tests fallback path directly
    return GeminiService()


def test_fallback_hindi_woman_garments(service):
    transcript = "मैं 28 साल की महिला हूँ, उत्तर प्रदेश से। सिलाई और रेडीमेड कपड़ों के व्यवसाय के लिए 5 लाख का लोन चाहिए।"
    profile = service._heuristic_fallback_extract(transcript)

    assert profile.age == 28
    assert profile.gender == "Female"
    assert profile.state == "Uttar Pradesh"
    assert profile.investment_needed == 500000.0
    assert profile.existing_business is False


def test_fallback_sc_greenfield_manufacturing(service):
    transcript = "I am 32 years old, SC category from Maharashtra. Starting a new manufacturing unit, need 25 lakhs loan."
    profile = service._heuristic_fallback_extract(transcript)

    assert profile.age == 32
    assert profile.social_category == "SC"
    assert profile.state == "Maharashtra"
    assert profile.sector == "Manufacturing"
    assert profile.investment_needed == 2500000.0
    assert profile.existing_business is False


def test_fallback_street_vendor_micro(service):
    transcript = "I run a small vegetable vending cart in Delhi, annual income 1.5 lakh, need 20,000 working capital."
    profile = service._heuristic_fallback_extract(transcript)

    assert profile.state == "Delhi"
    assert profile.sector == "Trading"
    assert profile.investment_needed == 20000.0
    assert profile.annual_income == 150000.0


def test_fallback_bihar_food_dairy(service):
    transcript = "बिहार से हूँ, 24 वर्ष, ओबीसी। डेयरी और मखाना प्रोसेसिंग यूनिट के लिए 8 लाख का लोन चाहिए।"
    profile = service._heuristic_fallback_extract(transcript)

    assert profile.age == 24
    assert profile.social_category == "OBC"
    assert profile.state == "Bihar"
    assert profile.sector == "Food Processing"
    assert profile.investment_needed == 800000.0


def test_fallback_existing_business_flag(service):
    transcript = "मेरा पहले से कपड़े का दुकान चल रहा है, 4 लाख की जरूरत है।"
    profile = service._heuristic_fallback_extract(transcript)

    assert profile.existing_business is True
    assert profile.investment_needed == 400000.0


def test_fallback_never_crashes_on_empty_or_gibberish(service):
    # Should not raise exception
    p1 = service._heuristic_fallback_extract("")
    assert p1 is not None

    p2 = service._heuristic_fallback_extract("hello test bla bla xyz 123 !@#$%^")
    assert p2 is not None


def test_extract_profile_returns_fallback_when_gemini_offline(service):
    # Since GEMINI_API_KEY is not set or mocked, extract_profile_from_transcript should cleanly return fallback
    result = service.extract_profile_from_transcript(
        transcript="I need 10 lakh loan for my food packaging business in Gujarat, age 30",
        language="en-IN"
    )
    assert result.profile is not None
    assert result.profile.age == 30
    assert result.profile.state == "Gujarat"
    assert result.profile.investment_needed == 1000000.0
    assert result.extractor_used == "fallback_heuristic"
