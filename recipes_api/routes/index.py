import sqlalchemy

from aiohttp import web
from recipes_api.helpers.auth import auth_by_api_key

index_routes = web.RouteTableDef()

#TODO remove the endpoint
@index_routes.get('')
@auth_by_api_key
async def index(request):
    return web.json_response({"status": "OK", "results": "hello"})
