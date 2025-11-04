from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(None, description="Номер страницы", ge=1 )]
    per_page: Annotated[int, Query(None, description="Элементов на странице", ge= 1, lt=10)]


PaginationDep = Annotated[PaginationParams, Depends()]