import uvicorn
from fastapi import FastAPI, Query, Body, HTTPException
from typing import Optional

app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dybai", "name": "dubai"}
]



@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None,description="Айди"),
        title: str | None = Query(None,description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_



@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        name: Optional[str] = Body(None),
        title: Optional[str] = Body(None),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return hotel
    return {"error": "Hotel not found!"}



@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    name: str = Body(None),
    title: str = Body(None)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel.update({"name": name, "title": title})
            return {"hotel": hotel}

    raise HTTPException(status_code=404, detail="Отель не найден")


@app.delete("/hotels/{hotel_id}")
def hotels_delete(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)