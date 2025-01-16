from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated, List


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory='module_16/templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_users(request: Request, user_id: int):
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.post("/user/{username}/{age}")
async def create_user(user: User) -> User:
    new_id = max((n_user.id for n_user in users), default=0) + 1
    new_user = User(id=new_id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
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