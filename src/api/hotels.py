from fastapi import APIRouter, Query, HTTPException, Body, Depends

from sqlalchemy import insert, select

from src.api.dependencies import PaginationParams, PaginationDep
from src.db import async_session_maker
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Айди"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if location is not None:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        if title is not None:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))

        query = query.limit(pagination.per_page)

        query = query.offset(pagination.per_page * (pagination.page - 1))

        # query = (
        #     select(HotelsORM).
        #     filter_by(location=location, title=title)
        #     .limit(pagination.per_page)
        #     .offset(pagination.per_page * (pagination.page - 1))
        # )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels





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
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{
        "summary": "Сочи",
        "value": {
            "title": "Rich Hotel",
            "location": "Сочи, ул. Моря 1",
        }
    },
    "2":{
        "summary": "Dybai",
        "value": {
            "title": "Dybai Rich Hotel",
            "location": "Дубай, ул. Шейха 1"
        }
    }
})):
    async with async_session_maker() as session:
        add_hotels_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotels_stmt)
        await session.commit()

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