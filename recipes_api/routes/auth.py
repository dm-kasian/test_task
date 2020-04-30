import functools
from aiohttp import web

def auth_by_api_key(func):
    @functools.wraps(func)
    async def check(request):
        api_key = request.query.get('apikey')
        if api_key:
            user = await request.app['pg'].fetchrow(
                "SELECT * FROM users WHERE api_key = $1", api_key
            )
            
        if not api_key or user is None:
            raise web.HTTPForbidden
        return await func(request)
    return check
