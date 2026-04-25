from fastapi import APIRouter

from .groups import *

__all__ = ["v1_router"]


v1_router = APIRouter()

v1_router.include_router(groups_router)
