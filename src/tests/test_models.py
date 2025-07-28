import pytest

from models.models import CreateScrapingJobModel


def _valid_payload() -> dict:
    """Return a baseline valid payload for CreateScrapingJobModel."""
    return {
        "name": "My scraping job",
        "keywords": ["pizza", "restaurants"],
        "lang": "en",
        "zoom": 15,
        "lat": 40.0,
        "lon": -3.0,
        "fast_mode": True,
        "radius": 5_000,
        "depth": 10,
        "email": True,
        "max_time": 600,
        "proxies": [],
    }


def test_valid_model_creation_and_payload_conversion():
    """A fully-populated, valid payload should create the model and convert correctly."""
    model = CreateScrapingJobModel(**_valid_payload())

    # Basic attribute assertions
    assert model.name == "My scraping job"
    assert model.keywords == ["pizza", "restaurants"]

    # Latitude/Longitude must be converted to *string* when building API payload
    payload = model.to_api_payload()
    assert isinstance(payload["lat"], str)
    assert isinstance(payload["lon"], str)
    assert payload["lat"] == "40.0"
    assert payload["lon"] == "-3.0"


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),                # Empty name
        ("keywords", []),             # Empty keywords list
        ("keywords", ["", "test"]), # Keyword with empty string
        ("lang", ""),               # Empty language code
    ],
)
def test_validation_errors_for_empty_fields(field, value):
    """Model should raise ValueError when required string/list fields are empty."""
    data = _valid_payload()
    data[field] = value
    with pytest.raises(ValueError):
        CreateScrapingJobModel(**data)


@pytest.mark.parametrize(
    "field,value",
    [
        ("zoom", -1),
        ("radius", -10),
        ("depth", -5),
        ("max_time", -60),
    ],
)
def test_validation_errors_for_negative_integers(field, value):
    """Numerical fields declared as non-negative must raise on negative input."""
    data = _valid_payload()
    data[field] = value
    with pytest.raises(ValueError):
        CreateScrapingJobModel(**data)


def test_whitespace_is_trimmed():
    """Leading/trailing whitespace in string inputs should be stripped by validators."""
    data = _valid_payload()
    data["name"] = "  My scraping job  "
    data["keywords"] = ["  pizza  ", "   coffee"]

    model = CreateScrapingJobModel(**data)

    assert model.name == "My scraping job"
    assert model.keywords == ["pizza", "coffee"] 