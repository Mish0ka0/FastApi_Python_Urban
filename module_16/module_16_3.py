from fastapi import FastAPI, HTTPException, Path
from typing import Annotated


app = FastAPI()

users = {"1": "Имя: Example, Возраст: 18"}


@app.get("/user")
async def get_users() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=4,
                                      max_length=20,
                                      description='Enter username',
                                      example='NewUser')],
        age: Annotated[int, Path(ge=18,
                                 le=100,
                                 description='Enter age',
                                 example='24'
                                 )]) -> str:
    new_id = max(int(user) for user in users.keys()) + 1 if users else 1
    users.update({str(new_id): f'Имя: {username}, Возраст: {age}'})
    return f'User {new_id} is registered'


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path(ge=1,
                                     le=10,
                                     description='Enter user_id',
                                     example=1)],
        username: Annotated[str, Path(min_length=4,
                                      max_length=20,
                                      description='Enter username',
                                      example='NewUser')],
        age: Annotated[int, Path(ge=18,
                                 le=100,
                                 description='Enter age',
                                 example='24'
                                 )]) -> str:
    for user_k in users.keys():
        if user_k == str(user_id):
            users[user_k] = f'Имя: {username}, Возраст: {age}'
            return f'The user {user_id} is update'
    raise HTTPException(status_code=404, detail='Пользователь не найден')


@app.delete("/user/{user_id}")
async def delete_user(
        user_id: Annotated[int, Path(ge=1,
                                     le=10,
                                     description='Enter user_id',
                                     example=1
                                     )]) -> str:
    for user_k in users.keys():
        if user_k == str(user_id):
            del users[user_k]
            return f'User {user_id} is deleted'
    raise HTTPException(status_code=404, detail='Пользователь не найден')
