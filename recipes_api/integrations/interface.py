
class RecipesProvider:
    """
        Search recipes
        :param query: The recipe query
        :return: list of recipes of the format
        [{
            "name": "recipe name",
            "instructions": "Instructions",
            "ingredients": ["ingredient1", "ingredient2"],
            "image_url": "http://site.com/image-of-recipe.jpg"
        }]
    """
    async def search(self, query):
        raise NotImplementedError()
