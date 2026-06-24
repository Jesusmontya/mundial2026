import httpx
import os
from datetime import datetime
from dotenv import load_dotenv
import cache

load_dotenv()

API_KEY = os.getenv("FOOTBALL_DATA_KEY")
API_URL = os.getenv("FOOTBALL_DATA_URL")
WC = "WC"

HEADERS = {
    "X-Auth-Token": API_KEY
}

async def fetch(endpoint: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/{endpoint}", headers=HEADERS)
        r.raise_for_status()
        return r.json()

async def actualizar_cache():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Actualizando cache...")
    try:
        await _cargar_partidos()
        await _cargar_tabla()
        await _cargar_goleadores()
        await _cargar_calendario()
        cache.set_update_time(datetime.now().isoformat())
        print("✓ Cache actualizado")
    except Exception as e:
        print(f"✗ Error: {e}")

async def _cargar_partidos():
    data = await fetch(f"competitions/{WC}/matches?status=FINISHED")
    partidos = []
    for m in data.get("matches", []):
        partidos.append({
            "id":        m["id"],
            "fecha":     m["utcDate"],
            "fase":      m["stage"],
            "grupo":     m.get("group"),
            "local":     m["homeTeam"]["name"],
            "visitante": m["awayTeam"]["name"],
            "escudo_l":  m["homeTeam"].get("crest"),
            "escudo_v":  m["awayTeam"].get("crest"),
            "goles_l":   m["score"]["fullTime"]["home"],
            "goles_v":   m["score"]["fullTime"]["away"],
            "estado":    m["status"],
        })
    cache.set("partidos", partidos)

async def _cargar_tabla():
    data = await fetch(f"competitions/{WC}/standings")
    tabla = {}
    for grupo in data.get("standings", []):
        nombre = grupo["group"]
        tabla[nombre] = []
        for eq in grupo["table"]:
            tabla[nombre].append({
                "pos":    eq["position"],
                "equipo": eq["team"]["name"],
                "escudo": eq["team"].get("crest"),
                "pj":     eq["playedGames"],
                "g":      eq["won"],
                "e":      eq["draw"],
                "p":      eq["lost"],
                "gf":     eq["goalsFor"],
                "gc":     eq["goalsAgainst"],
                "dif":    eq["goalDifference"],
                "pts":    eq["points"],
            })
    cache.set("tabla", tabla)

async def _cargar_goleadores():
    data = await fetch(f"competitions/{WC}/scorers?limit=10")
    goleadores = []
    for s in data.get("scorers", []):
        goleadores.append({
            "nombre":   s["player"]["name"],
            "pais":     s["team"]["name"],
            "escudo":   s["team"].get("crest"),
            "goles":    s["goals"],
            "partidos": s.get("playedMatches"),
        })
    cache.set("goleadores", goleadores)

async def _cargar_calendario():
    data = await fetch(f"competitions/{WC}/matches?status=SCHEDULED")
    calendario = []
    for m in data.get("matches", [])[:20]:
        calendario.append({
            "id":        m["id"],
            "fecha":     m["utcDate"],
            "fase":      m["stage"],
            "grupo":     m.get("group"),
            "local":     m["homeTeam"]["name"],
            "visitante": m["awayTeam"]["name"],
            "escudo_l":  m["homeTeam"].get("crest"),
            "escudo_v":  m["awayTeam"].get("crest"),
        })
    cache.set("calendario", calendario)