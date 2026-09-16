from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(image_bytes)
    }