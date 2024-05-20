from fastapi import APIRouter

from .v1.data import router as data_router
from .v1.transaction import router as transaction_router

v1 = APIRouter(prefix="/v1")
v1.include_router(data_router)
v1.include_router(transaction_router)
