from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.config import settings
from app.models.schemas import BatchResponse, BatchResult, ProductDescriptionRequest
from app.services.vision_service import describe_image

router = APIRouter()


@router.get("/health")
def health_check():
    """Simple liveness check — used by Docker/CI/deployment platforms to confirm the app is up."""
    return {"status": "ok"}


@router.post("/describe", response_model=BatchResult)
async def describe_single_image(
    file: UploadFile = File(...),
    brand_tone: str = Form(default="professional"),
    target_keywords: str = Form(default=""),
):
    """
    Generate an SEO-optimized product description for a single uploaded image.
    target_keywords should be a comma-separated string, e.g. "shoes,running,comfort".
    """
    keywords_list = [k.strip() for k in target_keywords.split(",") if k.strip()]
    request = ProductDescriptionRequest(brand_tone=brand_tone, target_keywords=keywords_list)

    image_bytes = await file.read()

    try:
        description = describe_image(image_bytes, request)
        return BatchResult(filename=file.filename, success=True, description=description)
    except ValueError as e:
        return BatchResult(filename=file.filename, success=False, error=str(e))


@router.post("/batch-describe", response_model=BatchResponse)
async def describe_batch(
    files: list[UploadFile] = File(...),
    brand_tone: str = Form(default="professional"),
    target_keywords: str = Form(default=""),
):
    """
    Generate SEO-optimized product descriptions for multiple images in one request.
    Enforces MAX_BATCH_SIZE to prevent abuse of the free-tier API quota.
    """
    if len(files) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size {len(files)} exceeds maximum of {settings.MAX_BATCH_SIZE}."
        )

    keywords_list = [k.strip() for k in target_keywords.split(",") if k.strip()]
    request = ProductDescriptionRequest(brand_tone=brand_tone, target_keywords=keywords_list)

    results: list[BatchResult] = []

    for file in files:
        image_bytes = await file.read()
        try:
            description = describe_image(image_bytes, request)
            results.append(BatchResult(filename=file.filename, success=True, description=description))
        except ValueError as e:
            results.append(BatchResult(filename=file.filename, success=False, error=str(e)))

    succeeded = sum(1 for r in results if r.success)
    return BatchResponse(
        total=len(results),
        succeeded=succeeded,
        failed=len(results) - succeeded,
        results=results,
    )