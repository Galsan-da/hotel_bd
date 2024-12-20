from pydantic import BaseModel
from fastapi import Query, Depends
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(ge=0, default=None, description="Номер страницы для отображения")]
    per_page: Annotated[int | None, Query(ge=1, le=10, description="Количество записей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]