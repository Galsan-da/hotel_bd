from pydantic import BaseModel
from fastapi import Query, Depends
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1,ge=1, description="Номер страницы для отображения")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Количество записей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]