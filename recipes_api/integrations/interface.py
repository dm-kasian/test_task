
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
    base_url = ''
    #TODO ask about 5 items limit (1-st task)
    limit = 5

    async def search(self, query):
        raise NotImplementedError()
