import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from core.db.tasks import ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('start function on_startup')
    await ensure_indexes()

    yield

    logging.info('end function on_startup')
