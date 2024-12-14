
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
    hotel_ = [city for city in hotels if id == city['id'] or title == city['title']]
    return hotel_
# Query параметр используется для сортировки и  пагинации

@app.delete("/hotels/{hotels_id}")
def delete_hotel(hotels_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotels_id != hotel['id']]
    return {'status': 'ok'}

@app.post("/hotels")
def create_hotel(
    title: str = Body(),
    name: str = Body()
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {'status': 'ok'}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)