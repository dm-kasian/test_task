import aiohttp
from .interface import RecipesProvider

# API Docs: https://www.themealdb.com/api.php


class Edamam(RecipesProvider):
    base_url = 'https://api.edamam.com/search'

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    async def search(self, query):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}?app_id={self.app_id}&app_key={self.app_key}&q={query}&to={self.limit}'
            async with session.get(url) as resp:
                response = await resp.json()
        return self._prepare_results(response)

    async def search_by_ingredient(self, query):
        # According to API documetation there are not different way to search by ingredients.
        # And the search endpoint works for ingredients as well. 
        return await self.search(query)
        
    @classmethod
    def _prepare_results(cls, response):

        if not response.get('count'):
            return []

        results = []
        for meal in response['hits']:
            recipe = meal['recipe']
            meal_name = recipe['label']
            meal_inst = (
                f'You can find an instruction by the following link: {recipe["url"]}'
            )
            meal_img = recipe['image']
            meal_ingr = recipe['ingredientLines']

            results.append({
                "name": meal_name,
                "instructions": meal_inst,
                "ingredients": meal_ingr,
                "image_url": meal_img
            })
        return results
