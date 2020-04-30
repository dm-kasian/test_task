# import functools
# import pickle
# from aiohttp import web

# def cache(timeout=60):
#     def decorator(func):
#         @functools.wraps(func)
#         async def wraper(request):
#             resid = request.app['redis']
#             key = request.rel_url
#             cached_
#             response = await func(request)
#             if response.status = 200:
#                 serialized_response = pickle.dumps(response)

#             return response
#         return wraper
#     return decorator

#TODO remove it