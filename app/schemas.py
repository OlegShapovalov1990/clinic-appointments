from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class AppointmentBase(BaseModel):
    patient_name: str
    doctor_id: int
    start_time: datetime


class AppointmentCreate(AppointmentBase):
    @field_validator("start_time")
    def validate_start_time(cls, value):
        if value.minute not in (0, 30):
            raise ValueError("Appointments can only start at full or half hours")
        if value.second != 0 or value.microsecond != 0:
            raise ValueError("Seconds and microseconds must be zero")
        return value


class AppointmentResponse(AppointmentBase):
    id: UUID
    end_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True
