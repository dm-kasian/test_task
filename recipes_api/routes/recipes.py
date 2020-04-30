import json
from aiohttp import web
    
from recipes_api.config import MEALDB_APIKEY
from recipes_api.integrations.themealdb import TheMealDB
from recipes_api.integrations.recipepuppy import RecipePuppy
from recipes_api.helpers import auth_by_api_key, log_requests


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
    query = data['query']
    _cache = SearchCache(request, query)

    cached_responce = await _cache.get()
    if cached_responce:
        return web.json_response(cached_responce)

    themealdb_results = await TheMealDB(api_key=MEALDB_APIKEY).search(query=query)
    #TODO aks about preferrences way to merge
    recipepuppy_results = await RecipePuppy().search(query=query)   

    response = {
        "status": "OK", 
        "themealdb_results": themealdb_results,
        'recipepuppy_results': recipepuppy_results
    }
    await _cache.set(response)

    return web.json_response(response)