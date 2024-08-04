import logging
from core.db.session import session
from pymongo import ASCENDING


async def ensure_indexes():
    indexes = await session.users.index_information()
    if 'telegram_id_1' not in indexes:
        await session.users.create_index([("telegram_id", ASCENDING)], unique=True)
        logging.info('Index telegram_id created')
