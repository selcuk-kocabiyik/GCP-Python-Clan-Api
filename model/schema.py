# model/schemas.py

from pydantic import BaseModel
from enum import Enum
from typing import Optional
from uuid import UUID
from datetime import datetime

class ClanCreate(BaseModel):
    name: str
    region: str

class ClanRow(BaseModel):
    id: UUID
    name: str
    region: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class ClanResponse(BaseModel):
    message: str
    id: Optional[UUID]


class SortField(str, Enum):
    created_at = "created_at"
    region = "region"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

