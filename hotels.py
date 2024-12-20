from fastapi import Query, HTTPException, APIRouter

from src.hotels import Hotel, HotelPATCH
from src.dependencies import PaginationDep

# Создаем экземпляр FastAPI приложения
router = APIRouter(prefix="/hotels", tags=["Отели"])

# Список отелей для демонстрационных целей
hotels = [
    {'id': 1, 'title': 'Sochi', 'hotel_name': 'sochi'},
    {'id': 2, 'title': 'Moscow', 'hotel_name': 'moscow'},
    {'id': 3, 'title': 'New York', 'hotel_name': 'New York'},
    {'id': 4, 'title': 'Saint-Petersburg', 'hotel_name': 'saint-Petersburg'},
    {'id': 5, 'title': 'Ulan-ude', 'hotel_name': 'ulan-ude'},
    {'id': 6, 'title': 'Irkutsk', 'hotel_name': 'irkutsk'},
    {'id': 7, 'title': 'Tomsk', 'hotel_name': 'tomsk'}
]

@router.get("")
def get_hotel(
        id: int | None = Query(default=None, description="ID города"),
        title: str | None = Query(default=None, description="Название города"),
        hotel_name: str | None = Query(default=None, description="Название отеля")
):
    """
    Получить список отелей с фильтрацией по ID, названию города и названию отеля.

    :param id: ID города (необязательный параметр)
    :param title: Название города (необязательный параметр)
    :param hotel_name: Название отеля (необязательный параметр)
    :return: Список отелей, соответствующих заданным параметрам
    """
    hotel_ = [
        hotel for hotel in hotels
        if (id is None or id == hotel['id']) and
           (title is None or title == hotel['title']) and
           (hotel_name is None or hotel_name == hotel['name'])
    ]
    return hotel_  # Возвращаем отфильтрованный список отелей

@router.delete("/{hotels_id}")
def delete_hotel(hotels_id: int):
    """
    Удалить отель по ID.

    :param hotels_id: ID отеля, который нужно удалить
    :return: Статус операции
    """
    global hotels
    hotels = [hotel for hotel in hotels if hotels_id != hotel['id']]
    return {'status': 'ok'}

@router.post("")
def create_hotel(hotel_data: Hotel):
    """
    Создать новый отель.

    :param title: Название города
    :param name: Название отеля
    :return: Статус операции
    """
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,  # Устанавливаем ID как последний ID + 1
        "title": hotel_data.title,
        "name": hotel_data.hotel_name
    })
    return {'status': 'ok'}

@router.put("/{hotel_id}")
def create_update(
    hotel_id: int,
    hotel_data: Hotel
):
    """
    Полное обновление отеля по ID.

    :param hotel_id: ID отеля, который нужно обновить
    :param title: Новое название города (опционально)
    :param hotel_name: Новое название отеля (опционально)
    :return: Сообщение об успешном обновлении или ошибка
    """
    global hotels
    # Ищем отель по ID
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.hotel_name is not None:
                hotel['name'] = hotel_data.hotel_name
            return {"message": "Обновление прошло успешно", "hotel": hotel}  # Возвращаем обновленный отель

    # Если отель не найден, возвращаем ошибку
    raise HTTPException(status_code=404, detail="Отель не найден")

@router.patch("/{hotel_id}")
def create_patch(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    """
    Частичное обновление отеля по ID.

    :param hotel_id: ID отеля, который нужно обновить
    :param title: Новое название города (опционально)
    :param hotel_name: Новое название отеля (опционально)
    :return: Обновленный отель или ошибка
    """
    # Проверяем, что хотя бы одно поле для обновления указано
    if hotel_data.title is None and hotel_data.hotel_name is None:
        raise HTTPException(status_code=400, detail="Необходимо предоставить данные для обновления")

    # Ищем отель по ID
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            # Обновляем только те поля, которые переданы
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title
            if hotel_data.hotel_name is not None:
                hotel['name'] = hotel_data.hotel_name
            return hotel  # Возвращаем обновленный отель

    # Если отель не найден, возвращаем ошибку
    raise HTTPException(status_code=404, detail="Отель не найден")


@router.get("/hotels")
def paginated_hotel(
    paginatoin: PaginationDep,
    id: int | None = Query(default=None, description="ID города"),
    hotel_name: str | None = Query(default=None, description="Название отеля"),
):

    """
    Получить список отелей с поддержкой пагинации (page и size).
    """
    global hotels

    hotel_ = [
        hotel for hotel in hotels
        if (id is None or id == hotel['id']) and
           (hotel_name is None or hotel_name == hotel['name'])
    ]
    if paginatoin.page and paginatoin.per_page:
        return hotel_[paginatoin.per_page * (paginatoin.page - 1):][:paginatoin.per_page]
    return hotel_
