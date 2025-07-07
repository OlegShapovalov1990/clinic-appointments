class DoctorBusyException(Exception):
    def __init__(self, doctor_id: int, start_time: str):
        self.doctor_id = doctor_id
        self.start_time = start_time
        super().__init__(f"Doctor {doctor_id} is busy at {start_time}")


class AppointmentNotFoundException(Exception):
    def __init__(self, appointment_id: str):
        self.appointment_id = appointment_id
        super().__init__(f"Appointment {appointment_id} not found")
