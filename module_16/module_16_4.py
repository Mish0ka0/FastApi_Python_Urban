from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from typing import List


app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/users/{username}/{age}")
async def create_user(user: User) -> User:
    new_id = max((n_user.id for n_user in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}/{username}/{age}")
async def update_user(user: User) -> User:
    for i, us in enumerate(users):
        if us.id == user.id:
            us.username = user.username
            us.age = user.age
            return us[i]
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user: User) -> User:
    for i, us in enumerate(users):
        if us.id == user.id:
            del_user = users[i]
            del users[i]
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")
