from .interface import RecipesProvider
import aiohttp

# API Docs: http://www.recipepuppy.com/about/api/


class RecipePuppy(RecipesProvider):
    # TODO implement search
    async def search(self, query):
        raise NotImplementedError()
