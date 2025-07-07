from datetime import datetime, timedelta

from sqlalchemy import UUID, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import text

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    patient_name = Column(String, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = ({"comment": "Table for storing doctor appointments"},)

    @classmethod
    def calculate_end_time(cls, start_time: datetime, duration: int = 30) -> datetime:
        return start_time + timedelta(minutes=duration)
