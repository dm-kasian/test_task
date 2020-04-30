from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    BigInteger
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
