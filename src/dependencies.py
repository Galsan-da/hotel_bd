from pydantic import BaseModel
from fastapi import Query, Depends
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=None, ge=0,  description="Номер страницы для отображения")]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=10, description="Количество записей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]