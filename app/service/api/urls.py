from fastapi import APIRouter, Response, status
from .v1 import router as v1_router

router = APIRouter(
    prefix='/api'
)

router.include_router(v1_router)


@router.get('/health-check/')
async def health_check():
    return Response(status_code=status.HTTP_200_OK)
