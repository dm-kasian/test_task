import json 
import aiohttp
from .interface import RecipesProvider

# API Docs: http://www.recipepuppy.com/about/api/


class RecipePuppy(RecipesProvider):
    base_url = 'http://www.recipepuppy.com/api/'

    # TODO ask about instruction
    async def search(self, query):
        async with aiohttp.ClientSession() as session:
            url = self.base_url + '?q=' + query
            async with session.get(url) as resp:
                response = await resp.read()
        response = json.loads(response)
        if response['results'] is None:
            return []
        results = []

        for meal in response['results'][:self.limit]:
            meal_name = meal['title']
            #TODO maybe to fix
            meal_inst = (
                f'You can find an instruction by the following link: {meal["href"]}'
            )
            meal_img = meal['thumbnail']
            meal_ingr = [i.strip() for i in meal['ingredients'].split(',')]

            results.append({
                "name": meal_name,
                "instructions": meal_inst,
                "ingredients": meal_ingr,
                "image_url": meal_img
            })
        return results
