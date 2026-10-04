from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from routes import base_router, data_router
from helpers import db, get_settings, Settings, DB
from motor.motor_asyncio import AsyncIOMotorClient
    
# 1. Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup Logic ----
    app.mongo_conn = AsyncIOMotorClient(get_settings().mongodb_uri)
    app.mongo_db = app.mongo_conn[get_settings().mongodb_db_name]
    
    yield  # The app runs and processes requests while sitting here
    # Close the connection when the app is shutting down
    app.mongo_conn.close()  
    # ---- Shutdown Logic ----
    await app.state.db_client.disconnect()

# 2. Pass the lifespan function to your FastAPI instance
app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(data_router)
