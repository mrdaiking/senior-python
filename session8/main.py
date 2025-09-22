from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True


class Status(BaseModel):
    status: str
    detail: str | None = None
    

# In-memory database
users: List[User] = []

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/users/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def list_users():
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated: User):
    for idx, user in enumerate(users):
        if user.id == user_id:
            users[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(users):
        if user.id == user_id:
            users.pop(idx)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/users/active", response_model=List[User])
def get_active_users():
    return [user for user in users if user.is_active]
