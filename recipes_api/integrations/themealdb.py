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
        return self._prepare_results(response)


    async def search_by_ingredient(self, query):
        # Actually in this case it is a filter.

        # Get only first one, because: filter by multi-ingredient (only available to $2+ Patreon supporters) (from: https://www.themealdb.com/api.php)
        ingredient = query.split(',')[0] 

        #TODO refactor it!!!
        async with aiohttp.ClientSession() as session:
            url = self.base_url + self.api_key + '/filter.php?i=' + ingredient
            details_url = self.base_url + self.api_key + '/lookup.php?i='
            async with session.get(url) as resp:
                general_info_response = await resp.json()
                meals =  general_info_response['meals']

            response = {'meals': []}
            if meals:
                for meal in general_info_response['meals'][:self.limit]:
                    url = details_url + meal['idMeal']
                    async with session.get(url) as resp:
                        meal_details = await resp.json()
                        response['meals'].append(meal_details['meals'][0])
        return self._prepare_results(response)

    @classmethod
    def _prepare_results(cls, response):
        if response['meals'] is None:
            return []

        results = []
        for meal in response['meals'][:cls.limit]:
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
