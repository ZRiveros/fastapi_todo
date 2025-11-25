# import necessary libraries & MongoDB client
from fastapi import FastAPI
from pydantic import BaseModel
from bson import ObjectId # Installera Pymongo för att använda detta
from fastapi import HTTPException
from database import todo_collection


# Create FastAPI instance
app = FastAPI()

# In-memory storage for todo items
items = []

#Basemodel used to define the structure of a todo item
class TodoItem(BaseModel):
    title : str

#Create outputs for the API
class TodoItemOut(TodoItem):
    id: str
    title: str    

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Todo API"}

# Endpoint to create a new todo item
@app.post("/todo", response_model=TodoItemOut)
async def create_item(item: TodoItem):
    result = await todo_collection.insert_one(item.model_dump())
    print(f"Todo added:: {result}")
    saved_item = await todo_collection.find_one({"_id": result.inserted_id})
    return TodoItemOut(
        id=str(saved_item["_id"]),
        title=saved_item["title"]
    )

@app.get("/todo", response_model=list[TodoItemOut])
async def get_all_items():
    todos = []
    cursor = todo_collection.find({})
    async for document in cursor:
        todos.append(TodoItemOut(
            id=str(document["_id"]),
            title=document["title"]
        ))
    return todos

@app.put("/todo/{item_id}", response_model=TodoItemOut)
async def update_item(item_id: str, updated_item: TodoItem):
    #Try and convert item_id to ObjectId
    try:
        obj_id = ObjectId(item_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    result = await todo_collection.update_one(
        {"_id": obj_id},
        {"$set": {"title": updated_item.title}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    saved_item = await todo_collection.find_one({"_id": obj_id})
    print(saved_item)
    return TodoItemOut(
        id=str(saved_item["_id"]),
        title=saved_item["title"]
    )

@app.delete("/todo/{item_id}")
async def delete_item(item_id: str):
    #Delete a todo item by its ID
    try:
        obj_id = ObjectId(item_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid item ID format")
    result = await todo_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    print(f"Deleted item with id: {item_id}")
    return {"message": "Item deleted successfully"}



# To run the app, use the command: # uv run uvicorn main:app --reload
# Make sure to have FastAPI and Uvicorn installed in your environment.
# You can install them using pip:
# pip install fastapi uvicorn
# Then, navigate to http://127.0.0.1:8000/ in your web browser to access the API.

# To add Todo items, you can use tools like Postman or curl to send POST requests to the /todo endpoint with a JSON body containing the title of the todo item.
# CRUD operation works well in swagger UI at http://127.0.0.1:8000/docs which adds all Todo items to MongoDB database.
# Make sure MongoDB server is running locally on default port 27017 before starting the FastAPI app.
# Start the MongoDB server using the command: sudo systemctl start mongod
# Check status - sudo systemctl status mongod
# Start mongo shell - mongosh
# To show all databases - show dbs
# To use a specific database - use <Todo_db>
# to see all collections in the database - show collections
# Get all documents in a collection - db.todos.find().pretty()
# Count all documents in a collection - db.todos.countDocuments()
# To exit mongo shell - exit

# Post - curl -X POST http://127.0.0.1:8000/todos \
# -H "Content-Type: application/json" \
# -d '{"title": "Lära mig FastAPI"}'

# Get - curl http://127.0.0.1:8000/todos

# Get by ID - curl http://127.0.0.1:8000/todos/<id>

# curl -X PUT http://127.0.0.1:8000/todos/<id> \
# -H "Content-Type: application/json" \
# -d '{"title": "Nytt namn"}' 

# Delete - curl -X DELETE http://127.0.0.1:8000/todos/<id>
# Note: Replace <id> with the actual ID of the todo item you want to update or delete.

# 