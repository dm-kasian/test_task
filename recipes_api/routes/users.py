from aiohttp import web


users_routes = web.RouteTableDef()


@users_routes.post('/users/register')
async def register(request):
    data = await request.json()
    username = data['username']
    password = data['password']

    await request.app['pg'].fetchrow('INSERT INTO users (username, password) VALUES ($1, $2)', username, password)
    return web.json_response({'status': 'OK'})


@users_routes.post('/users/me')
async def get_me(request):
    data = await request.json()
    username = data['username']
    password = data['password']

    user = await request.app['pg'].fetchrow("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
    if user is None:
        return web.json_response({'status': 'User not found'})

    return web.json_response({'username': user['username']})
