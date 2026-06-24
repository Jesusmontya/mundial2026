from fastapi import APIRouter
import cache

router = APIRouter()

@router.get("/")
async def get_goleadores():
    return cache.get("goleadores") or []