#openfood.py
import httpx

async def buscar_alimentos_openfood(query: str, limit: int =10):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    resultados = []
    for p in data.get("products", []):
        if not all(k in p for k in ("product_name", "nutriments")):
            continue
        nutr = p["nutriments"]
        resultados.append({
            "nombre": p.get("product_name", ""),
            "kcal": nutr.get("energy-kcal_100g", 0),
            "proteinas": nutr.get("proteins_100g", 0),
            "carbohidratos": nutr.get("carbohydrates_100g", 0),
            "grasas": nutr.get("fat_100g", 0),
            "fibra": nutr.get("fiber_100g", 0),
            "imagen_url": p.get("image_front_url"),
            "codigo_barras": p.get("code"),
        })

    return resultados
