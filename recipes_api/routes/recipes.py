from aiohttp import web
    
from recipes_api.config import MEALDB_APIKEY
from recipes_api.integrations.themealdb import TheMealDB
from recipes_api.integrations.recipepuppy import RecipePuppy
from recipes_api.helpers.auth import auth_by_api_key

import json
from aiohttp import web

recipes_routes = web.RouteTableDef()


async def _get_cached_response(app, cache_key):
    redis = app['redis']
    response = await redis.get(cache_key, encoding='utf-8')
    if response:
        return json.loads(response)


async def _set_cached_response(app, cache_key, response, timeout=30):
    redis = app['redis']
    await redis.set(cache_key, json.dumps(response))
    await redis.expire(cache_key, timeout)


@recipes_routes.post('/recipes/search')
@auth_by_api_key
async def search(request):
    data = await request.json()
    query = data['query']

    cache_key = f'{request.path}_{query}' 
    cached_responce = await _get_cached_response(request.app, cache_key)
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
    await _set_cached_response(request.app, cache_key, response)

    return web.json_response(response)