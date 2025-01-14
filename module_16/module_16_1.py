from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main_page() -> str:  # статичный маршрут
    return "Главная страница"


@app.get("/user/admin")
async def admin_panel() -> str:  # статичный маршрут
    return "Вы вошли как администратор"


@app.get("/user/{user_id}")
async def user_number(user_id: int) -> str:  # динамический машрут с параметром в пути
    return f'Вы вошли как пользователь № {user_id}'


@app.get("/user")
async def user_info(username: str, age: int) -> str:  # динамический маршрут с параметрами запроса(query parameters)
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
