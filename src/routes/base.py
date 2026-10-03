from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["Base"]
)

@base_router.get("/health-check")
async def health_check(app_settings: Settings = Depends(get_settings)):
    
    return {
        "app_name": app_settings.app_name,
        "app_version": app_settings.app_version,
    }
