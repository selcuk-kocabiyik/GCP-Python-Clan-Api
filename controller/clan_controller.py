from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from model.database import get_db
from model.schema import ClanCreate, ClanResponse, ClanRow, SortField, SortOrder
from service.clan_service import insert_clan, delete_clan, get_clan_by_id, get_clans
from uuid import UUID
from typing import List

router = APIRouter()

@router.post("/clans", response_model=ClanResponse, status_code=status.HTTP_201_CREATED)
def create_clan(clan: ClanCreate, db: Session = Depends(get_db)):
    return insert_clan(db, clan)

@router.delete("/clans/{id}", response_model=ClanResponse)
def remove_clan(id: UUID, db: Session = Depends(get_db)):
    return delete_clan(db, id)


@router.get("/clans", response_model=List[ClanRow])
def list_all(
    sort_by: SortField = Query(SortField.created_at, description="Sort by 'created_at' or 'region'"),
    sort_order: SortOrder = Query(SortOrder.asc, description="Sort order: 'asc' or 'desc'"),
    db: Session = Depends(get_db)
):
    return get_clans(db, sort_by=sort_by, sort_order=sort_order)

@router.get("/clans/{id}", response_model=ClanRow)
def list_one_clan(id: UUID, db: Session = Depends(get_db)):
    return get_clan_by_id(db, id)
