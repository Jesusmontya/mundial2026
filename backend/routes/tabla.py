from fastapi import APIRouter
import cache

router = APIRouter()

@router.get("/")
async def get_tabla():
    return cache.get("tabla") or {}

@router.get("/{grupo}")
async def get_grupo(grupo: str):
    tabla = cache.get("tabla") or {}
    return tabla.get(grupo.upper(), [])