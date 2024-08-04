# from pymongo.server_api import ServerApi
from core import Config
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(Config.MONGO_DB_URL)  # , server_api=ServerApi('1'))

session = client[Config.MD_DB]
