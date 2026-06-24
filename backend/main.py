from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from routes import partidos, tabla, goleadores, calendario
from services.football_api import actualizar_cache

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar: carga datos y programa actualizaciones cada 5 min
    await actualizar_cache()
    scheduler.add_job(actualizar_cache, "interval", minutes=5)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="Mundial 2026 API",
    description="Datos en tiempo real del Mundial 2026",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(partidos.router,   prefix="/api/partidos",   tags=["Partidos"])
app.include_router(tabla.router,      prefix="/api/tabla",      tags=["Tabla"])
app.include_router(goleadores.router, prefix="/api/goleadores", tags=["Goleadores"])
app.include_router(calendario.router, prefix="/api/calendario", tags=["Calendario"])

@app.get("/")
async def root():
    return {"status": "ok", "mensaje": "Mundial 2026 API corriendo"}