import uuid
import bcrypt

from aiohttp import web
from asyncpg.exceptions import UniqueViolationError

users_routes = web.RouteTableDef()

def validate_body(data):
    return data.get('username') and data.get('password')

@users_routes.post('/users/register')
async def register(request):
    data = await request.json()
    if not validate_body(data):
        raise web.HTTPBadRequest(text='"username" and "password" keys are required!')

    username = data['username']
    password = data['password'].encode()

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    hased_password = hashed.decode('utf-8')
    api_key = str(uuid.uuid4())
    try:
        await request.app['pg'].fetchrow(
            'INSERT INTO users (username, password, api_key) VALUES ($1, $2, $3)', 
            username, hased_password, api_key
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
    if not validate_body(data):
        raise web.HTTPBadRequest(text='"username" and "password" keys are required!')

    username = data['username']
    password = data['password']

    user = await request.app['pg'].fetchrow("SELECT * FROM users WHERE username = $1", username)

    if user is None:
        response = {'status': 'ERROR' , 'message': 'User not found!'}
    elif not bcrypt.checkpw(password.encode(), user.get('password').encode()):
        response = {'status': 'ERROR' , 'message': 'Wrong password!'}
    else:
        response = {'api_key': user.get('api_key')}

    return web.json_response(response)
