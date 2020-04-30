import functools
from datetime import datetime
from aiohttp import web

__all__ = ['log_requests']


def log_requests(func):
    @functools.wraps(func)
    async def wrap(request):
        api_key = request.query.get('apikey')
        if not api_key:
            return await func(request)

        user = await request.app['pg'].fetchrow(
            "SELECT * FROM users WHERE api_key = $1", api_key
        )
        if user:
            data = await request.json()
            query = data['query']
            await request.app['pg'].fetchrow(
                'INSERT INTO recipes_search_logs (user_id, query, request_datetime) VALUES ($1, $2, $3)', 
                user.get('id'), query, datetime.utcnow()
            )
        return await func(request)

    return wrap
