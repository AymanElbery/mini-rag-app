from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings, Settings

class DB:
    def __init__(self):
        self.client = AsyncIOMotorClient()
        self.settings: Settings = get_settings()
        
    async def connect(self):
        #await self.client.connect()
        return self.client(self.settings.mongodb_uri)
    async def disconnect(self):
        #await self.client.disconnect()
        print("Disconnected from motors.")