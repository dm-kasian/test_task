from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    BigInteger,
    DateTime
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("username", String(128), unique=True, nullable=False),
    Column("password", String(128), nullable=False),
    Column('api_key', String(36), unique=True, nullable=False)
)

recipes_search_logs = Table(
    "recipes_search_logs",
    metadata,
    Column("id", BigInteger, primary_key=True),
    Column("user_id", BigInteger, nullable=False),
    Column("query", String(128), nullable=False),
    Column("request_datetime", DateTime, nullable=False)
)
