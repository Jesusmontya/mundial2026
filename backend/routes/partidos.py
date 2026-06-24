from fastapi import APIRouter
import cache

router = APIRouter()

@router.get("/")
async def get_partidos():
    return cache.get("partidos") or []

@router.get("/hoy")
async def get_hoy():
    from datetime import date
    hoy = date.today().isoformat()
    partidos = cache.get("partidos") or []
    return [p for p in partidos if p["fecha"].startswith(hoy)]