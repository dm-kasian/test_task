import os

SERVER_PORT = os.getenv("SERVER_PORT", "8080")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

REDIS_ADDRESS = os.getenv("REDIS_ADDRESS", "redis://localhost")

MEALDB_APIKEY = os.getenv("MEALDB_APIKEY", "1")
