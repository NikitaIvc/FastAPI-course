from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int
    per_page: int


def get_pagination(
    page: int = Query(1, description="Номер страницы", ge=1),
    per_page: int = Query(10, description="Элементов на странице", ge=1, lt=100)
):
    return PaginationParams(page=page, per_page=per_page)


PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]