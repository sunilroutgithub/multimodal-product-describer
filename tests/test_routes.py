from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import ProductDescription

client = TestClient(app)


def test_health_check():
    """The /health endpoint should always return 200 and status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.routes.describe_image")
def test_describe_single_image_success(mock_describe):
    """
    /describe should return a successful BatchResult when the vision
    service returns a valid ProductDescription.
    We mock describe_image so this test never calls the real Groq API.
    """
    mock_describe.return_value = ProductDescription(
        title="Mock Product",
        short_description="A mock short description.",
        long_description="A mock long description of the product.",
        bullet_points=["Mock point 1", "Mock point 2"],
        seo_keywords=["mock", "test"],
        category_guess="Mock Category",
    )

    fake_image = b"fake image bytes"
    response = client.post(
        "/describe",
        files={"file": ("test.jpg", fake_image, "image/jpeg")},
        data={"brand_tone": "professional", "target_keywords": "test,mock"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["description"]["title"] == "Mock Product"


@patch("app.api.routes.describe_image")
def test_describe_single_image_failure(mock_describe):
    """
    /describe should gracefully report failure (not crash) when the
    vision service raises a ValueError (e.g. malformed model output).
    """
    mock_describe.side_effect = ValueError("Model did not return valid JSON")

    fake_image = b"fake image bytes"
    response = client.post(
        "/describe",
        files={"file": ("bad.jpg", fake_image, "image/jpeg")},
        data={"brand_tone": "professional", "target_keywords": ""},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert "valid JSON" in body["error"]


def test_batch_describe_enforces_max_batch_size():
    """Uploading more files than MAX_BATCH_SIZE should return a 400 error."""
    from app.core.config import settings

    fake_files = [
        ("files", (f"img{i}.jpg", b"fake bytes", "image/jpeg"))
        for i in range(settings.MAX_BATCH_SIZE + 1)
    ]

    response = client.post("/batch-describe", files=fake_files)
    assert response.status_code == 400
    assert "exceeds maximum" in response.json()["detail"]