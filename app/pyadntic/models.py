import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Body
from pydantic import BaseModel, Field

from app.db.models import OperationType


class Pagination(BaseModel):
    offset: int = Field(default=0, ge=0, description="Начало чтения записей")
    limit: int = Field(default=10, ge=1, description="Количество записей")


PaginationDep = Annotated[Pagination, Depends()]


class OperationParams(BaseModel):
    operation: OperationType = Field(description="Тип операции")
    amount: int = Field(gt=0, description="Сумма")


ParamsDep = Annotated[OperationParams, Body()]


class HistorySchema(BaseModel):
    id: UUID
    operation_type: str
    time: datetime.datetime
    account_id: UUID
