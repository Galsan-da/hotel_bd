
from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI() #создаем экземпляр приложения

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi', },
    {'id': 2, 'title': 'Moscow', 'name': 'moscow', },
    {'id': 3, 'title': 'New York', 'name': 'New York', },
]
@app.get("/hotels")
def get_hotel(
        id: int | None = Query(default=None, description="ID города"),
        title: str | None = Query(default=None, description="Название города")
):
    ct = [city for city in data_db if id == city['id'] or title == city['title']]
    return ct
@app.delete("/hotels/{hotels_id}")
def delete_hotel(hotels_id: int):
    global data_db
    data_db = [hotel for hotel in data_db if hotels_id != hotel['id']]
    return {'status': 'ok'}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)