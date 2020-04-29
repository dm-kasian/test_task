from aiohttp import web
from recipes_api.config import MEALDB_APIKEY
from recipes_api.integrations.themealdb import TheMealDB


recipes_routes = web.RouteTableDef()


@recipes_routes.post('/recipes/search')
async def search(request):
    data = await request.json()
    query = data['query']

    themealdb_results = await TheMealDB(api_key=MEALDB_APIKEY).search(query=query)

    # TODO: Implement RecipePuppy API and merge results
    # recipepuppy_results = await RecipePuppy().search(query=query)

    return web.json_response({"status": "OK", "results": themealdb_results})
