from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClanTable(Base):
    __tablename__ = "clans"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    region = Column(String(10), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW() AT TIME ZONE 'UTC'"),
        nullable=False
    )
