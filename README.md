# Recipes API

### Description

Recipes API is a recipes aggregator service providing recipes from all around the internet in one place.  
The service is not yet completed.  
Your task is to extend the code basis for more features.

### System Requirements
- Python 3.7: https://www.python.org/downloads/release/python-377/
- PostgresSQL 11: https://www.postgresql.org/download/
- Redis: https://redis.io/download

### Python libraries
- [`aiohttp`](https://docs.aiohttp.org/en/stable/index.html) - Web server and HTTP client
- [`asyncpg`](https://magicstack.github.io/asyncpg/current/) - PostgreSQL access
- [`aioredis`](https://aioredis.readthedocs.io/en/v1.3.1/) - Redis access
- [`alembic`](https://alembic.sqlalchemy.org/en/latest/), [`sqlalchemy`](https://docs.sqlalchemy.org/en/13/) - Database migrations

### Notes
- All requests and responses are JSON formatted
- Application configs are read from the OS environment. check `config.py` file
- SQLAlchemy database schema is defined in `schema.py` file
- To run database migrations `alembic upgrade head`
- To run the server `python -m recipes_api`
- This package is using [`pypoetry`](https://python-poetry.org/) for package management. But a `requirements.txt` file is also present for other tools usage

### Tasks

1. Complete the `search` function for `RecipePuppy` recipes provider and merge its results in `/recipes/search` endpoint  
**Make sure to get the first 5 recipes for each search**  
API Docs: http://www.recipepuppy.com/about/api/

2. Add API keys for users, each user should have a random API key generated for him on registration,  
Add the key to the `/users/me` endpoint response

3. Add an API key authorization to `recipes/search` endpoint, the key needs to be provided as `apikey` parameter in the request query string  
**Implement this with mind of future endpoints also needing key authorization**

4. Add basic time-based caching mechanism for the recipes results using Redis

5. Log API requests to the `recipes/search` endpoint in to a new PostgresSQL table. the log should contain the user ID, the query he searched for and the time of request.

6. Add integration of a new recipes provider: EDAMAM  
API Docs: https://developer.edamam.com/edamam-docs-recipe-api  
Developer Key Registration: https://developer.edamam.com/edamam-recipe-api  
**This provider does not return the recipe instructions, so return them as `None` in the API**

7. Create new route `/recipes/search-ingr`, it should be exactly like the `/recipes/search` route, only searching
recipes by an ingredient instead of name.  
**Update the recipes provider interface to include a new search_by_ingredient function and implement it for all providers.**  
**Make sure to add API key authorization for this endpoint too.**

8. Fix any security/performance issues you might find

9. Upload the completed project to any public git websites (e.g. GitHub, GitLab)