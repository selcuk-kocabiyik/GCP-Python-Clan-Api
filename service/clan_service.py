from sqlalchemy.orm import Session
from model.table_model import ClanTable
from model.schema import ClanCreate, ClanResponse, SortOrder, SortField, ClanRow
from fastapi import HTTPException, status
from uuid import UUID
from typing import Optional, List
from sqlalchemy import asc, desc


def insert_clan(db: Session, clan: ClanCreate):
    existing = db.query(ClanTable).filter(
        ClanTable.name == clan.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Clan already exists."
        )

    try:
        new_clan = ClanTable(
            name=clan.name,
            region=clan.region
        )
        db.add(new_clan)
        db.commit()
        db.refresh(new_clan)
    except Exception as e:
        db.rollback()
        print(f"Insert error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while creating the clan."
        )

    return ClanResponse(
        message= "Clan created successfully.",
        id=new_clan.id
    )


def delete_clan(db: Session, clan_id: UUID):
    existing = db.query(ClanTable).filter(
        ClanTable.id == clan_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Clan deletion failed: clan doesn't exist."
        )

    try:
        db.delete(existing)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Delete error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during the deletion process."
        )

    return ClanResponse(
        message = "Clan deleted successfully.",
        id=None
    )


def get_clans(
        db: Session,
        sort_by: SortField = SortField.created_at,
        sort_order: SortOrder = SortOrder.asc
        ) -> List[ClanTable]:
    
    query = db.query(ClanTable)

    if sort_by is None:
        sort_by = "created_at"

    if sort_order is None:
        sort_order = "desc"

    column = getattr(ClanTable, sort_by.value)

    if sort_order == SortOrder.asc:
        query = query.order_by(asc(column))
    else:
        query = query.order_by(desc(column))


    return query.all()


def get_clan_by_id(db: Session, clan_id: UUID) -> ClanTable:
    clan = db.query(ClanTable).filter(ClanTable.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clan not found")
    return ClanRow.from_orm(clan)