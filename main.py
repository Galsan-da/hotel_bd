
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
        title: str | None = Query(default=None, description="Название города"),
        hotel_name: str | None = Query(default=None, description="Название отеля")
):
    hotel_ = [
        hotel for hotel in hotels
        if (id is None or id == hotel['id'])
        and (title is None or title  == hotel['title'])
        and (hotel_name is None or hotel_name == hotel['name'])
        ]
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

@app.put("/hotels/{hotel_id}")
def update_hotels(
    hotels_id: int,
    title: str = Body(default=None, description="Название города"),
    hotel_name: str = Body(default=None, description="Название отеля")
):
    for hotel in hotels:
        if hotel['id'] == hotels_id:
            if title is not None:
                hotel['title'] == title
            if hotel_name is not None:
                hotel['name'] == hotel_name
            return {'status': 'ok'}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)