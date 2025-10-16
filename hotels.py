from fastapi import Query, HTTPException
from fastapi import APIRouter

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dybai", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None,description="Айди"),
        title: str | None = Query(None,description="Название отеля"),
        page: int = Query(1, description="Номер страницы"),
        per_page: int = Query(3, description="Элементов на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)


    start = (page - 1) * per_page
    end = start + per_page

    if start >= len(hotels_):
        raise HTTPException(status_code=404, detail="Страница не найдена")

    return hotels_[start:end]


@router.patch("{hotel_id}")
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.post("")
def create_hotel(hotel_data = Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data = Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"name": hotel_data.name, "title": hotel_data.title})
            return {"hotel": hotel}

    raise HTTPException(status_code=404, detail="Отель не найден")


@router.delete("/{hotel_id}")
def hotels_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}