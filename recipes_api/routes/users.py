import uuid
import bcrypt

from aiohttp import web
from asyncpg.exceptions import UniqueViolationError

users_routes = web.RouteTableDef()


@users_routes.post('/users/register')
async def register(request):
    data = await request.json()
    username = data['username']
    password = data['password'].encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hased_password = hashed.decode('utf-8')
    try:
        await request.app['pg'].fetchrow(
            'INSERT INTO users (username, password) VALUES ($1, $2)', username, hased_password
        )
    #TODO use "if" instead of "try...except"
    except UniqueViolationError as e:
        response = {
            'status': 'ERROR',
            'message': f'User with username "{username}" already exists!'
        }
    else:
        response = {'status': 'OK'}

    return web.json_response(response)


@users_routes.post('/users/me')
async def get_me(request):
    data = await request.json()
    username = data['username']
    password = data['password']
    update = data['update']

    user = await request.app['pg'].fetchrow("SELECT * FROM users WHERE username = $1", username)

    if user is None:
        response = {'status': 'ERROR' , 'message': 'User not found!'}
    elif not bcrypt.checkpw(password.encode(), user.get('password').encode()):
        response = {'status': 'ERROR' , 'message': 'Wrong password!'}
    else:
        response = {'username': user['username']}

    return web.json_response(response)
