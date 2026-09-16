"""Integration tests for FastAPI endpoints with mocked Gemini service."""
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models import UserProfile, ExtractionResponse


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "Udhyami Yojna"


def test_list_schemes_all(client):
    response = client.get("/api/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert isinstance(schemes, list)
    assert len(schemes) >= 15


def test_list_schemes_filter_sector(client):
    response = client.get("/api/schemes?sector=Food Processing")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) > 0
    for s in schemes:
        assert any("food" in sec.lower() for sec in s["sectors"])


def test_list_schemes_filter_type(client):
    res_central = client.get("/api/schemes?type=Central")
    assert res_central.status_code == 200
    for s in res_central.json():
        assert s["type"] == "Central"

    res_state = client.get("/api/schemes?type=State")
    assert res_state.status_code == 200
    for s in res_state.json():
        assert s["type"] == "State"


def test_get_scheme_by_id(client):
    response = client.get("/api/schemes/pmegp")
    assert response.status_code == 200
    scheme = response.json()
    assert scheme["id"] == "pmegp"
    assert "PMEGP" in scheme["name"]
    assert len(scheme["required_documents"]) > 0


def test_get_scheme_by_id_not_found(client):
    response = client.get("/api/schemes/non_existent_scheme_xyz")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_states(client):
    response = client.get("/api/states")
    assert response.status_code == 200
    states = response.json()
    assert isinstance(states, list)
    assert len(states) >= 10
    state_codes = [s["state_code"] for s in states]
    assert "MH" in state_codes
    assert "UP" in state_codes
    assert "TN" in state_codes


def test_get_state_details(client):
    response = client.get("/api/states/MH")
    assert response.status_code == 200
    data = response.json()
    assert "ecosystem" in data
    assert data["ecosystem"]["name"] == "Maharashtra"
    assert "district_clusters" in data["ecosystem"]
    assert len(data["ecosystem"]["district_clusters"]) > 0
    assert "state_schemes" in data
    assert len(data["state_schemes"]) > 0


def test_get_state_details_not_found(client):
    response = client.get("/api/states/ZZ")
    assert response.status_code == 404


def test_post_match_schemes_endpoint(client):
    payload = {
        "age": 29,
        "gender": "Female",
        "social_category": "OBC",
        "state": "Uttar Pradesh",
        "district": "Varanasi",
        "sector": "Manufacturing",
        "investment_needed": 1000000,
        "existing_business": False,
        "urban_rural": "Rural"
    }
    response = client.post("/api/match-schemes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_matched"] > 0
    assert data["total_evaluated"] >= 15
    assert len(data["matched_schemes"]) > 0
    # First scheme should have highest match score
    first = data["matched_schemes"][0]
    assert "match_score" in first
    assert "why_matched" in first
    assert len(first["why_matched"]) > 0
    assert "required_documents" in first
    assert "official_url" in first


def test_post_extract_with_mocked_gemini(client):
    mock_profile = UserProfile(
        age=35,
        gender="Female",
        annual_income=250000,
        state="Tamil Nadu",
        social_category="Women",
        sector="Handicraft/Handloom",
        investment_needed=500000,
        existing_business=False
    )

    with patch("backend.gemini_service.gemini_service.extract_profile_from_transcript") as mock_extract:
        mock_extract.return_value = ExtractionResponse(
            profile=mock_profile,
            confidence=0.95,
            extractor_used="gemini",
            notes="Mocked Gemini extraction."
        )

        response = client.post(
            "/api/extract",
            json={"transcript": "Test speech input", "language": "ta-IN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["profile"]["age"] == 35
        assert data["profile"]["gender"] == "Female"
        assert data["profile"]["state"] == "Tamil Nadu"
        assert data["extractor_used"] == "gemini"


def test_post_extract_input_validation(client):
    # Empty transcript should fail validation (min_length=1)
    response = client.post("/api/extract", json={"transcript": "   ", "language": "hi-IN"})
    assert response.status_code == 422
