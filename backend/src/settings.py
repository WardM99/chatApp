"""Settings of the project"""
from environs import Env

env = Env()

DB_NAME: str = env.str("DB_NAME", "database")
