from fastapi import APIRouter
import cache

router = APIRouter()

@router.get("/")
async def get_calendario():
    return cache.get("calendario") or []