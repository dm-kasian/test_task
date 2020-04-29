from aiohttp import web
from recipes_api import config
from recipes_api.routes import users, recipes, index
import asyncpg
import aioredis


async def connect_to_postgres(app):
    pg = await asyncpg.create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )
    app['pg'] = pg
    yield
    await pg.close()


async def connect_to_redis(app):
    redis = await aioredis.create_pool(config.REDIS_ADDRESS)
    app['redis'] = redis
    yield
    redis.close()
    await redis.wait_closed()


app = web.Application()
app.add_routes(index.index_routes)
app.add_routes(users.users_routes)
app.add_routes(recipes.recipes_routes)
app.cleanup_ctx.append(connect_to_postgres)
app.cleanup_ctx.append(connect_to_redis)
