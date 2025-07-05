from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Appointment
from app.schemas import AppointmentCreate, AppointmentResponse
from app.exceptions import DoctorBusyException


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment_data: AppointmentCreate) -> AppointmentResponse:
        end_time = Appointment.calculate_end_time(appointment_data.start_time)

        appointment = Appointment(
            patient_name=appointment_data.patient_name,
            doctor_id=appointment_data.doctor_id,
            start_time=appointment_data.start_time,
            end_time=end_time
        )

        self.db.add(appointment)
        try:
            self.db.commit()
            self.db.refresh(appointment)
        except IntegrityError:
            self.db.rollback()
            raise DoctorBusyException(
                doctor_id=appointment_data.doctor_id,
                start_time=appointment_data.start_time
            )

        return AppointmentResponse.model_validate(appointment)

    def get_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            raise AppointmentNotFoundException(appointment_id)
        return AppointmentResponse.model_validate(appointment)