import base64
import json

from groq import Groq

from app.core.config import settings
from app.models.schemas import ProductDescription, ProductDescriptionRequest

client = Groq(api_key=settings.GROQ_API_KEY)

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def _encode_image(image_bytes: bytes) -> str:
    """Convert raw image bytes into a base64 string the Groq API can accept."""
    return base64.b64encode(image_bytes).decode("utf-8")


def _build_prompt(request: ProductDescriptionRequest) -> str:
    """
    Construct the instruction prompt that controls tone and keyword injection.
    Kept as a separate function so prompt tuning doesn't require touching
    the API-calling logic.
    """
    keywords_line = (
        f"Naturally incorporate these SEO keywords where relevant: {', '.join(request.target_keywords)}."
        if request.target_keywords
        else "Choose relevant SEO keywords yourself based on what you see in the image."
    )

    return f"""You are an e-commerce copywriting expert. Look at the product image and generate
a complete, SEO-optimized product listing.

Brand tone: {request.brand_tone}. Write consistently in this tone throughout.
{keywords_line}

Respond with ONLY a JSON object matching this exact structure, no other text:
{{
  "title": "string, under 70 characters",
  "short_description": "string, under 160 characters",
  "long_description": "string, 3-5 sentences",
  "bullet_points": ["3-5 short benefit-focused strings"],
  "seo_keywords": ["5-10 relevant keyword strings"],
  "category_guess": "string, best-guess e-commerce category"
}}"""


def describe_image(image_bytes: bytes, request: ProductDescriptionRequest) -> ProductDescription:
    """
    Send a single image to Groq's vision model and return a validated,
    structured ProductDescription.

    Raises:
        ValueError: if the model's response isn't valid JSON matching our schema.
    """
    base64_image = _encode_image(image_bytes)
    prompt = _build_prompt(request)

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
        temperature=0.4,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content

    try:
        parsed = json.loads(raw_content)
        return ProductDescription(**parsed)
    except (json.JSONDecodeError, TypeError) as e:
        raise ValueError(f"Model did not return valid structured JSON: {e}") from e