import json
import asyncio
from aiohttp import web
    
from recipes_api.config import (
    MEALDB_APIKEY,
    EDAMAM_ID,
    EDAMAM_APIKEY
)
from recipes_api.helpers import (
    auth_by_api_key,
    log_requests
)
from recipes_api.integrations.themealdb import TheMealDB
from recipes_api.integrations.recipepuppy import RecipePuppy
from recipes_api.integrations.edamam import Edamam


recipes_routes = web.RouteTableDef()

class SearchCache:
    def __init__(self, request, query):
        self.redis = request.app['redis']
        self.cache_key = f'{request.path}_{query}' 

    async def get(self):
        response = await self.redis.get(self.cache_key, encoding='utf-8')
        if response:
            return json.loads(response)

    async def set(self, response, timeout=30):
        await self.redis.set(self.cache_key, json.dumps(response))
        await self.redis.expire(self.cache_key, timeout)


@recipes_routes.post('/recipes/search')
@auth_by_api_key
@log_requests
async def search(request):
    data = await request.json()
    query = data.get('query')
    if query is None:
        raise web.HTTPBadRequest(text='"query" key is required!')

    _cache = SearchCache(request, query)

    cached_responce = await _cache.get()
    if cached_responce:
        return web.json_response(cached_responce)

    themealdb_results = TheMealDB(api_key=MEALDB_APIKEY).search(query=query)
    recipepuppy_results = RecipePuppy().search(query=query)
    edamam_results = Edamam(app_id=EDAMAM_ID, app_key=EDAMAM_APIKEY).search(query=query)
    results = await asyncio.gather(themealdb_results, recipepuppy_results, edamam_results)

    response = {
        "status": "OK", 
        "themealdb_results": results[0],
        'recipepuppy_results': results[1],
        'edamam_results': results[2]
    }
    await _cache.set(response)

    return web.json_response(response)


@recipes_routes.post('/recipes/search-ingr')
@auth_by_api_key
async def search_by_ingredient(request):
    data = await request.json()
    query = data.get('query')
    if query is None:
        raise web.HTTPBadRequest(text='"query" key is required!')
    _cache = SearchCache(request, query)

    cached_responce = await _cache.get()
    if cached_responce:
        return web.json_response(cached_responce)

    themealdb_results = TheMealDB(api_key=MEALDB_APIKEY).search_by_ingredient(query=query)
    recipepuppy_results = RecipePuppy().search_by_ingredient(query=query)
    edamam_results = Edamam(app_id=EDAMAM_ID, app_key=EDAMAM_APIKEY).search_by_ingredient(query=query)
    results = await asyncio.gather(themealdb_results, recipepuppy_results, edamam_results)

    response = {
        "status": "OK", 
        "themealdb_results": results[0],
        'recipepuppy_results': results[1],
        'edamam_results': results[2]
    }
    await _cache.set(response)

    return web.json_response(response)
