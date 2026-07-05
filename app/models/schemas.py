from pydantic import BaseModel, Field
from typing import Literal


class ProductDescriptionRequest(BaseModel):
    """Input parameters controlling how the description is generated."""

    brand_tone: Literal["professional", "playful", "luxury", "casual", "technical"] = Field(
        default="professional",
        description="The tone/voice to apply to the generated copy."
    )
    target_keywords: list[str] = Field(
        default_factory=list,
        description="SEO keywords that should be naturally injected into the output."
    )


class ProductDescription(BaseModel):
    """Structured, SEO-optimized product description generated from an image."""

    title: str = Field(description="SEO-friendly product title, under 70 characters.")
    short_description: str = Field(description="1-2 sentence hook, under 160 characters (meta-description length).")
    long_description: str = Field(description="Full marketing description, 3-5 sentences.")
    bullet_points: list[str] = Field(description="3-5 key selling points, scannable, benefit-focused.")
    seo_keywords: list[str] = Field(description="5-10 SEO keywords/phrases relevant to the product.")
    category_guess: str = Field(description="Best-guess e-commerce category for this product.")


class BatchResult(BaseModel):
    """Result for a single image within a batch job."""

    filename: str
    success: bool
    description: ProductDescription | None = None
    error: str | None = None


class BatchResponse(BaseModel):
    """Response for a full batch of processed images."""

    total: int
    succeeded: int
    failed: int
    results: list[BatchResult]