#database MongoDB connection setup
from motor.motor_asyncio import AsyncIOMotorClient

# 1. URL till MongodB-servern
MONGO_URL = "mongodb://localhost:27017"

# 2. Skapa en asynkron MongoDB-klient
client = AsyncIOMotorClient(MONGO_URL)

# 3. Välj databas
database = client.todo_db

# 4. Välj samling
todo_collection = database.todos