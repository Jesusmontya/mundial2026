# Cache en memoria — se actualiza cada 5 minutos
_cache = {
    "partidos":   [],
    "tabla":      {},
    "goleadores": [],
    "calendario": [],
    "ultimo_update": None
}

def get(key: str):
    return _cache.get(key)

def set(key: str, value):
    _cache[key] = value

def set_update_time(t):
    _cache["ultimo_update"] = t