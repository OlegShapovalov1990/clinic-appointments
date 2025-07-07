from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime
from app.exceptions import AppointmentNotFoundException, DoctorBusyException
from app.models import Appointment
from app.schemas import AppointmentCreate, AppointmentResponse


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, appointment_data: AppointmentCreate) -> AppointmentResponse:
        start_time: datetime = appointment_data.start_time
        # duration из схемы (по умолчанию 30)
        duration = getattr(appointment_data, "duration", 30)
        end_time = Appointment.calculate_end_time(start_time, duration)


        conflict = (
            self.db.query(Appointment)
            .filter(
                Appointment.doctor_id == appointment_data.doctor_id,
                Appointment.start_time < end_time,
                Appointment.end_time > start_time,
            )
            .first()
        )
        if conflict:
            # если нашли, кидаем наш эксепшн
            raise DoctorBusyException(appointment_data.doctor_id, start_time.isoformat())

        # нет конфликта — создаём
        appointment = Appointment(
            patient_name=appointment_data.patient_name,
            doctor_id=appointment_data.doctor_id,
            start_time=start_time,
            end_time=end_time,
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)

        return AppointmentResponse.model_validate(appointment)

    def get_appointment(self, appointment_id: UUID) -> AppointmentResponse:
        appointment = (
            self.db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )
        if not appointment:
            raise AppointmentNotFoundException(str(appointment_id))
        return AppointmentResponse.model_validate(appointment)

