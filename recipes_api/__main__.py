from aiohttp import web
from .app import app
from .config import SERVER_PORT

web.run_app(app, port=int(SERVER_PORT))
