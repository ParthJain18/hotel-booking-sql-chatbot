from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(tags=["Health"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}