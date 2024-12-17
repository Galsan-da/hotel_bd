from fastapi import FastAPI, Query, Body
import uvicorn
app = FastAPI()  # создаем экземпляр приложения
data_db = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi', },
    {'id': 2, 'title': 'Moscow', 'name': 'moscow', },
    {'id': 3, 'title': 'Ufa', 'name': 'ufa', },
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
def update_hotel(data_db: list,
                 hotel_id: int,
                 title: str,
                 name: str):
    for data in data_db:
        if data['id'] == hotel_id:
            if data['title'] is not None:
                data['title'] = title
            if data['name'] is not None:
                data['name'] = name
            return {"status": "ok"}
        return {"error": "all fields are required"}
@app.put("/hotels/{hotels_id}")
def create_hotel_put(
        hotels_id: int,
        title: str = Query(description='Название города'),
        name: str = Query(description='какой-то идентификатор')
):
    global data_db
    return update_hotel(data_db, hotels_id, title, name)
@app.patch("/hotels/{hotels_id}")
def create_hotel_patch(
        hotels_id: int,
        title: str | None = Query(description='Название города'),
        name: str | None = Query(description='какой-то идентификатор')
):
    return update_hotel(data_db, hotels_id, title, name)
@app.post('/hotels')
def create_hotel(
        title: str = Body(embed=True, description="Название города")
):
    data_db.append(
        {'id': data_db[-1]['id'] + 1,
         'title': title}
    )
    return {"status": "ok"}
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)