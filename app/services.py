from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.exceptions import AppointmentNotFoundException
from app.models import Appointment
from app.schemas import AppointmentCreate, AppointmentResponse


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment_data: AppointmentCreate):
        appointment = Appointment(
            patient_name=appointment_data.patient_name,
            doctor_id=appointment_data.doctor_id,
            start_time=appointment_data.start_time,
            end_time=Appointment.calculate_end_time(appointment_data.start_time),
        )

        self.db.add(appointment)

        try:
            self.db.commit()
            self.db.refresh(appointment)
            return AppointmentResponse.model_validate(appointment)
        except Exception as e:
            self.db.rollback()
            print(f"Ошибка при коммите: {str(e)}")
            raise

        # Убедитесь, что объект имеет ID
        if not appointment.id:
            raise HTTPException(500, "Failed to save appointment")

        return AppointmentResponse.model_validate(appointment)

    def get_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        appointment = (
            self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        )
        if not appointment:
            raise AppointmentNotFoundException(appointment_id)
        return AppointmentResponse.model_validate(appointment)
