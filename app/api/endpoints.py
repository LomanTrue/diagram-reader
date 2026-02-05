from fastapi import APIRouter, UploadFile, File
from app.pipeline.pipeline import process_image
from app.schemas.diagram import DiagramResponse

router = APIRouter(prefix="/api")

@router.post("/analyze", response_model=DiagramResponse)
async def analyze_diagram(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = process_image(image_bytes)
    return result
