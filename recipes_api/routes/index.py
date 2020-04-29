from aiohttp import web
import sqlalchemy

index_routes = web.RouteTableDef()

#TODO remove the endpoint
@index_routes.get('')
async def search(request):
    return web.json_response({"status": "OK", "results": "hello"})
