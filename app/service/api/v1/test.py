from fastapi import APIRouter
from core.celery import app

router = APIRouter(
    prefix='/test'
)


@router.get('/')
async def test():
    print(app.conf.beat_schedule)
