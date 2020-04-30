import aiohttp
from .interface import RecipesProvider

# API Docs: https://www.themealdb.com/api.php


class TheMealDB(RecipesProvider):
    base_url = 'https://www.themealdb.com/api/json/v1/'

    def __init__(self, api_key):
        self.api_key = api_key

    async def search(self, query):
        async with aiohttp.ClientSession() as session:
            url = self.base_url + self.api_key + '/search.php?s=' + query
            async with session.get(url) as resp:
                response = await resp.json()

        if response['meals'] is None:
            return []

        results = []
        for meal in response['meals']:
            meal_name = meal['strMeal']
            meal_inst = meal['strInstructions']
            meal_img = meal['strMealThumb']
            meal_ingr = []
            for i in range(1, 21):
                ing_value = meal.get('strIngredient' + str(i))
                if ing_value:
                    meal_ingr.append(ing_value)

            results.append({
                "name": meal_name,
                "instructions": meal_inst,
                "ingredients": meal_ingr,
                "image_url": meal_img
            })
        return results
