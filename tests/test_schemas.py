import pytest
from pydantic import ValidationError

from app.models.schemas import (
    BatchResponse,
    BatchResult,
    ProductDescription,
    ProductDescriptionRequest,
)


def test_product_description_request_defaults():
    """Default brand_tone should be 'professional' and keywords should default to empty list."""
    request = ProductDescriptionRequest()
    assert request.brand_tone == "professional"
    assert request.target_keywords == []


def test_product_description_request_rejects_invalid_tone():
    """An invalid brand_tone value must be rejected by Pydantic validation."""
    with pytest.raises(ValidationError):
        ProductDescriptionRequest(brand_tone="sarcastic")


def test_product_description_valid_payload():
    """A fully valid payload should construct successfully."""
    desc = ProductDescription(
        title="Test Product",
        short_description="A short hook.",
        long_description="A longer description of the product.",
        bullet_points=["Point one", "Point two"],
        seo_keywords=["keyword1", "keyword2"],
        category_guess="Test Category",
    )
    assert desc.title == "Test Product"
    assert len(desc.bullet_points) == 2


def test_product_description_missing_required_field():
    """Missing a required field (title) should raise a validation error."""
    with pytest.raises(ValidationError):
        ProductDescription(
            short_description="A short hook.",
            long_description="A longer description.",
            bullet_points=["Point one"],
            seo_keywords=["keyword1"],
            category_guess="Test Category",
        )


def test_batch_result_failure_case():
    """A failed BatchResult should allow description to be None while error is set."""
    result = BatchResult(filename="bad.jpg", success=False, description=None, error="Invalid image")
    assert result.success is False
    assert result.description is None
    assert result.error == "Invalid image"


def test_batch_response_aggregates_correctly():
    """BatchResponse should hold a list of mixed success/failure results."""
    results = [
        BatchResult(filename="a.jpg", success=True, description=None, error=None),
        BatchResult(filename="b.jpg", success=False, description=None, error="failed"),
    ]
    response = BatchResponse(total=2, succeeded=1, failed=1, results=results)
    assert response.total == 2
    assert len(response.results) == 2
    