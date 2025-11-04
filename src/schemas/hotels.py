from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str


class HotelPATCH(BaseModel):
    name: str | None = Field(None)
    title: str | None = Field(None)